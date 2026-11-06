import os
import sys

# the package import below needs the repository root on sys.path,
# so insert it before importing
path = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, path)

from spec_cleaner import main

if __name__ == '__main__':
    sys.exit(main())
