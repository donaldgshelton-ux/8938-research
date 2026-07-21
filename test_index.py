import unittest
import os
from html.parser import HTMLParser

class IndexHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.has_title = False
        self.meta_charset = False
        self.meta_viewport = False
        self.in_title = False
        self.title_text = ""

    def handle_starttag(self, tag, attrs):
        if tag == "title":
            self.has_title = True
            self.in_title = True
        elif tag == "meta":
            attrs_dict = dict(attrs)
            if attrs_dict.get("charset") == "UTF-8":
                self.meta_charset = True
            if attrs_dict.get("name") == "viewport" and attrs_dict.get("content") == "width=device-width, initial-scale=1.0":
                self.meta_viewport = True

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title_text += data

class TestIndexHtml(unittest.TestCase):
    def test_html_structure(self):
        """Test that the index.html file has basic structural elements."""
        self.assertTrue(os.path.exists('index.html'), "index.html does not exist")

        with open('index.html', 'r', encoding='utf-8') as f:
            content = f.read()

        parser = IndexHTMLParser()
        parser.feed(content)

        self.assertTrue(parser.has_title, "Missing <title> tag")
        self.assertTrue(parser.meta_charset, "Missing <meta charset=\"UTF-8\">")
        self.assertTrue(parser.meta_viewport, "Missing standard viewport meta tag")

        # Checking title matches what was given in the description
        self.assertIn("Form 8938 Delinquent Filing", parser.title_text)

if __name__ == '__main__':
    unittest.main()
