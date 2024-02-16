import pytest
import re
from md_converter import convert_to_md
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def test_convert_md_includes_does_not_show_hidden_elements():
    logging.info("Starting test: test_convert_md_includes_does_not_show_hidden_elements")

    # Locate and read the HTML file
    file_path = Path(__file__).parent.parent / 'data' / 'offline' / 'search_field.html'
    logging.debug(f"Reading HTML file from: {file_path}")
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Perform the conversion and log the action
    logging.debug("Converting HTML to Markdown")
    md_output = convert_to_md(html_content)

    id_from_hidden_element = "autoidtestup5"
    assert id_from_hidden_element not in md_output, f"ID {id_from_hidden_element} was found in the Markdown output, but since its a hidden element it should not be in the markdown"
    logging.info(f"Verified ID not in Markdown output: {id_from_hidden_element}")

    logging.info("Test completed successfully: test_convert_md_includes_does_not_show_hidden_elements")


def test_convert_to_md_includes_all_ids_search_field():
    logging.info("Starting test: test_convert_to_md_includes_all_ids_search_field")

    # Locate and read the HTML file
    file_path = Path(__file__).parent.parent / 'data' / 'offline' / 'search_field.html'
    logging.debug(f"Reading HTML file from: {file_path}")
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()


    # Convert HTML to Markdown
    logging.info("Converting HTML to Markdown")
    md_output = convert_to_md(html_content)

    # Verify that the following aria-labels are referenced in the Markdown output
    aria_labels_in_input = ["woocommerce-product-search-field-0", "autoidtestup4"]

    for aria_label in aria_labels_in_input:
        assert aria_label in md_output, logging.error(f"aria-label '{aria_label}' was not found in the Markdown output")
        logging.info(f"Verified ID '{aria_label}' is present in the Markdown output")

    logging.info("Test completed successfully")


