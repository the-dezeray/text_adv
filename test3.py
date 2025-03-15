import sys
import select


def non_blocking_readkey():
    """Check if a key is available without blocking."""
    if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
        return sys.stdin.read(1)
    return None


while True:
    ke = non_blocking_readkey()
    if ke:
        print(ke)
    print("hello")
