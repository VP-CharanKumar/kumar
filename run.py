#!/usr/bin/env python3
"""
Darukaa.Earth Launcher
"""
import sys
import uvicorn
from app.utils.logger import logger

def main():
    logger.info("Starting Darukaa.Earth AI Biodiversity Intelligence Server on http://127.0.0.1:8000 ...")
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    main()
