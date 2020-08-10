try:
    from IPython.core.getipython import get_ipython
except:
    def get_ipython():
        return False

if get_ipython():
    from quantum.magic import quantum
