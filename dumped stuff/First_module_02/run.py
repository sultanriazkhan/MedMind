#!/usr/bin/env python3
"""
Simple launcher for MedMind system
Ensures clean startup with no conflicts
"""
import sys
import subprocess

if __name__ == "__main__":
    print("Starting MedMind Lab Processing System...")
    print("Running: python main.py")
    subprocess.run([sys.executable, "main.py"])