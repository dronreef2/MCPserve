# Advanced Configuration for MCP Server
# This file contains additional configuration options

# Rate Limiting (requests per minute)
RATE_LIMIT_JINA = 60
RATE_LIMIT_GEMINI = 30
RATE_LIMIT_DEEPL = 30

# Timeouts (seconds)
REQUEST_TIMEOUT_JINA = 30
REQUEST_TIMEOUT_GEMINI = 60
REQUEST_TIMEOUT_DEEPL = 30

# Content Limits
MAX_URL_LENGTH = 2000
MAX_QUERY_LENGTH = 500
MAX_TEXT_LENGTH_TRANSLATE = 10000
MAX_TEXT_LENGTH_DEEPL = 5000
MAX_PROMPT_LENGTH = 5000

# Security Settings
BLOCKED_DOMAINS = [
    'localhost',
    '127.0.0.1',
    '0.0.0.0',
    '10.0.0.0/8',
    '172.16.0.0/12',
    '192.168.0.0/16'
]

BLOCKED_QUERY_TERMS = [
    'password',
    'api_key',
    'token',
    'secret',
    'private_key'
]

# Logging Configuration
LOG_LEVEL = 'INFO'  # DEBUG, INFO, WARNING, ERROR
LOG_MAX_SIZE = 10 * 1024 * 1024  # 10MB
LOG_BACKUP_COUNT = 5

# Cache Settings (if implemented)
CACHE_ENABLED = False
CACHE_TTL = 3600  # 1 hour
CACHE_MAX_SIZE = 1000

# Monitoring
ENABLE_METRICS = False
METRICS_PORT = 9090