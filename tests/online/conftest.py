# tests/online/conftest.py
import logging
from datetime import datetime
from pathlib import Path
import dotenv

import pytest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src')))


@pytest.fixture(scope="session")
def system_input():
    return """Your system input text for online tests here..."""


@pytest.fixture(scope="session")
def user_input():
    return """Your user input text for online tests here..."""


@pytest.fixture(scope="session")
def data_file_path():
    return Path(__file__).parent.parent / 'data' / 'online'


def pytest_configure(config):
    dotenv.load_dotenv()
    log_folder = "logs"
    os.makedirs(log_folder, exist_ok=True)  # Create the folder if it doesn't exist

    date_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_filename = f"{log_folder}/online_test_log_{date_str}.log"
    logging.basicConfig(
        filename=log_filename,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # This dictionary will store the test results
    test_results = {"passed": [], "failed": []}

    def pytest_runtest_makereport(item, call):
        if call.when == 'call':  # We're interested in the call phase for actual test outcomes
            if call.excinfo is None:
                test_results["passed"].append(item.nodeid)
            else:
                test_results["failed"].append(item.nodeid)

    def pytest_sessionfinish(session, exitstatus):
        log_folder = "test_summaries"
        os.makedirs(log_folder, exist_ok=True)  # Ensure the directory exists
        date_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        results_filename = f"{log_folder}/online_test_results_{date_str}.txt"

        with open(results_filename, "w") as f:
            f.write("Passed tests:\n")
            for test in test_results["passed"]:
                f.write(f"{test}\n")
            f.write("\nFailed tests:\n")
            for test in test_results["failed"]:
                f.write(f"{test}\n")

        print(f"Test results written to {results_filename}")
