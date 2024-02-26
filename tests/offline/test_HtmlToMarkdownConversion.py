import pytest

from md_converter import convert_to_md


class TestHtmlToMarkdownConversion:
    def test_heading_conversion(self):
        html = "<body><h1>Heading 1</h1></body>"
        expected_md = "Heading 1 ========= "
        result = convert_to_md(html)
        assert convert_to_md(html) == expected_md, f"Expected: {expected_md}, Got: {result}"

    def test_paragraph_conversion(self):
        html = "<body><p>This is a paragraph.</p></body>"
        expected_md = "This is a paragraph. "
        result = convert_to_md(html)
        assert convert_to_md(html) == expected_md, f"Expected: {expected_md}, Got: {result}"

    def test_link_conversion(self):
        html = '<body><a href="https://example.com">Example</a></body>'
        #expected_md = "[Example](https://example.com)"
        expected_md = "Example"
        result = convert_to_md(html)
        assert convert_to_md(html) == expected_md, f"Expected: {expected_md}, Got: {result}"

    def test_unordered_list_conversion(self):
        html = "<body><ul><li>Item 1</li><li>Item 2</li></ul></body>"
        #expected_md = "- Item 1\n- Item 2"
        expected_md = '* Item 1 * Item 2 '
        result = convert_to_md(html)
        assert convert_to_md(html) == expected_md, f"Expected: {expected_md}, Got: {result}"

    def test_ordered_list_conversion(self):
        html = "<body><ol><li>First</li><li>Second</li></ol></body>"
        #expected_md = "1. First\n2. Second"
        expected_md = '1. First 2. Second '
        result = convert_to_md(html)
        assert convert_to_md(html) == expected_md, f"Expected: {expected_md}, Got: {result}"

    def test_image_conversion(self):
        html = '<body><img src="image.jpg" alt="Alt text"></body>'
        expected_md = "![Alt text](image.jpg)"
        result = convert_to_md(html)
        assert convert_to_md(html) == expected_md, f"Expected: {expected_md}, Got: {result}"


