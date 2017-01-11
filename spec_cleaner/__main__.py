from __future__ import absolute_import

import os
import sys

# If we are running from a wheel, add the wheel to sys.path.
if __package__ == '':
    # __file__ is spec-cleaner-*.whl/spec_cleaner/__main__.py.
    # First dirname call strips of '/__main__.py', second strips off '/spec_cleaner'.
    # Resulting path is the name of the wheel itself.
    # Add that to sys.path so we can import spec_cleaner.
    path = os.path.dirname(os.path.dirname(__file__))
    sys.path.insert(0, path)

import spec_cleaner

if __name__ == '__main__':
    sys.exit(spec_cleaner.main())
