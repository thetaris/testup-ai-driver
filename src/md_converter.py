from bs4 import BeautifulSoup, Comment
from markdownify import markdownify as md
import re
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def convert_to_md(html_doc):

    logging.info('------------------------------------------------')
    logging.info('------------------------------------------------')
    logging.info('------------------------------------------------')
    logging.info('------------------------------------------------')
    logging.info('------------------------------------------------')

    soup = BeautifulSoup(html_doc, 'html.parser')

    for script in soup.find_all('script'):
        script.decompose()

    # Remove all comments, which includes CDATA
    for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
        comment.extract()

    for tag in soup.find_all():
        for attr in ['href', 'src', 'xlink:href']:
            if attr in tag.attrs:
                if 'base64,' in tag[attr]:
                    # Option 1: Remove the attribute entirely
                    del tag[attr]

    for li in soup.find_all('li'):
        a = li.find('a')
        if a:
            li.replace_with(a)

    for tag in soup.find_all(['li', 'button', 'input', 'textarea', 'a'], id=True):
        # Exclude hidden elements
        if tag.get('hidden') == 'true':
            continue
        # Initialize an empty list to hold the desired attributes
        desired_attributes = []

        exclude_attrs = {'class', 'style', 'href', 'value', 'target'}

        for attr, value in tag.attrs.items():
            if attr not in exclude_attrs:
                desired_attributes.append(f'{attr}="{value}"')

        # Join the desired attributes into a single string
        attributes_str = ' '.join(desired_attributes)

        # Replace tag with a modified version that includes only the desired attributes
        tag.replace_with(f'<{tag.name}.postfix {attributes_str}>{tag.get_text()}</{tag.name}>')

    # Convert the modified HTML to Markdown
    markdown = md(str(soup), strip=['span'])
    markdown = re.sub(r'(\w+)\.postfix', r'\1', markdown)
    markdown = re.sub('\\s+', ' ', markdown)
    markdown = markdown.replace('\\_', '_')

    logging.info(f"markdown: {markdown}")

    return markdown
