import os
import sys
# Path of frags package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                '..')))
# Path for core.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                '../frags')))
import frags
