import sys
import time

try:
    import queue
except ImportError:
    import Queue as queue
from acq4.util.Thread import Thread


class PatchThread(Thread):
    """Background thread that acquires and runs multiple jobs for a single pipette
    """

    class Stopped(Exception):
        """Raised when we request the thread to stop
        """

    def __init__(self, dev, module):
        Thread.__init__(self, name=f"VoltageImaging_PatchThread_{dev.name()}")
        self.dev = dev
        self.jobQueue = module.job_queue
        self.module = module
        self._stop = False

    def stop(self):
        self._stop = True

    def start(self):
        self._stop = False
        Thread.start(self)

    def checkStop(self):
        if self._stop is True:
            raise self.Stopped()

    def run(self):
        while self._stop is False:
            if self.dev.waitingForSwap or self.dev.active is False:
                # wait for user to swap pipette or enable
                time.sleep(0.5)
                continue

            pa = self.jobQueue.request_job(self.dev)
            self._currentPatchAttempt = pa
            if pa is None:
                # no jobs right now; sleep and try again.

                time.sleep(3)
                continue

            try:
                pa.start_logging()
                pa.set_status(f"start patch protocol: {pa.protocol.name}")
                protocol = pa.protocol(self, pa)
                protocol.runPatchProtocol()
                if pa.error is None:
                    pa.set_status("success")
                else:
                    pa.set_status(f"failed: {str(pa.error[1])}")
            except self.Stopped:
                protocol.abortPatchProtocol()
                pa.set_status("aborted")
                return
            except Exception as exc:
                pa.set_error(sys.exc_info())
            finally:
                pa.stop_logging()
