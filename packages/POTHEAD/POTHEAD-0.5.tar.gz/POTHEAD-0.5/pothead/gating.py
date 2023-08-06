from time import sleep, time
from math import ceil

from psutil import Process, cpu_count, cpu_times

# How often to poll the CPU, compared to the moving-average of the job-start-interval
CPU_IDLE_POLL_DIVISOR = 20

# Polling the cpu-idle more often than this is bound to give noisy results
# If your application consumes jobs more often than this, pothead probably is not for you
CPU_IDLE_POLL_MIN_INTERVAL = 0.050
CPU_IDLE_POLL_MAX_INTERVAL = 2

# Jobs will still be clamped to idle CPU, but we want SOME kind of upper bound on concurrency, to avoid I/O
# blockage causing ridiculous amounts of work
DEFAULT_MAX_CONCURRENT_MULTIPLIER = 2

__all__ = ["wait_for_idle_cpus"]


class MovingAverage:
    def __init__(self, init=0, inertia=0.6):
        self.value = init
        self.speed = 1 - inertia
        self.inertia = inertia

    def update(self, value):
        self.value = (self.value * self.inertia) + (value * self.speed)
        return self.value

class Worker:
    def __init__(self, cpu_reservation_amount, keep_cpu_reservation):
        self.cpu_reservation_amount = cpu_reservation_amount
        self.keep_cpu_reservation = keep_cpu_reservation
        self.on_done = None

    def reset_cpu_reservation(self, new_cpu_amount=0):
        self.cpu_reservation_amount = new_cpu_amount
        # Note: we do not call on_done() here, even if the amount would be 0
        # since that would remove a live worker from the list, which would give
        # the wrong worker count

    # Worker callback implementation
    def request_received(self, environ):
        environ['RESET_CPU_RESERVATION'] = self.reset_cpu_reservation
        if not self.keep_cpu_reservation:
            self.reset_cpu_reservation(0)

    # Worker callback implementation
    def done(self):
        self.on_done(self)

class WorkerList:
    def __init__(self):
        self.workers = set()

    def add_worker(self, worker):
        worker.on_done = lambda w : self.workers.remove(w)
        self.workers.add(worker)
        return worker

    def count(self):
        return len(self.workers)

    def reserved_cpu_amount(self):
        return sum([w.cpu_reservation_amount for w in self.workers])


"""Timed measurement on an incrementing counter

Reads the counter, divides with time passed since last reading, and smooths the value using a moving average
"""


class InertialTimeDerivate:
    def __init__(self, func, initial, inertia):
        self.func = func
        self.last_value = self.func()
        self.last_check = time()
        self.inertial_value = MovingAverage(initial, inertia)

    def update(self):
        new_value = self.func()
        this_check = time()
        elapsed = this_check - self.last_check
        delta = new_value - self.last_value
        self.last_check = this_check
        self.last_value = new_value
        return self.inertial_value.update(delta / elapsed)


"""CPU-gated wait_for_slot implementation

Creates a wait_for_slot-callable that will let through at least one concurrent job, and additional jobs as
long as `count` cpu:s are idle. It is cgroup-aware, and will not allow current process and subprocesses to
consume more CPU than configured cgroup-limit.

When a worker is spawned, but before it has received its job request, it will have the CPU amount
specified in the `required` parameter artificially reserved for it. The `keep_cpu_reservation` can be used
for jobs that when started don't immediately use the full amount of CPU that they will do eventually.
In order to avoid spawning lots of such jobs in a short time period before CPU usage has settled, the
artifical CPU reservation can be kept by setting `keep_cpu_reservation` to True. When doing this, the
job should at some later point during its request processing reset the CPU reservation by calling the
function stored under the "RESET_CPU_RESERVATION" key in the HTTP request environment, like so:

    http_request.environ["RESET_CPU_RESERVATION"](new_cpu_amount)

The function may be called several times during the request processing, but the last call should
normally set the amount to 0.
"""


def wait_for_idle_cpus(required, *, max_concurrent=None, fixed_delay=0.2, inertia=0.7, keep_cpu_reservation=False):
    worker_list = WorkerList()
    cpu_wait_time = MovingAverage(1, 0.7)

    process = Process()

    def cpu_used_in_process():
        times = process.cpu_times()
        return times.user + times.system + times.children_user + times.children_system

    # CPU.limits enforced by cgroup, configured by I.E. K8S
    # Authorative docs at https://www.kernel.org/doc/Documentation/scheduler/sched-bwc.txt
    with open("/sys/fs/cgroup/cpu/cpu.cfs_quota_us", "rt") as quota, open(
        "/sys/fs/cgroup/cpu/cpu.cfs_period_us", "rt"
    ) as period:
        quota = int(quota.read())
        if quota > 0:
            cpu_quota = quota / int(period.read())
            if not max_concurrent:
                max_concurrent = ceil(cpu_quota * DEFAULT_MAX_CONCURRENT_MULTIPLIER / required)

            # Precalculate the quota with headroom for a new job
            cpu_quota -= required
        else:
            cpu_quota = None
            if not max_concurrent:
                max_concurrent = ceil(cpu_count() * DEFAULT_MAX_CONCURRENT_MULTIPLIER / required)

    def wait_for_slot(halt):
        if worker_list.count() == 0:
            return worker_list.add_worker(Worker(required, keep_cpu_reservation))

        sleep(fixed_delay)

        start_time = time()

        idle = InertialTimeDerivate(lambda: cpu_times().idle, 0, inertia)
        if cpu_quota:
            cpu_used = InertialTimeDerivate(cpu_used_in_process, cpu_count(), inertia)

        cpu_poll_interval = max(CPU_IDLE_POLL_MIN_INTERVAL, min(cpu_wait_time.value / CPU_IDLE_POLL_DIVISOR, CPU_IDLE_POLL_MAX_INTERVAL))
        while worker_list.count() > 0 and not halt():
            reserved = worker_list.reserved_cpu_amount()
            idle_deriv = idle.update()
            if (
                worker_list.count() < max_concurrent
                and idle_deriv - reserved >= required
                and (cpu_quota is None or cpu_used.update() + reserved <= cpu_quota)
            ):
                cpu_wait_time.update(time() - start_time)
                break

            sleep(cpu_poll_interval)

        return worker_list.add_worker(Worker(required, keep_cpu_reservation))

    return wait_for_slot
