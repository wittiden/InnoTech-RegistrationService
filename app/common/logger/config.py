import sys

from loguru import logger

from app.common.config import application_config


def setup_logger() -> None:
    logger.remove()

    if application_config.ENVIRONMENT != 'dev':
        return

    format_template = '{time} | {level} | {message}'

    logger.add(sys.stdout, level='DEBUG', format=format_template)
    logger.add('logs/app.log', level='INFO', rotation='15 mb', retention='10 days', format=format_template)
    logger.add('logs/app.json', level='INFO', serialize=True, rotation='500 mb', retention='30 days', format=format_template)
