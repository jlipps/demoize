import ast
import copy
from astor import codegen
from web.server import run_app
from selenium import webdriver
from pygments import highlight
from pygments.lexers import get_lexer_by_name, get_lexer_for_filename
from pygments.formatters import HtmlFormatter
from selenium.common.exceptions import NoSuchElementException


class DemoServer(object):

    def start_server(self, script_file, language=None, port=5000, **params):
        lexer_opts = {
            'stripall': True
        }
        if language:
            lexer = get_lexer_by_name(language, **lexer_opts)
        else:
            lexer = get_lexer_for_filename(script_file, **lexer_opts)
        formatter = HtmlFormatter(linenos=True, linespans="line",
                                  anchorlinenos="aline")
        code = ''
        with open(script_file, 'r') as f:
            code = f.read()
        result = highlight(code, lexer, formatter)
        params['code'] = result
        run_app(port=port, **params)


class Demo(object):

    def __init__(self, script_file, port=5000, browser="chrome",
                 extra_globals=None):
        if extra_globals is None:
            extra_globals = {}
        self.extra_globals = extra_globals
        self.script_file = script_file
        print "Starting demo"
        self.url = "http://localhost:%s" % port
        if browser == "chrome":
            self.driver = webdriver.Chrome()
        elif browser == "safari":
            self.driver = webdriver.Safari()
        else:
            self.driver = webdriver.Firefox()
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
        self.driver.execute_script("demoize.scrollToCenterOnLine(%s)" % line)
        self.cur_line = line

    def next_line(self, skip=1):
        try:
            self.goto_line(self.cur_line + skip)
        except NoSuchElementException:
            self.goto_line(1)

    def run(self):
        try:
            with open(self.script_file) as f:
                script_lines = [line for line in f]
                script_py = "".join(script_lines)
            tree = ast.parse(script_py, filename=self.script_file)
            new_tree = DemoTransformer().visit(tree)
            print ast.dump(new_tree)
            new_tree = ast.fix_missing_locations(new_tree)
            print codegen.to_source(new_tree)
            code_obj = compile(new_tree, self.script_file, 'exec')
            self.extra_globals.update({'DEMOIZE_OBJ': self})
            exec(code_obj, self.extra_globals)
        except Exception:
            print "Error parsing or running demo code"
            raise
        finally:
            self.driver.quit()


class DemoTransformer(ast.NodeTransformer):

    def generic_visit(self, node, parent_nodes=None):
        if parent_nodes is None:
            parent_nodes = []
        else:
            parent_nodes = copy.copy(parent_nodes)
        avoid_classes = (ast.FunctionDef, ast.ClassDef, ast.If, ast.While,
                         ast.With, ast.TryExcept, ast.TryFinally,
                         ast.ExceptHandler, ast.IfExp, ast.For, ast.Global)
        class_assign = (node.__class__ == ast.Assign and
                        len(parent_nodes) > 0 and
                        parent_nodes[-1].__class__ == ast.ClassDef)
        if (hasattr(node, 'lineno') and
            issubclass(node.__class__, ast.stmt) and
            node.__class__ not in avoid_classes and
            not class_assign):
            extra_stmt = 'DEMOIZE_OBJ.goto_line(line=%s)' % node.lineno
            extra_node = ast.parse(extra_stmt)
            return (extra_node.body[0], node)
        else:
            parent_nodes.append(node)
            for field, old_value in ast.iter_fields(node):
                old_value = getattr(node, field, None)
                if isinstance(old_value, list):
                    new_values = []
                    for value in old_value:
                        if isinstance(value, ast.AST):
                            value = self.generic_visit(value, parent_nodes)
                            if value is None:
                                continue
                            elif not isinstance(value, ast.AST):
                                new_values.extend(value)
                                continue
                        new_values.append(value)
                    old_value[:] = new_values
                elif isinstance(old_value, ast.AST):
                    new_node = self.generic_visit(old_value, parent_nodes)
                    if new_node is None:
                        delattr(node, field)
                    else:
                        setattr(node, field, new_node)
            return node


if __name__ == "__main__":
    run_app()
