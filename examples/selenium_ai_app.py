from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium_ai_utils import SeleniumAiUtils  # Make sure this is correctly imported
import re
import argparse


def display_start_screen():
    # ASCII art for "testup.io"
    ascii_art_testup = r"""

 .----------------.  .----------------.  .----------------.  .----------------.  .----------------.  .----------------.  .----------------.  .----------------.  .----------------. 
| .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. |
| |  _________   | || |  _________   | || |    _______   | || |  _________   | || | _____  _____ | || |   ______     | || |              | || |     _____    | || |     ____     | |
| | |  _   _  |  | || | |_   ___  |  | || |   /  ___  |  | || | |  _   _  |  | || ||_   _||_   _|| || |  |_   __ \   | || |              | || |    |_   _|   | || |   .'    `.   | |
| | |_/ | | \_|  | || |   | |_  \_|  | || |  |  (__ \_|  | || | |_/ | | \_|  | || |  | |    | |  | || |    | |__) |  | || |              | || |      | |     | || |  /  .--.  \  | |
| |     | |      | || |   |  _|  _   | || |   '.___`-.   | || |     | |      | || |  | '    ' |  | || |    |  ___/   | || |              | || |      | |     | || |  | |    | |  | |
| |    _| |_     | || |  _| |___/ |  | || |  |`\____) |  | || |    _| |_     | || |   \ `--' /   | || |   _| |_      | || |      _       | || |     _| |_    | || |  \  `--'  /  | |
| |   |_____|    | || | |_________|  | || |  |_______.'  | || |   |_____|    | || |    `.__.'    | || |  |_____|     | || |     (_)      | || |    |_____|   | || |   `.____.'   | |
| |              | || |              | || |              | || |              | || |              | || |              | || |              | || |              | || |              | |
| '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' |
 '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------' 

    """

    # Welcoming message
    welcome_message = """
    Welcome to AI Selenium Driver, brought to you by testup.io!

    This tool enhances your web interaction automation, allowing you to control web browsers through natural language. 
    Whether you're executing predefined scripts or engaging in interactive commands, your approach to web testing and automation is simplified.

    Quick Start Guide:

    1. **Initialization Parameters**:
       - Browser Resolution: Use '--resolution WIDTHxHEIGHT' to set the window size (default: 1920x1080).
       - Starting Website: Use '--url YOUR_WEBSITE_URL' to begin on a specific site. Without this, we'll start on https://https://mywebsite.testup.io/ as an example.

    2. **Runtime Interaction**:
       - Direct Command: Simply type natural language commands to interact with the web page, such as 'buy warm clothing' or 'complete this form with my details: Max Mustermann, Munich, Germany, phone 089/12345678'.
       - Change Website: Use the '/URL' command to switch sites. You'll be prompted to enter the new website address.
       - Type '/exit' '/q' or '/quit' to quit:"

    Start your streamlined web automation journey with us! For further assistance, refer to our documentation or contact support.
    """

    #  print(ascii_art_testup)
    print(welcome_message)


def display_help_message():
    help_message = """
    Available Commands:
    - /URL [website] : Switch to a specific website. You can directly use '/URL website.com' or just '/URL' and then input the URL when prompted.
    - /exit, /q, /quit : Quit the interactive mode.
    - /help : Display this help message.

    How to Use:
    When you input commands, the AI processes your text and decides on an action: click, enter text, scroll, press enter, or finish. These actions are automatically executed on the webpage via the Selenium WebDriver, and you will see the changes directly in the browser.

    Example Commands:
    - "Click on the login button": The AI will attempt to find and click a login button on the current page.
    - "Enter 'John Doe' in the name field": The AI will look for a name field and enter the text 'John Doe'.
    - "Scroll down": The AI will scroll the webpage down.
    - "Press enter in the search box": The AI will simulate pressing the Enter key in a search box.
    - "Complete the form and submit": The AI will try to fill out a form with previously provided details and submit it.

    Command Tips:
    - Be Clear and Specific: Describe exactly what you want to do. Include any necessary details.
    - Use Natural Language: Phrase your commands in a straightforward manner, as if you were asking another person to perform the task.
    - Provide Context: If your command depends on previous actions or certain conditions, make sure to include that context in your request.

    """
    print(help_message)


def run_interactive_mode(selenium_utils):
    print("Interactive mode. Type '/URL' to switch the website, or ('/exit','/q' or '/quit') to quit:")

    while True:
        # Prompt the user for input
        user_input = input("> ").strip()

        # Check for help command
        if user_input.lower() == '/help':
            display_help_message()
            continue

        # Check if the user wants to exit the interactive mode
        if user_input.lower() in ['/exit', '/quit', '/q']:
            print("Exiting interactive mode. Goodbye!")
            break

        split_input = user_input.split(' ')
        # Handle URL change request
        if split_input[0].lower() == '/url':
            if len(split_input) == 2:
                new_url = split_input[1]
            else:
                new_url = input("Enter the new URL: ").strip()
            original_new_url = new_url  # Store the original input for user feedback
            # Automatically prepend 'http://' if necessary
            if not new_url.startswith(('http://', 'https://')):
                new_url = 'http://' + new_url
            while not validate_url(new_url):
                print("Invalid URL. Please enter a valid URL.")
                new_url = input("Enter the new URL: ").strip()
                original_new_url = new_url  # Update the original input for user feedback
                if not new_url.startswith(('http://', 'https://')):
                    new_url = 'http://' + new_url
            selenium_utils.go_to_url(new_url)
            print(f"Switched to {original_new_url}")  # Show the URL as the user entered it
            continue

        # Handle empty input gracefully
        if not user_input:
            print("Please enter a command, or type 'exit' to quit.")
            continue

        try:
            # Execute the command through SeleniumUtils
            selenium_utils.execute_prompt(user_input)
        except Exception as e:
            # Catch and display any errors that occur during command execution
            print(f"An error occurred: {e}")
            continue

    # Clean up before exiting the interactive mode
    selenium_utils.driver.quit()
    print("The browser has been closed.")


def validate_url(url):
    # Prepend 'http://' if no scheme is specified
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url

    # A simple regex to check for valid URL format
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, url) is not None


def setup_arg_parser():
    parser = argparse.ArgumentParser(description="Control the browser with your words. .")

    # Argument for setting browser resolution
    parser.add_argument('--resolution', default='1920x1080', help='Browser window resolution, default is 1920x1080.')
    parser.add_argument('--url', default='https://mywebsite.testup.io/',
                        help='Website URL to start with. If not specified, will use an example website.')

    return parser


def main():
    display_start_screen()

    parser = setup_arg_parser()
    args = parser.parse_args()

    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument(f"window-size={args.resolution}")
    chrome_options.add_argument("--start-fullscreen")  # This line ensures full screen mode

    driver = webdriver.Chrome(options=chrome_options)
    url = "https://mywebsite.testup.io/"
    selenium_utils = SeleniumAiUtils()
    selenium_utils.set_local_driver(driver, url)

    run_interactive_mode(selenium_utils)


if __name__ == "__main__":
    main()
