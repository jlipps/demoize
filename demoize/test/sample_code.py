import time


class MySweetClass(object):

    foo = ""

    def do_things(self):
        self.foo = "bar"
        x = 0
        while x < 2:
            time.sleep(1)
            x += 1
        self.bar = "foo"

    def print_things(self):
        try:
            1 / 0
        except Exception:
            print "Didn't find bar"
        time.sleep(1)
        if 1 == 2:
            print "not possible"
        elif 2 == 3:
            print "also not possible"
        else:
            print self.bar
        time.sleep(1)


def run_code():
    obj = MySweetClass()
    obj.do_things()
    obj.print_things()
    for x in [1, 2, 3]:
        print x + 5
    print "MY_CONST is %s" % MY_CONST


run_code()
