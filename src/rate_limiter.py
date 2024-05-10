import logging
import time
from threading import Lock



logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class RateLimiter:

    def __init__(self, max_requests_per_minute, max_tokens_per_minute):
        self.max_requests_per_minute = max_requests_per_minute
        self.max_tokens_per_minute = max_tokens_per_minute
        self.request_count = 0
        self.token_count = 0
        self.lock = Lock()
        self.window_start = time.time()

    def reset_window(self):
        self.window_start = time.time()
        self.request_count = 0
        self.token_count = 0

    def add_token_consumed(self, token_consumed):
        with self.lock:
            # logging.info("acquired lock to set tokens")
            self.token_count += token_consumed

    def check_and_update_limits(self,num_tokens):
        from gpt_client import TokenLimitExceededError
        # logging.info("Going to wait and check once")
        current_time = time.time()
        elapsed_time = current_time - self.window_start

        if elapsed_time >= 61:  # More than a minute has passed, reset window
            self.reset_window()
        if num_tokens > self.max_tokens_per_minute:
            raise TokenLimitExceededError("Message larger than token per minute limit")
        if self.request_count < self.max_requests_per_minute and (self.token_count + num_tokens) <= self.max_tokens_per_minute:
            self.request_count += 1
            return True
        else:
            return False

    def wait_and_check(self, num_tokens):
        with self.lock:
            # logging.info("acquired lock for availability")
            allowed = self.check_and_update_limits(num_tokens)
            while not allowed:
                # logging.info("waiting for tokens to be available")
                time.sleep(1)
                allowed = self.check_and_update_limits(num_tokens)
            return True
