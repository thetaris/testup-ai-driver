import os

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
  }
]




# Session_id to use for all tests
session_id = 1234

# Function to generate test files
def generate_test_files(input_pairs):
    # Create a directory for the test files if it doesn't exist
    test_dir = "test_files"
    os.makedirs(test_dir, exist_ok=True)

    i = 0
    for item in input_pairs:
        website = item['url']
        html_filename = item['filename']
        tasks = item['tasks']

        # Sanitize and create a unique test file for each website
        safe_website_name = sanitize_filename(html_filename.replace("https://", "").replace("/", "_").replace(".html", "_").strip("_"))
        test_file_path = os.path.join(test_dir, f"test_{safe_website_name}.py")

        with open(test_file_path, "w") as test_file:
            # Write imports, setup code for pytest, and logging configuration
            test_file.write("import pytest\n")
            test_file.write("import logging\n")
            test_file.write("from pathlib import Path\n")
            test_file.write("from test_utils import assert_chatGPT_response\n")

            test_file.write("from action_processor import DomAnalyzer  \n\n")
            test_file.write("logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')\n")
            test_file.write(f"# Test cases for {website}\n")
            test_file.write(f"class Test{safe_website_name.replace('.', '_').replace('-', '_')}:\n\n")
            test_file.write("    @pytest.fixture\n")
            test_file.write("    def setup(self):\n")
            test_file.write("        # Setup code here, adjust as needed\n")
            test_file.write("        self.instance = DomAnalyzer()\n")
            test_file.write("        logging.info('Test setup completed')\n")
            test_file.write("        yield\n")
            test_file.write("        logging.info('Test teardown initiated')\n")
            test_file.write("        # Teardown code here, if any\n\n")


            # Generate a test function for each task
            for task_element in tasks:
                task = task_element['task']
                last_played_actions = task_element['last_played_actions']
                expected_action = task_element['expected_action']
                expected_css_selector = task_element['expected_css_selector']
                expected_text = task_element['expected_text']

                i = i + 1

                test_file.write(f"    def test_case_{i}(self, setup, data_file_path):\n")
                test_file.write(f"        logging.info('Starting test case {i}: {task}')\n")
                test_file.write(f"        session_id = {session_id}\n")
                test_file.write(f"        user_prompt = \"{task}\"\n")
                test_file.write(f"        # Locate and read the HTML file\n")
                test_file.write(f"        file_path = data_file_path / '{html_filename}'\n")
                test_file.write(f"        logging.debug(f\"Reading HTML file from: {{file_path}}\")\n")
                test_file.write(f"        with open(file_path, 'r', encoding='utf-8') as file:\n")
                test_file.write(f"            html_content = file.read()\n")
                test_file.write(f"        actions_executed = \"\"\"{last_played_actions}\"\"\"\n")
                test_file.write(f"        expected_action = \"{expected_action}\"\n")
                test_file.write(f"        expected_css_selector = \"{expected_css_selector}\"\n")
                test_file.write(f"        expected_text = \"{expected_text}\"\n")
                test_file.write(f"        logging.debug(f\"Calling get_actions with session_id={{session_id}}, user_prompt='{{user_prompt}}', actions_executed={{actions_executed}}, html_content_length={{len(html_content)}} \")\n")

                test_file.write(f"        actual_response = self.instance.get_actions(session_id, user_prompt, html_content, actions_executed)\n")
                test_file.write(f"        assert_chatGPT_response(actual_response, \"{expected_action}\", \"{expected_css_selector}\", \"{expected_text}\")\n")
                test_file.write(f"        logging.info('Test case {i} completed successfully')\n\n")

            print(f"Generated test file: {test_file_path}")

def sanitize_filename(filename):
    """Sanitize the filename by replacing or removing characters not allowed in Windows filenames."""
    return "".join([c if c not in "\\/:*?\"<>|" else "_" for c in filename])



# Call the function to generate test files
generate_test_files(input_pairs)
