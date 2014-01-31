import sys
import os.path
from demoize import Demo, DemoServer

if __name__ == "__main__":
    filepath = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                "test/sample_code.py"))
    if sys.argv[1] == "server":
        d = DemoServer()
        d.start_server(filepath, title="My Code", heading="My Code!")
    elif sys.argv[1] == "demo":
        d = Demo(filepath)
        d.run()
