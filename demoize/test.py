import os.path
from demoize import Demo

if __name__ == "__main__":
    filepath = os.path.abspath("./test/sample_code.py")
    d = Demo()
    d.start_server(filepath, title="My Code", heading="My Code!")
