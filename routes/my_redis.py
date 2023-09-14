import redis
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_redis_client():
    logger.info('Connected to the redis database successfully')
    return redis.Redis(host='localhost', port=6379, db=0)
