
# AI-Based Website Testing Tool

This project introduces an AI-driven tool to automate website testing through Selenium. By harnessing the power of natural language instructions and Selenium's comprehensive browser automation capabilities, it simplifies executing complex test scenarios on web applications. From adding products to shopping carts and navigating through pages to verifying webpage elements, this tool makes web testing accessible and efficient.

## Features

- **DOM Tree compression** To limit the token count sent to the AI model the first step is to reduce the DOM to relevant information.
- **Automatic ID generation** Ids are added to all DOM elements to ensure back and forth communication with the AI model.
- **Conversation context** The model may use repeated requests to inform the AI about the result of its actions to make sure that the entire task can be completed.
- **Selenium wrapper**: The `SeleniumAIUtils` class wraps the Selenium WebDriver and offers the additional AI functions.

## Usage

Setup the selenium driver as usual then use our wrapper to execute prompts:

```python
selenium_utils = SeleniumAiUtils()
selenium_utils.set_local_driver(driver, url)

selenium_utils.execute_prompt("put any product in shopping cart")
```

# Setup

## Setting up python

Ensure you have the following prerequisites installed on your system before starting:

- Python 3.6 or newer

Follow these steps to set up the tool:

1. Install required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

The following software packages are required, as listed in `requirements.txt`:

- `selenium`: For automating web browser interaction.
- `webdriver-manager`: Helps manage browser drivers easily.
- `flask`: A lightweight WSGI web application framework.
- `requests`: Allows you to send HTTP/1.1 requests easily.
- `beautifulsoup4`: For pulling data out of HTML and XML files.
- `markdownify`: Converts HTML content to Markdown.
- `cachetools`: Provides extensible memorizing collections and decorators.

If you are using an ide you can then add `src` and `examples` to your source root paths and add
`test` to your test root path. Alternatively you can set it up in the shell:

```bash
   export PYTHONPATH=$(pwd)/src
```

## Setting up the OpenAI connection

Before running the tool, you must set up the following environment variable:

- `OPENAI_API_KEY`: Your OpenAI API key for processing natural language commands.

To limit the amount of traffic to the API you can optionally set the following environment variables:

- `MAX_REQUESTS`: The maximum number of API requests per minute (default is 20).
- `MAX_TOKENS`: The maximum number of tokens (input characters) per minute (default is 160000).

You may want to consider setting up these variables in your environment or through a `.env` file in the project's root directory for security reasons.


# Usage

## Interactive Mode

This mode allows real-time natural language commands for web application interaction. Users can change URLs, navigate, click, input data, and exit as needed.
To start using the tool:

1. Run the app:
   ```bash
   python example/selenium_ai_app.py
   ```

## Example Test Script

If you want to write your own standalone test, please refer to our reference file
`testup_mywebshop.py`,  for an automation script example. It illustrates the use of the api
using a simple selneium wrapper. It opens a demo web shop, adds a product to a shopping
cart and checks out. Each step is tested with selenium core functions, demonstrating the mix between
AI and traditional testing methods.

1. Open and customize `examples/testup_mywebshop.py` to fit your test scenario.
2. Execute the script:
   ```bash
   python examples/testup_mywebshop.py
   ```

The script initiates a browser session, performs the defined actions, and automatically closes the browser upon completion or error.

You may Adapt `examples/testup_mywebshop.py` or create new scripts using the `SeleniumUtils` class
for AI-driven Selenium interactions and the `execute_prompt` method for AI-driven navigation
and actions.


## Contributing

Contributions are welcome! Fork the repository, make your changes, and submit a pull request.
