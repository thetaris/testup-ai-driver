import os

# Define the input pairs and their associated test cases
# website, html_filename
input_pairs = [("https://thetaris.org/playground/", 'playground_start.html', [
    # task , last_played_actions,  expected response
    ("click the button", "", "#autoidtestup0")
]),
               ("https://thetaris.org/playground/?page=2", 'playground_page2.html', [
                   # task ,last_played_actions, expected response
                   ("enter HelloWorld in the textbox", "", "#autoidtestup0"),
                   ("click ok", "", "#autoidtestup1"),
                   ("enter the text HelloWorld and then click ok",
                    """{"action":"enter_text","css_selector":"#autoidtestup0","text":"HelloWorld","explanation":"To input text HelloWorld into the 'input' element with id 'autoidtestup0'","description":"Enter the text HelloWorld into the input field with id 'autoidtestup0'"}""",
                    "#autoidtestup1"),

               ]),
               ("https://thetaris.org/playground/?page=3", 'playground_page3.html', [
                   # task ,last_played_actions, expected response
                   ("scroll down", "", "")
               ]),
               ("https://mywebsite.testup.io/", 'myWebshop_start.html', [
                   # task ,last_played_actions, expected response
                   ("search for beanie with logo", "", "#woocommerce-product-search-field-0")
               ]),
               ("https://mywebsite.testup.io/?s=beanie+with+logo&post_type=product",
                'myWebshop_searched_beanie_with_logo.html', [
                    # task ,last_played_actions, expected response
                    ("add beanie to cart", "", "#autoidtestup41")
                ]),
               ("https://mywebsite.testup.io/product/beanie-with-logo-2/",
                'myWebshop_product_page_beanie_with_logo.html', [
                    # task ,last_played_actions, expected response
                    ("add beanie to cart", "", "#autoidtestup40")
                ]),
               ("https://www.bogner.com/de-de/c/herren/453350/", 'bogner_herren.html', [
                   # task ,last_played_actions, expected response
                   ("go to the women section", "", "#autoidtestup4")
               ]),
               ("https://www.bogner.com/de-de/c/damen/specials/diesen-monat/570394/?prefn1=productLine&prefv1=bogner",
                'bogner_damen_neuheiten.html', [
                    # task ,last_played_actions, expected response
                    ("buy any product", "", "#autoidtestup40")
                ]),
               ("https://www.bogner.com/de-de/p/bogner-leichtdaunenweste-ennie/242-3685-6855-205.html",
                'bogner_damen_product_page.html', [
                    # task ,last_played_actions, expected response
                    ("add the product to the cart", "", "#autoidtestup968")
                ])

               ]


# Session_id to use for all tests
session_id = 1234

# Function to generate test files
def generate_test_files(input_pairs):
    # Create a directory for the test files if it doesn't exist
    test_dir = "test_files"
    os.makedirs(test_dir, exist_ok=True)

    for website, html_filename, test_cases in input_pairs:
        # Sanitize and create a unique test file for each website
        safe_website_name = sanitize_filename(html_filename.replace("https://", "").replace("/", "_").replace(".html", "_").strip("_"))
        test_file_path = os.path.join(test_dir, f"test_{safe_website_name}.py")

        with open(test_file_path, "w") as test_file:
            # Write imports, setup code for pytest, and logging configuration
            test_file.write("import pytest\n")
            test_file.write("import logging\n")
            test_file.write("from pathlib import Path\n")

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
            for i, (task, last_played_actions, expected_response) in enumerate(test_cases, start=1):
                test_file.write(f"    def test_case_{i}(self, setup):\n")
                test_file.write(f"        logging.info('Starting test case {i}: {task}')\n")
                test_file.write(f"        session_id = {session_id}\n")
                test_file.write(f"        user_prompt = \"{task}\"\n")
                test_file.write(f"        # Locate and read the HTML file\n")
                test_file.write(f"        file_path = Path(__file__).parent.parent/ 'data'/ 'online'/ '{html_filename}'\n")
                test_file.write(f"        logging.debug(f\"Reading HTML file from: {{file_path}}\")\n")
                test_file.write(f"        with open(file_path, 'r', encoding='utf-8') as file:\n")
                test_file.write(f"            html_content = file.read()\n")
                test_file.write(f"        actions_executed = \"\"\"{last_played_actions}\"\"\"\n")
                test_file.write(f"        expected_response = \"{expected_response}\"\n")
                test_file.write(f"        logging.debug(f\"Calling get_actions with session_id={{session_id}}, user_prompt='{{user_prompt}}', actions_executed={{actions_executed}}, html_content_length={{len(html_content)}} \")\n")

                test_file.write(f"        actual_response = self.instance.get_actions(session_id, user_prompt, html_content, actions_executed)\n")
                test_file.write(f"        assert actual_response == expected_response, f\"Expected: {expected_response}, but got: {{actual_response}}\"\n")
                test_file.write(f"        logging.info('Test case {i} completed successfully')\n\n")

            print(f"Generated test file: {test_file_path}")

def sanitize_filename(filename):
    """Sanitize the filename by replacing or removing characters not allowed in Windows filenames."""
    return "".join([c if c not in "\\/:*?\"<>|" else "_" for c in filename])



# Call the function to generate test files
generate_test_files(input_pairs)
