import uvicorn
from app.utils.logging import AppLogger

logger = AppLogger().get_logger()

if __name__ == "__main__":
    logger.info('Starting app...')
    uvicorn.run("main:app", host="0.0.0.0", port=8000,
                reload=True, reload_excludes='*.log')
