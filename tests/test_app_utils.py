import unittest

from app_utils import escape_html_text


class EscapeHtmlTextTests(unittest.TestCase):
    def test_escapes_markup_and_quotes(self):
        self.assertEqual(
            escape_html_text('<script>alert("x")</script>'),
            '&lt;script&gt;alert(&quot;x&quot;)&lt;/script&gt;',
        )

    def test_converts_non_string_values(self):
        self.assertEqual(escape_html_text(98.9), '98.9')

    def test_escapes_ampersands(self):
        self.assertEqual(escape_html_text('A & B'), 'A &amp; B')


if __name__ == '__main__':
    unittest.main()
