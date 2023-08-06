from lins_servico.exceptions import ProcessInterrupted, ZeroThreadRunning

import time
import threading

import logging

class thread_loop():
    def __init__(self, sleep_time=1):
        self.sleep_time = sleep_time

    def __call__(self, function):
        def thread_loop(*args):
            thread_list = function(*args)

            for item in thread_list:
                item.start()

            while True:
                try:
                    qtd_threads_ativas = threading.active_count()-1

                    if qtd_threads_ativas == 0:
                        raise ZeroThreadRunning('NO THREADS ARE RUNNING.')

                    logging.debug(f'RUNNING {qtd_threads_ativas} THREADS - SLEEP TIME: {self.sleep_time}s')
                    time.sleep(self.sleep_time)

                except ProcessInterrupted:
                    logging.critical('PROCESS INTERRUPTED - KILLING THREADS.')

                    for item in thread_list:
                        item.stop()

                    break

                except ZeroThreadRunning as err:
                    logging.critical(f'{type(err).__name__} - KILLING THREADS.')

                    for item in thread_list:
                        item.stop()

                    break
                
        return thread_loop