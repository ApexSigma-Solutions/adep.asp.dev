from unittest.mock import patch

@patch.dict('os.environ', {
    'DATABASE_URL': 'test_db_url',
    'REDIS_URL': 'test_redis_url',
    'QDRANT_URL': 'test_qdrant_url',
    'NEO4J_URL': 'test_neo4j_url'
})
def test_settings():
    from apexsigma_core.utils.config import Settings
    settings = Settings()
    assert settings.database_url == 'test_db_url'
    assert settings.redis_url == 'test_redis_url'
    assert settings.qdrant_url == 'test_qdrant_url'
    assert settings.neo4j_url == 'test_neo4j_url'

def test_get_logger():
    from apexsigma_core.utils.logging import get_logger
    logger = get_logger('test_logger')
    assert logger.name == 'test_logger'
    assert logger.level == 20 # INFO