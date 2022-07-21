# config var
DEBUG = False


# end config var


# tool functions

def update_config(**kwargs):
    global DEBUG
    for k, v in kwargs.items():
        if k == "DEBUG":
            DEBUG = v
        else:
            pass


def debug_info(msg):
    if DEBUG:
        print("[Info]", msg)


# end tool functions


# error class
class Error(Exception):
    def __init__(self, msg):
        self.message = msg

    def message(self):
        return self.message

# error class
