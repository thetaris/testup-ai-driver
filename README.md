
# AI-Based Website Testing Tool

This project introduces an AI-driven tool to automate website testing through Selenium. By harnessing the power of natural language instructions and Selenium's comprehensive browser automation capabilities, it simplifies executing complex test scenarios on web applications. From adding products to shopping carts and navigating through pages to verifying webpage elements, this tool makes web testing accessible and efficient.

## Features

- **Natural Language Understanding**: Facilitates test execution through simple English commands, broadening accessibility to users with minimal technical expertise.
- **Selenium Integration**: Utilizes the Selenium WebDriver, offering extensive capabilities for browser automation and testing.

## Prerequisites

Ensure you have the following prerequisites installed on your system before starting:

- Python 3.6 or newer


## Installation

Follow these steps to set up the tool:

1. Install required Python packages:
   ```bash
   pip install -r requirements.txt
   ```


## Software Requirements

To ensure the tool functions correctly, the following software packages are required. These are listed in the `requirements.txt` file:

- `selenium`: For automating web browser interaction.
- `webdriver-manager`: Helps manage browser drivers easily.
- `flask`: A lightweight WSGI web application framework.
- `requests`: Allows you to send HTTP/1.1 requests easily.
- `beautifulsoup4`: For pulling data out of HTML and XML files.
- `markdownify`: Converts HTML content to Markdown.
- `cachetools`: Provides extensible memorizing collections and decorators.


## Environment Configuration

Before running the tool, you must set up the following environment variable:

- `OPENAI_API_KEY`: Your OpenAI API key for processing natural language commands.
 
Additionally, you can set the following environment variables if you want to differ from their default values: 

- `MAX_REQUESTS`: The maximum number of API requests per minute (default is 20).
- `MAX_TOKENS`: The maximum number of tokens (input characters) per minute (default is 160000).

You can set these variables in your environment or through a `.env` file in the project's root directory.


## Usage

### Interactive Mode

This mode allows real-time natural language commands for web application interaction. Users can change URLs, navigate, click, input data, and exit as needed.
To start using the tool:

1. Run the app:
   ```bash
   python selenium_ai_app.py
   ```

### Example Test Script

Refer to `example_testup_mywebshop.py`,  for an automation script example. It illustrates adding a product to a shopping cart and checking out, ensuring each step functions as expected.

To start using the tool:

1. Open and customize `example_testup_mywebshop.py` to fit your test scenario.
2. Execute the script:
   ```bash
   python example_testup_mywebshop.py
   ```

The script initiates a browser session, performs the defined actions, and automatically closes the browser upon completion or error.




## Customizing Test Scripts

Adapt `example_testup_mywebshop.py` or create new scripts using the `SeleniumUtils` class for simplified Selenium interactions and the `execute_prompt` method for AI-driven navigation and actions.


## Contributing

Contributions are welcome! Fork the repository, make your changes, and submit a pull request.

