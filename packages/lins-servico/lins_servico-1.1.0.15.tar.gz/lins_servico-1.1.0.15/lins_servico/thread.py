from lins_servico.exceptions import ProcessInterrupted
from lins_servico.utils import is_time_between
import utils

from datetime import datetime, timedelta, time
import threading
import signal

import logging

class Thread(threading.Thread):
    def __init__(self, interval, execute, stop_time_interval=None, *args, **kwargs):
        threading.Thread.__init__(self)

        self.daemon = False
        self.stopped = threading.Event()
        self.interval = timedelta(seconds=interval)
        self.execute = execute
        self.stop_time_interval = stop_time_interval
        self.args = args
        self.kwargs = kwargs

        signal.signal(signal.SIGTERM, self.signal_handler)
        signal.signal(signal.SIGINT, self.signal_handler)

    def stop(self):
        self.stopped.set()
        self.join()

    def run(self):
        pause_run = False

        while not self.stopped.wait(self.interval.total_seconds()):
            if self.stop_time_interval:
                if 'inicio' in self.stop_time_interval and 'fim' in self.stop_time_interval and 'thread_name' in self.stop_time_interval:
                    thread_name = self.stop_time_interval['thread_name']

                    inicio = self.stop_time_interval['inicio']
                    hora_ini = inicio.split(':')

                    fim = self.stop_time_interval['fim']
                    hora_fim = fim.split(':')

                    pause_run = is_time_between(
                        time(int(hora_ini[0]), int(hora_ini[1])),
                        time(int(hora_fim[0]), int(hora_fim[1]))
                    )

            if pause_run:
                time_now = datetime.utcnow().time()
                logging.debug(f'{time_now} - Pause thread [{thread_name}] from {inicio} to {fim} - waiting...')
                self.stopped.wait(1)
                continue
            else:
                try:
                    self.execute(*self.args, **self.kwargs)
                except Exception as err:
                    logging.critical(err, exc_info=True)

    def signal_handler(self, signum, frame):
        raise ProcessInterrupted