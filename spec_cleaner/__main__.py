import os
import sys

from spec_cleaner import main

path = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, path)


if __name__ == '__main__':
    sys.exit(main())
