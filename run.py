import time
import logging

class TimerContext:
    def __enter__(self):
        self.cotext_start = time.time_ns()

    def __exit__(self, exc_type, exc_value, traceback):
        context_end = time.time_ns()
        delta_time =  context_end - self.cotext_start
        logging.info(f"Execution time {delta_time} ns" )

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

with TimerContext():
    time.sleep(2)


