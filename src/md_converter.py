from bs4 import BeautifulSoup, Comment
from markdownify import markdownify as md
import re
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def clean_markdown(markdown):
    # Remove base64 encoded images
    cleaned_markdown = re.sub(r'!\[[^\]]*\]\(data:image\/[a-zA-Z]+;base64,[^\)]+\)', '', markdown)

    # Remove CSS styles - targeting patterns that start with a period or within style tags
    cleaned_markdown = re.sub(r'<style>[\s\S]*?<\/style>', '', cleaned_markdown)

    # Remove excessive whitespace
    cleaned_markdown = re.sub(r'\n\s*\n', '\n\n', cleaned_markdown)

    return cleaned_markdown


def convert_to_md(html_doc):

    soup = BeautifulSoup(html_doc, 'html.parser')

    for element in soup(['script', 'style', 'iframe', 'noscript']):
        element.decompose()

    # Remove all comments, which includes CDATA
    for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
        comment.extract()

    for tag in soup.find_all():
        for attr in ['href', 'src', 'xlink:href']:
            if attr in tag.attrs and 'base64,' in tag[attr].lower():
                del tag[attr]

        if 'style' in tag.attrs:
            del tag['style']

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

        if 'id' in tag.attrs:
            desired_attributes.append(f'id="{tag["id"]}"')

        include_attrs = {'aria-label',
                         'type',
                         'aria-current',
                         'aria-hidden',
                         'value',
                         'name',
                         'data-value',
                         'placeholder',
                         'role',
                         'title'
                         }

        for attr, value in tag.attrs.items():
            if attr in include_attrs:
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

    return clean_markdown(markdown)


