from typing import Any, Callable

from sqlalchemy.orm import Session


class TransactionRepository:
    def __init__(self, db: Session):
        self.db = db

    def run_in_transaction(self, callback: Callable) -> Any:
        """
        Execute a function within a database transaction.

        Args:
            callback: A function that takes the session as parameter and returns a result

        Returns:
            The result of the callback function
        """
        try:
            result = callback(self.db)
            self.db.commit()
            return result
        except Exception as e:
            self.db.rollback()
            raise e
