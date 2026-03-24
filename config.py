import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from loguru import logger

load_dotenv()

if getattr(sys, 'frozen', False):
    ROOT_DIR = Path(sys.executable).absolute()
else:
    ROOT_DIR = Path(__file__).parent.absolute()

FILES_DIR = os.path.join(ROOT_DIR, 'files')
DB_NAME = os.path.join(FILES_DIR, 'db.sql')

DELETE_OLD_APOINTMENT = False

logger.add(
    f'{os.path.join(FILES_DIR, "debug.log")}',
    format='{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}',
    level='DEBUG'
)
