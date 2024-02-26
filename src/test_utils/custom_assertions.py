import re


def assert_chatGPT_response(data, expected_action, expected_css_selector, expected_text=None):
    # Check if the action of the first step is equal to the expected action
    assert data['steps'][0][
               'action'] == expected_action, f"Expected action '{expected_action}', but got '{data['steps'][0]['action']}'"

    # Check if the css_selector is similar to the expected css_selector
    actual_css_selector = data['steps'][0]['css_selector']
    # Prepare the expected CSS selector for regex match (escaping special characters)
    escaped_expected_css_selector = re.escape(expected_css_selector)
    # Pattern to match the expected CSS selector with possible prefix like "button" or similar
    pattern = rf"(.*\s)?{escaped_expected_css_selector}$"
    assert re.match(pattern,
                    actual_css_selector), f"CSS selector '{actual_css_selector}' does not match the expected pattern '{expected_css_selector}'"

    # If the action is "text", check that the text matches the expected text
    if expected_action == "text":
        actual_text = data['steps'][0]['text']
        assert actual_text == expected_text, f"Expected text '{expected_text}', but got '{actual_text}'"


# Example usage
data = {
    "steps": [
        {
            "action": "scroll",
            "css_selector": "",
            "text": "",
            "explanation": "Scrolling down to complete the task",
            "description": "Scroll down using the Page Down key or the scroll bar"
        },
        {
            "action": "click",
            "css_selector": "#testupautoid1234",
            "text": "",
            "explanation": "Scrolling down to complete the task",
            "description": "Scroll down using the Page Down key or the scroll bar"
        },
        {
            "action": "text",
            "css_selector": "#testupautoid1111",
            "text": "some text",
            "explanation": "writing a text ",
            "description": "write sth"
        },
    ]
}

# Call the custom assert function with example expectations
try:
    assert_chatGPT_response(data, "scroll", "#testupautoid1234")
    print("Test passed.")
except AssertionError as e:
    print(f"Test failed: {e}")
