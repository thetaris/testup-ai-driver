import os


def generate_test_files(input_pairs):
    base_dir = "generated_test_cases"  # Directory to save the generated test case files
    os.makedirs(base_dir, exist_ok=True)  # Create the directory if it doesn't exist

    for pair in input_pairs:
        url = pair["url"]
        filename = pair["filename"].replace('.html', '')
        tasks = pair["tasks"]

        # Create a sanitized class name
        class_name = f"Test{filename.replace('.', '_').replace('-', '_')}"

        # Generate a sanitized filename for Python test files
        test_file_name = os.path.join(base_dir, f"{filename}_test.py")

        with open(test_file_name, 'w') as test_file:  # Write mode to create a new file for each URL
            # Write imports and class definition
            test_file.write(
                "import pytest\nimport logging\nfrom pathlib import Path\nfrom test_utils import assert_chatGPT_response\nfrom action_processor import DomAnalyzer\n\n")
            test_file.write(f"class {class_name}:\n\n")
            test_file.write("    @pytest.fixture\n    def setup(self):\n")
            test_file.write("        # Setup code here, adjust as needed\n")
            test_file.write(
                "        self.instance = DomAnalyzer()\n        logging.info('Test setup completed')\n        yield\n")
            test_file.write("        logging.info('Test teardown initiated')\n        # Teardown code here, if any\n\n")

            # Generate test cases
            for idx, task in enumerate(tasks, start=1):
                test_function = generate_test_function(task, idx, filename, url)
                test_file.write(f"    {test_function}\n\n")


def generate_test_function(task, idx, filename, url):
    """Generates the string representation of a test function."""
    template = f"""def test_case_{idx}(self, setup, data_file_path):
        logging.info('Starting test case {idx}: {task["task"]} on URL: {url}')
        session_id = 1234
        user_prompt = \"\"\"{task["task"]}\"\"\"
        # Locate and read the HTML file
        file_path = data_file_path / '{filename}.html'
        logging.debug(f"Reading HTML file from: {{file_path}}")
        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
        actions_executed = \"\"\"{task["last_played_actions"]}\"\"\"
        expected_action = \"\"\"{task["expected_action"]}\"\"\"
        expected_css_selector = \"\"\"{task["expected_css_selector"]}\"\"\"
        expected_text = \"\"\"{task["expected_text"]}\"\"\"
        logging.debug(f"Calling get_actions with session_id={{session_id}}, user_prompt='{{user_prompt}}', actions_executed={{actions_executed}}, html_content_length={{len(html_content)}} ")
        actual_response = self.instance.get_actions(session_id, user_prompt, html_content, actions_executed)
        assert_chatGPT_response(actual_response, "{task["expected_action"]}", "{task["expected_css_selector"]}", "{task["expected_text"]}")
        logging.info('Test case {idx} completed successfully')"""
    return template


# Define the input pairs and their associated test cases
# website, html_filename
input_pairs = [
  {
    "url": "https://thetaris.org/playground/",
    "filename": "playground_start.html",
    "tasks": [
      {
        "task": "click the button",
        "last_played_actions": "",
        "expected_action": "click",
        "expected_css_selector": "#autoidtestup0",
        "expected_text": "Button clicked"
      }
    ]
  },
  {
    "url": "https://thetaris.org/playground/?page=2",
    "filename": "playground_page2.html",
    "tasks": [
      {
        "task": "enter HelloWorld in the textbox",
        "last_played_actions": "",
        "expected_action": "enter_text",
        "expected_css_selector": "#autoidtestup0",
        "expected_text": "HelloWorld"
      },
      {
        "task": "click ok",
        "last_played_actions": "",
        "expected_action": "click",
        "expected_css_selector": "#autoidtestup1",
        "expected_text": "OK clicked"
      },
      {
        "task": "enter the text HelloWorld and then click ok",
        "last_played_actions": """{
          "steps": [
            {
              "action": "enter_text",
              "css_selector": "#autoidtestup0",
              "text": "HelloWorld",
              "explanation": "To input the text HelloWorld as instructed.",
              "description": "Enter the text HelloWorld in the input field."
            }
          ]
        }""",
        "expected_action": "enter_text",
        "expected_css_selector": "#autoidtestup1",
        "expected_text": "HelloWorld, then OK clicked"
      }
    ]
  },
  {
    "url": "https://thetaris.org/playground/?page=3",
    "filename": "playground_page3.html",
    "tasks": [
      {
        "task": "scroll down",
        "last_played_actions": "",
        "expected_action": "scroll",
        "expected_css_selector": "",
        "expected_text": "Scrolled down"
      }
    ]
  },
  {
    "url": "https://mywebsite.testup.io/",
    "filename": "myWebshop_start.html",
    "tasks": [
      {
        "task": "use search field to search for beanie with logo",
        "last_played_actions": "",
        "expected_action": "click",
        "expected_css_selector": "#woocommerce-product-search-field-0",
        "expected_text": "Beanie with logo"
      }
    ]
  },
  {
    "url": "https://mywebsite.testup.io/?s=beanie+with+logo&post_type=product",
    "filename": "myWebshop_searched_beanie_with_logo.html",
    "tasks": [
      {
        "task": "add beanie to cart",
        "last_played_actions": "",
        "expected_action": "click",
        "expected_css_selector": "#autoidtestup41",
        "expected_text": "Beanie added to cart"
      }
    ]
  },
  {
    "url": "https://mywebsite.testup.io/product/beanie-with-logo-2/",
    "filename": "myWebshop_product_page_beanie_with_logo.html",
    "tasks": [
      {
        "task": "add beanie to cart",
        "last_played_actions": "",
        "expected_action": "click",
        "expected_css_selector": "#autoidtestup40",
        "expected_text": "Beanie added to cart"
      }
    ]
  },
  {
    "url": "https://www.bogner.com/de-de/c/herren/453350/",
    "filename": "bogner_herren.html",
    "tasks": [
      {
        "task": "go to the women section",
        "last_played_actions": "",
        "expected_action": "click",
        "expected_css_selector": "#autoidtestup4",
        "expected_text": "Navigated to women section"
      }
    ]
  },
  {
    "url": "https://www.bogner.com/de-de/c/damen/specials/diesen-monat/570394/?prefn1=productLine&prefv1=bogner",
    "filename": "bogner_damen_neuheiten.html",
    "tasks": [
      {
        "task": "buy any product",
        "last_played_actions": "",
        "expected_action": "click",
        "expected_css_selector": "#onetrust-accept-btn-handler",
        "expected_text": ""
      }
    ]
  },
  {
    "url": "https://www.bogner.com/de-de/p/bogner-leichtdaunenweste-ennie/242-3685-6855-205.html",
    "filename": "bogner_damen_product_page.html",
    "tasks": [
      {
        "task": "add the product to the cart",
        "last_played_actions": "",
        "expected_action": "click",
        "expected_css_selector": "#autoidtestup968",
        "expected_text": "Product added to cart"
      }
    ]
  },
  {
    "url": "https://mywebsite.testup.io/checkout/",
    "filename": "myWebshop_checkout.html",
    "tasks": [
      {
        "task": "fill out the form",
        "last_played_actions": "",
        "expected_action": "enter_text",
        "expected_css_selector": "#billing_first_name",
        "expected_text": "Barbara"
      }
    ]
  }
]

generate_test_files(input_pairs)
