#!/usr/bin/env python3
"""
Railway Entry Point for Agency System
Handles PORT environment variable correctly
"""
import os
import sys

# Change to api directory
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "api"))
sys.path.insert(0, os.getcwd())

import uvicorn

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"Starting Agency System on port {port}")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        workers=1,
        log_level="info",
        access_log=True
    )
