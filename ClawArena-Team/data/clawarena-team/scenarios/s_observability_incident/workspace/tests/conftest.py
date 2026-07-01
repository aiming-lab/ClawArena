"""pytest conftest for checkout pool pressure tests."""
import pytest


@pytest.fixture
def pool_size():
    """Return the current configured pool size (mirrors REDIS_POOL_SIZE env)."""
    return 5  # reflects the v3.2.1 misconfiguration
