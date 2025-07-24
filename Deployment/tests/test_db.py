from codes.db import create_database_if_missing
from unittest.mock import patch


@patch("psycopg.connect")
def test_create_database_if_missing(mock_connect):
    create_database_if_missing()
    mock_connect.assert_called()
