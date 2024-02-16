# tests/online/conftest.py
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