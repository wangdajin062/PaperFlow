import sys
from pathlib import Path

# Ensure the backend root is on sys.path for imports
BACKEND_ROOT = Path(__file__).parent.parent
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))
