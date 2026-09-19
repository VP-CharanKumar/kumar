#!/usr/bin/env python3
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.database.init_db import init_database
from app.utils.logger import logger

def main():
    logger.info("Initializing SQLite database and seeding knowledge sources...")
    init_database()
    logger.info("Database initialization successful.")

if __name__ == "__main__":
    main()
