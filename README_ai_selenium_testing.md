# AI-Based Website Testing Tool

This project provides an AI-driven tool to automate website testing using Selenium. It enables the execution of complex test scenarios on web applications, including adding products to shopping carts, navigating through pages, and verifying web page elements, all with the power of natural language instructions and Selenium.

## Features

- **Natural Language Understanding**: Execute tests through simple English prompts, making it accessible even to those with minimal coding experience.
- **Selenium Integration**: Leverages the Selenium WebDriver for robust browser automation and testing capabilities.


## Prerequisites

Before you can run this tool, you'll need to have the following installed:

- Python 3.6 or newer
- Selenium WebDriver
- ChromeDriver (or any compatible driver for your browser of choice)

## Installation

1. Clone the repository to your local machine:

```bash
git clone git@bitbucket.org:thetaris/testup-prompt-service.git
cd testup-prompt-service
```

2. Install the required Python packages:

```bash
pip install -r requirements.txt
```

3. Make sure you have ChromeDriver installed and added to your system's PATH. Instructions for installing ChromeDriver can be found at [ChromeDriver - WebDriver for Chrome](https://sites.google.com/a/chromium.org/chromedriver/).

## Usage

To use this tool, you simply need to run the provided script after customizing it for your test scenario:

1. Open `your_test_script.py` with your favorite text editor.
2. Customize the test steps within the script to match your specific testing needs.
3. Execute the script:

```bash
python your_test_script.py
```

The script will initiate the browser, perform the specified actions, and automatically close the browser upon completion or in case of an error.

## Example Test Script

An example script is provided in the repository (`example_test.py`). It demonstrates how to automate adding a product to a shopping cart and proceeding to checkout, with checks at each step to ensure the process works as expected.

## Customizing Test Scripts

You can customize or create new test scripts by following the structure provided in `example_test.py`. Use the `SeleniumUtils` class for simplified interactions with Selenium and the `execute_prompt` method for AI-driven navigation and actions.

## Contributing

Contributions to this project are welcome! Please feel free to fork the repository, make your changes, and submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Additional Features

### ASCII Art and Welcome Message

Upon starting the tool, users are greeted with ASCII art of "testup.io" followed by a welcoming message. This message provides a quick guide on how to use the application, including how to enter interactive mode or run a test script, and how to specify the browser window resolution and the website URL to start with.

### Interactive Mode

The tool also supports an interactive mode, allowing users to enter natural language commands in real-time to interact with the web application being tested. Users can switch the website URL on the fly, execute commands to perform actions like navigating, clicking, or inputting data, and exit the mode when finished.

### Command Line Arguments

Users have the option to customize their testing session via command-line arguments, such as setting the browser window resolution and specifying the initial website URL. This flexibility allows for tailored testing experiences based on individual needs or test requirements.

## Getting Started

To leverage these additional features, simply follow the usage instructions provided in the previous sections. The tool is designed to be intuitive and user-friendly, making web testing accessible to users with varying levels of technical expertise.
