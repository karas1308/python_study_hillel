from multiprocessing import Process, JoinableQueue
from threading import Semaphore
from time import sleep

from utils.common import run_time


def lucky_ticket(ticket_number, counter, semaphore):
    with semaphore:
        len_ticket_number = len(str(ticket_number))
        ticket_number_part_1 = list(map(int, str(ticket_number)[:len_ticket_number // 2]))
        ticket_number_part_2 = list(map(int, str(ticket_number)[len_ticket_number // 2:]))
        sum_part_1 = sum(ticket_number_part_1)
        sum_part_2 = sum(ticket_number_part_2)
        sleep(1)  # just to see how many threads are active

        if sum_part_1 == sum_part_2:
            print(f"lucky {ticket_number}")
            if isinstance(counter, list):
                counter.append(ticket_number)
            else:
                counter.put(ticket_number)
        else:
            if isinstance(counter, list):
                print(f"wrong {ticket_number}")
            else:
                print(f"wrong {ticket_number}")
                counter.put(None)


@run_time
def process_handler():
    ticket_numbers = (str(a).zfill(2) for a in range(100))
    values = []
    queue = JoinableQueue()
    threads = []
    semaphore = Semaphore(4)
    for ticket_number in ticket_numbers:
        threads.append(Process(target=lucky_ticket, args=[ticket_number, queue, semaphore]))
    for t in threads:
        t.start()
    for t in threads:
        t.join()
        value = queue.get()
        queue.task_done()
        if value:
            values.append(value)
    print(f"COUNT = {len(values)}")


if __name__ == '__main__':
    process_handler()
