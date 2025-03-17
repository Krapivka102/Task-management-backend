from config.env import env

REDIS_HOST = env.str('REDIS_HOST', 'redis')
REDIS_PORT = 6379
