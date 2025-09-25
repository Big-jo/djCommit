# This is a medium-sized change that should trigger "good" classification
# It has more than 10 lines but no new functions

# Update existing configuration
CONFIG = {
    'database_url': 'postgresql://localhost:5432/myapp',
    'redis_url': 'redis://localhost:6379',
    'api_key': 'your-api-key-here',
    'debug_mode': True,
    'log_level': 'INFO',
    'max_connections': 100,
    'timeout': 30,
    'retry_attempts': 3,
    'cache_ttl': 3600,
    'rate_limit': 1000
}

# Update environment variables
import os
os.environ['DATABASE_URL'] = CONFIG['database_url']
os.environ['REDIS_URL'] = CONFIG['redis_url']
os.environ['API_KEY'] = CONFIG['api_key']
os.environ['DEBUG'] = str(CONFIG['debug_mode'])
os.environ['LOG_LEVEL'] = CONFIG['log_level']
