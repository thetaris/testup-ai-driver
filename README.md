
# Testup AI driver

This project introduces an AI-driven tool to automate website testing through Selenium. By harnessing the power of natural language instructions and Selenium's comprehensive browser automation capabilities, it simplifies executing complex test scenarios on web applications. From adding products to shopping carts and navigating through pages to verifying webpage elements, this tool makes web testing accessible and efficient.

This tool is brought to you by [testup.io](https://testup.io),
the easist no-code test automation tool on the web.

## Features

- **DOM Tree compression** To limit the token count sent to the AI model the first step is to reduce the DOM to relevant information.
- **Automatic ID generation** Ids are added to all DOM elements to ensure back and forth communication with the AI model.
- **Conversation context** The model may use repeated requests to inform the AI about the result of its actions to make sure that the entire task can be completed.
- **Selenium wrapper**: The `SeleniumAIUtils` class wraps the Selenium WebDriver and offers the additional AI functions.
- **Training data**: By running parameter fine tuning against our sample data you can significantly increase the accuracy of the results.

## Usage

Setup the selenium driver as usual then use our wrapper to execute prompts:

```python
selenium_utils = SeleniumAiUtils()
selenium_utils.set_local_driver(driver, url)

selenium_utils.execute_prompt("put any product in shopping cart")
```

# Setup

## Setting up python and selenium

1. Make sure you have python installed and add the requireds from the `requirements.txt` file:
   ```bash
   pip install -r requirements.txt
   ```

2. Make sure you have ChromeDriver installed and added to your system's PATH. Instructions for installing ChromeDriver can be found at [ChromeDriver - WebDriver for Chrome](https://sites.google.com/a/chromium.org/chromedriver/).


3.  If you are using an ide you can then add `src` and `examples` to your source root paths and add
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
   python examples/selenium_ai_app.py
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


# Model Fine-Tuning
Fine-tuning a model will help ensuring getting more accurate results from the gpt model, the process requires training data in a specific format, this section guides you through the process of preparing your training data and executing the fine-tuning
by converting HTML content to Markdown, which is a preferred format for text-based machine learning tasks due to its simplicity, readability and reduced size.


## HTML to Markdown Conversion
The first step of training is to reduce the HTML content from `scripts/data/input` directory.  Execute the following command from your project's root directory:
```bash
cd scripts
python prepare_training_data.py
```
## Fine-Tuning Your Model
Once your data is prepared and converted to Markdown, you can fine-tune your model using the provided script. Execute the fine-tuning script with the following command, which will use the converted Markdown data for training:
   ```bash
  python3 fine_tune.py
  ```
The script will process the training data and initiate the fine-tuning job. It will continue to run until the fine-tuning is complete, at which point it will display the new model ID.

## Setting the New Trained Model
After the fine-tuning process is finished and you have your new model ID, you can set your environment to use this trained model for future tasks:
```bash
export GPT_MODEL=<new trained model>
```

Replace `<new trained model>` with the actual model ID provided after the fine-tuning process.

# Contributing
Contributions are welcome! Fork the repository, make your changes, and submit a pull request.
