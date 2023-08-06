#function only be executed once.
def syszux_once(f):
    def wrapper(*args, **kwargs):
        if not wrapper.has_run:
            wrapper.has_run = True
            return f(*args, **kwargs)
    wrapper.has_run = False
    return wrapper

def qat(f):
    def wrapper(*args, **kwargs):

        f(*args, **kwargs)
        print "new"
    return wrapper
    
if __name__ == "__main__":
    @syszux_once
    def test(x,y):
        print(x**y)

    test(2,3)
    test(3,4)
    