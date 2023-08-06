# Parse markdown table into tuple of lists
# Armaan Bhojwani 2021

import sys
from bs4 import BeautifulSoup
import markdown

from .deck import Card


def md2html(file):
    """Use the markdown module to convert input to HTML"""
    try:
        return markdown.markdown(open(file, "r").read(), extensions=['tables'])
    except FileNotFoundError:
        print(f"lightcards: \"{file}\": No such file or directory")
        exit(1)


def parse_html(html):
    """Use BeautifulSoup to parse the HTML"""
    def clean_text(inp):
        return inp.get_text().rstrip()

    soup = BeautifulSoup(html, 'html.parser')
    outp = []

    for x in soup.find_all("tr"):
        outp.append(Card([clean_text(y) for y in x.find_all("td")[:2]]))

    # Return a tuple of nested lists
    return ([clean_text(x) for x in soup.find_all("th")][:2], outp[1:])


def main(file):
    return parse_html(md2html(file))


if __name__ == "__main__":
    print(main(sys.argv[1]))
