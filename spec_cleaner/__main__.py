import os
import sys

path = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, path)

from spec_cleaner import main

if __name__ == '__main__':
    sys.exit(main())
