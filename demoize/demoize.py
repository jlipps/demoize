import os

from web.server import run_app
from selenium import webdriver
from pygments import highlight
from pygments.lexers import get_lexer_by_name, get_lexer_for_filename
from pygments.formatters import HtmlFormatter


class Demo(object):

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.child_pid = None

    def start_server(self, code_file, language=None, port=5000, **params):
        self.child_pid = os.fork()
        if self.child_pid == 0:
            lexer_opts = {
                'stripall': True
            }
            if language:
                lexer = get_lexer_by_name(language, **lexer_opts)
            else:
                lexer = get_lexer_for_filename(code_file, **lexer_opts)
            formatter = HtmlFormatter(linenos=True)
            code = ''
            with open(code_file, 'r') as f:
                code = f.read()
            result = highlight(code, lexer, formatter)
            params['code'] = result
            run_app(port=port, **params)


if __name__ == "__main__":
    run_app()
