import pytest
import re
from md_converter import convert_to_md
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def test_convert_md_includes_all_aria_labels_empty_a_with_aria():
    logging.info("Starting test: test_convert_md_includes_all_aria_labels_empty_a_with_aria")

    # Locate and read the HTML file
    file_path = Path(__file__).parent.parent / 'data' / 'offline' / 'empty_links_with_aria.html'
    logging.debug(f"Reading HTML file from: {file_path}")
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    logging.info("Extracting aria-labels from the HTML input")
    # Extract all aria-labels from the HTML input
    aria_labels_in_input = set(re.findall(r'aria-label="([^"]+)"', html_content))
    logging.debug(f"Extracted aria-labels: {aria_labels_in_input}")

    # Convert HTML to Markdown
    logging.info("Converting HTML to Markdown")
    md_output = convert_to_md(html_content)

    # Verify each aria-label is referenced in the Markdown output
    for aria_label in aria_labels_in_input:
        assert aria_label in md_output, logging.error(f"aria-label '{aria_label}' was not found in the Markdown output")
        logging.info(f"Verified aria-label '{aria_label}' is present in the Markdown output")

    logging.info("Test completed successfully")


def test_convert_md_includes_all_ids_empty_a_with_aria():
    logging.info("Starting test: test_convert_md_includes_all_ids_empty_a_with_aria")

    # Locate and read the HTML file
    file_path = Path(__file__).parent.parent / 'data' / 'offline' / 'li_a_aria_extended.html'
    logging.debug(f"Reading HTML file from: {file_path}")
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Perform the conversion and log the action
    logging.debug("Converting HTML to Markdown")
    md_output = convert_to_md(html_content)

    # Extract and log the IDs found
    ids_in_input = set(re.findall(r'id="(autoidtestup\d+)"', html_content))
    logging.debug(f"IDs found in input: {ids_in_input}")

    # Verify each ID is referenced in the Markdown output
    for id_ in ids_in_input:
        assert id_ in md_output, f"ID {id_} was not found in the Markdown output"
        logging.info(f"Verified ID present in Markdown output: {id_}")

    logging.info("Test completed successfully: test_convert_md_includes_all_ids_empty_a_with_aria")
