import re
from web.server import run_app
from selenium import webdriver
from pygments import highlight
from pygments.lexers import get_lexer_by_name, get_lexer_for_filename
from pygments.formatters import HtmlFormatter
from selenium.common.exceptions import NoSuchElementException


class DemoServer(object):

    def start_server(self, code_file, language=None, port=5000,
                     striplines_regex=None, **params):
        #!! this line shouldn't appear
        lexer_opts = {
            'stripall': True
        }
        x = 1  #!! neither should this line
        if language:
            lexer = get_lexer_by_name(language, **lexer_opts)
        else:
            lexer = get_lexer_for_filename(code_file, **lexer_opts)
        formatter = HtmlFormatter(linenos=True, linespans="line",
                                  anchorlinenos="aline")
        code = ''
        with open(code_file, 'r') as f:
            code = f.read()
        if striplines_regex is not None:
            codelines = code.split("\n")
            keeplines = []
            for l in codelines:
                if re.search(striplines_regex, l) is None:
                    keeplines.append(l)
            code = "\n".join(keeplines)
        result = highlight(code, lexer, formatter)
        params['code'] = result
        run_app(port=port, **params)


class Demo(object):

    def __init__(self, port=5000):
        print "Starting demo"
        self.url = "http://localhost:%s" % port
        self.driver = webdriver.Chrome()
        self.driver.get(self.url)
        self.cur_line = 0

    def goto_line(self, line=1):
        self.driver.find_element_by_id("line-%s" % line)
        self.highlight_line(line)

    def highlight_line(self, line):
        print "Highlighting line %s" % line
        script = """(function() {
                        $(".hll").removeClass("hll");
                        $("#line-%s").addClass("hll");
                        $("a[href='#-%s']").addClass("hll");
                    })()""" % (line, line)
        script = script.replace(" ", "")
        script = script.replace("\n", "")
        self.driver.execute_script(script)
        self.cur_line = line

    def next_line(self, skip=1):
        try:
            self.goto_line(self.cur_line + skip)
        except NoSuchElementException:
            self.goto_line(1)

    def stop_demo(self):
        self.driver.quit()


if __name__ == "__main__":
    run_app()
