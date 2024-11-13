import psycopg2
from psycopg2.extras import NamedTupleCursor


class DatabaseConnection:
    """Manages a reusable connection to the database."""
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.connection = self._create_connection()

    def _create_connection(self) -> psycopg2.extensions.connection:
        """Creates and returns a connection to the database."""
        return psycopg2.connect(self.database_url)

    def get_cursor(self):
        """Returns a cursor for executing queries."""
        return self.connection.cursor(cursor_factory=NamedTupleCursor)

    def close(self):
        """Closes the database connection."""
        self.connection.close()

    def commit(self):
        """Commits the current transaction."""
        self.connection.commit()

    def rollback(self):
        """Rolls back the current transaction."""
        self.connection.rollback()
