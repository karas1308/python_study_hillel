from multiprocessing import Semaphore
from threading import Thread

from multy_tasks.use_process import lucky_ticket
from utils.common import run_time


@run_time
def tread_handler():
    threads = []
    ticket_numbers = (str(a).zfill(4) for a in range(10000))
    count = []
    semaphore = Semaphore(4)
    for ticket_number in ticket_numbers:
        threads.append(Thread(target=lucky_ticket, args=[ticket_number, count, semaphore]))
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print(f"COUNT = {len(count)}")


if __name__ == '__main__':
    tread_handler()
