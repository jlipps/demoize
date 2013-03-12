import sys
import time
import os.path
from demoize import Demo, DemoServer

if __name__ == "__main__":
    if sys.argv[1] == "server":
        filepath = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                   "test/sample_code.py"))
        d = DemoServer()
        d.start_server(filepath, title="My Code", heading="My Code!",
                       striplines_regex=r'#!!')
    elif sys.argv[1] == "demo":
        d = Demo()
        while True:
            d.next_line()
            time.sleep(1)
        d.stop_demo()
