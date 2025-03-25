import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

LOG_FORMAT: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_DIR = Path(__file__).parent.parent / "logs"


def setup_loggers():
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    # Endpoints FastAPI logger
    endpoints_logger = logging.getLogger('endpoints')
    endpoints_logger.setLevel(logging.INFO)
    endpoints_handler = RotatingFileHandler(
        filename=str(LOG_DIR / 'endpoints.log'),
        maxBytes=1024*1024*5,
        backupCount=5
    )
    endpoints_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    endpoints_logger.addHandler(endpoints_handler)

    # RabbitMQ logger
    rabbitmq_logger = logging.getLogger('rabbitmq')
    rabbitmq_logger.setLevel(logging.INFO)
    rabbitmq_handler = RotatingFileHandler(
        filename=str(LOG_DIR / 'rabbitmq.log'),
        maxBytes=1024*1024*5,
        backupCount=5
    )
    rabbitmq_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    rabbitmq_logger.addHandler(rabbitmq_handler)

    # Background tasks logger
    background_tasks_logger = logging.getLogger('backround_tasks')
    background_tasks_logger.setLevel(logging.INFO)
    background_tasks_handler = RotatingFileHandler(
        filename=str(LOG_DIR / 'background_tasks.log'),
        maxBytes=1024*1024*5,
        backupCount=5
    )
    background_tasks_handler.setFormatter(
        logging.Formatter(LOG_FORMAT)
    )
    background_tasks_logger.addHandler(background_tasks_handler)
