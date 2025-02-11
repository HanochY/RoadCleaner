import logging.config
import uvicorn
import json
import logging
from config.provider import ConfigProvider
from utils.enums.environments import Environment

def run_server():
    main_settings = ConfigProvider.main_app_settings()
    uvicorn.run(
        "api.main.app:app",
        host=main_settings.ADDRESS,
        port=main_settings.PORT,
        reload=(main_settings.ENVIRONMENT == Environment.DEVELOPMENT),
        workers=main_settings.THREAD_COUNT,
    )
    

if __name__ == "__main__":
    run_server()