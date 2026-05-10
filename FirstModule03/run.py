#!/usr/bin/env python3
import subprocess
import sys

if __name__ == "__main__":
    subprocess.run([sys.executable, "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"])