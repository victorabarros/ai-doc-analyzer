import ebooklib
import os
import pdfplumber
import re
import xml.etree.ElementTree as ET

from bs4 import BeautifulSoup
from ebooklib import epub


def _parse_content_from_pdf(file_path):
    with pdfplumber.open(file_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text.strip()


def _parse_content_from_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    text = []
    for elem in root.iter():
        if elem.text:
            text.append(elem.text.strip())
    return " ".join(text)


def _parse_content_from_epub(file_path):
    book = epub.read_epub(file_path)
    text = []
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            # Decode content and clean HTML/XML
            soup = BeautifulSoup(item.get_content(), "html.parser")
            text.append(soup.get_text())
    return "\n".join(text)


def _clean_up_content(content):
    text = content.replace(' \n', '').replace('\n\n\n', '\n').replace('\n\n', '\n').replace('\n\n', '\n').strip()
    text = re.sub(r"(?<=\n)\d{1,2}", "", text)
    text = re.sub(r"\b(?:the|this)\s*slide\s*\w+\b", "", text, flags=re.IGNORECASE)
    return text


def parse_content(file_path):
    """
    Parses the content of a file to plain text.
    Valid file formats are pdf, xml, and epub.

    Args:
        file_path (str): The path to the file to be parsed.

    Returns:
        str: The parsed content of the file.

    Raises:
        ValueError: If the file format is not supported.

    """
    if file_path.endswith('.pdf'):
        content = _parse_content_from_pdf(file_path)
    elif file_path.endswith('.xml'):
        content = _parse_content_from_xml(file_path)
    elif file_path.endswith('.epub'):
        content = _parse_content_from_epub(file_path)
    else:
        raise ValueError("Unsupported file format")

    return _clean_up_content(content)


def save_in_disk(destination_directory, file_name, content, extension='txt'):
    """
    Save the content to a file in the specified destination directory.

    Args:
        destination_directory (str): The directory where the file will be saved.
        file_name (str): The name of the original file.
        content (str): The content to be saved.

    Returns:
        str: The path of the saved file.

    """
    save_path = os.path.join(destination_directory, f"{file_name}.{extension}")
    with open(save_path, 'w', encoding='utf-8') as file:
        file.write(content)

    return save_path
