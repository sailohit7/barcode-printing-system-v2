# printer/print_queue.py

import queue
import threading

from printer.raw_printer import send_raw


class PrintQueue:

    def __init__(self):

        self.queue = queue.Queue()
        self.worker = threading.Thread(target=self._worker)
        self.worker.daemon = True
        self.worker.start()

    # ---------------------------------
    # Add job to queue
    # ---------------------------------
    def add_job(self, label_cmd):

        self.queue.put(label_cmd)

    # ---------------------------------
    # Worker thread
    # ---------------------------------
    def _worker(self):

        while True:

            label_cmd = self.queue.get()

            try:

                send_raw(label_cmd)

                print("Printed job")

            except Exception as e:

                print("Print failed:", e)

            finally:

                self.queue.task_done()

    # ---------------------------------
    # Wait until queue empty
    # ---------------------------------
    def wait_until_done(self):

        self.queue.join()