import pytest

from md_converter import convert_to_md


class TestInteractiveElementsConversion:
    @pytest.fixture
    def setup(self):
        # This setup could be used to initialize or mock data for tests.
        pass

    def test_link_with_id_conversion(self, setup):
        html = '<body><a href="https://example.com" id="testupautoid1234">Example</a></body>'
        #expected_md = '[Example](https://example.com) <!-- id: testupautoid1234 -->'
        expected_md = """<a id="testupautoid1234">Example</a>"""
        result = convert_to_md(html)
        assert result == expected_md, f"Expected: {expected_md}, Got: {result}"

    def test_button_with_id_conversion(self, setup):
        html = '<body><button id="testupautoid1234">Click me</button></body>'
        expected_md = """<button id="testupautoid1234">Click me</button>"""
        result = convert_to_md(html)
        assert result == expected_md, f"Expected: {expected_md}, Got: {result}"

    def test_input_with_id_conversion(self, setup):
        html = '<body><input type="text" id="testupautoid1234"></body>'
        #expected_md = 'Input: <!-- id: testupautoid1234 -->'
        expected_md = """<input type="text" id="testupautoid1234"></input>"""
        result = convert_to_md(html)
        assert result == expected_md, f"Expected: {expected_md}, Got: {result}"

    def test_input_with_id_and_placeholder_conversion(self, setup):
        html = '<body><input type="text" id="testupautoid1234" placeholder="Enter your text here"></body>'
        #expected_md = 'Input: <!-- id: testupautoid1234, placeholder: Enter your text here -->'
        expected_md = """<input type="text" id="testupautoid1234" placeholder="Enter your text here"></input>"""
        result = convert_to_md(html)
        assert result == expected_md, f"Expected: {expected_md}, Got: {result}"

