import sys
import os

# Add the root directory to path so that we can import backend.src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.src.app import app
