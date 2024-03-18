class TestStep:
    def __init__(self, action, css_selector, text, explanation, description):
        self.action = action
        self.css_selector = css_selector
        self.text = text
        self.explanation = explanation
        self.description = description

    def __str__(self):
        return f"{{\"action\": \"{self.action}\", \"css_selector\": \"{self.css_selector}\", \"Text\": \"{self.text}\", \"explanation\": \"{self.explanation}\", \"description\": \"{self.description}\"}}"

    def to_dict(self):
        return {
            "action": self.action,
            "css_selector": self.css_selector,
            "text": self.text,
            "explanation": self.explanation,
            "description": self.description,
        }


class TestSteps:
    def __init__(self, steps_data):
        self.steps = []

        # Validate that steps_data is not None and it contains 'steps'
        if steps_data is None or 'steps' not in steps_data:
            print("Invalid or missing steps data.")
            return  # Exit the initializer if validation fails

        for step_data in steps_data['steps']:
            # Not all steps have 'text', so we use `get` method to avoid KeyError
            text = step_data.get('text', '')  # Defaulting to empty string if 'text' is not present

            # Not all steps have 'explanation', so we use `get` method to avoid KeyError
            explanation = step_data.get('explanation', '')  # Defaulting to empty string if 'text' is not present

            # Not all steps have 'description', so we use `get` method to avoid KeyError
            description = step_data.get('description', '')  # Defaulting to empty string if 'text' is not present

            css_selector = step_data.get('css_selector', '')  # Defaulting to empty string if 'css_selector' is not present

            step = TestStep(step_data['action'], css_selector, text, explanation, description)
            self.steps.append(step)

    def __str__(self):
        # Join all steps representations with a newline for better readability
        return "\n".join(str(step) for step in self.steps)

    def to_dict(self):
        return {"steps": [step.to_dict() for step in self.steps]}