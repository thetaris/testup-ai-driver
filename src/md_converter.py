from bs4 import BeautifulSoup
from markdownify import markdownify as md
import re
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def convert_to_md(html_doc):
    html_doc = re.sub('<script[^>]*>[^<]*</script>', '', html_doc)

    html_doc = re.sub('<link .*?/>', '', html_doc)

    html_doc = re.sub('<img[^>]*>', '', html_doc)

    html_doc = re.sub('<!--.*?-->', '', html_doc)

    html_doc = re.sub('data-link-behaviour="[^"]*"', '', html_doc, flags=re.DOTALL)

    html_doc = re.sub('data-modalopenparam="[^"]*"', '', html_doc, flags=re.DOTALL)

    html_doc = re.sub('data-loadedonopen="[^"]*"', '', html_doc, flags=re.DOTALL)

    html_doc = re.sub('data-tabber-content="[^"]*"', '', html_doc, flags=re.DOTALL)

    html_doc = re.sub('style="[^"]*"', '', html_doc, flags=re.DOTALL)

    html_doc = re.sub('role="[^"]*"', '', html_doc, flags=re.DOTALL)

    html_doc = re.sub('height="[^"]*"', '', html_doc, flags=re.DOTALL)

    html_doc = re.sub('color="[^"]*"', '', html_doc, flags=re.DOTALL)

    html_doc = re.sub('width="[^"]*"', '', html_doc, flags=re.DOTALL)

    html_doc = re.sub('x="[^"]*"', '', html_doc, flags=re.DOTALL)

    html_doc = re.sub('y="[^"]*"', '', html_doc, flags=re.DOTALL)

    html_doc = re.sub('href="[^"]*"', '', html_doc, flags=re.DOTALL)

    html_doc = re.sub(r'<source[^>]*>', '', html_doc, flags=re.DOTALL)
    html_doc = re.sub(r'<svg.*?>.*?</svg>', '', html_doc, flags=re.DOTALL)

    logging.info(f"html_doc: {html_doc}")

    logging.info('------------------------------------------------')
    logging.info('------------------------------------------------')
    logging.info('------------------------------------------------')
    logging.info('------------------------------------------------')
    logging.info('------------------------------------------------')

    soup = BeautifulSoup(html_doc, 'html.parser')

    for tag in soup.find_all(['li', 'button', 'input', 'textarea', 'a'], id=True):
        # Initialize an empty list to hold the desired attributes
        desired_attributes = []

        for attr, value in tag.attrs.items():
            if attr != 'class':
                desired_attributes.append(f'{attr}="{value}"')

        # Join the desired attributes into a single string
        attributes_str = ' '.join(desired_attributes)

        # Replace tag with a modified version that includes only the desired attributes
        tag.replace_with(f'<{tag.name}.postfix {attributes_str}>{tag.get_text()}</{tag.name}>')

    # Convert the modified HTML to Markdown
    markdown = md(str(soup), strip=['span'])

    # Remove '.postfix' from tag names in the Markdown content
    markdown = re.sub(r'(\w+)\.postfix', r'\1', markdown)

    markdown = re.sub('\s+', ' ', markdown)

    return markdown
