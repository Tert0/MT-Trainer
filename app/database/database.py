from typing import TypeVar

from sqlalchemy import create_engine

from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session, Session, Query
from config import SQL_SERVER_LOCATION, SQL_DATABASE, SQL_USERNAME, SQL_PASSWORD, SQL_ECHO_OUTPUT, SQLITE_DATABASE
T = TypeVar("T")


class DB:
    """
    Database connection
    Attributes
    ----------
    engine: :class:`sqlalchemy.engine.Engine`
    Base: :class:`sqlalchemy.ext.declarative.DeclarativeMeta`
    """

    def __init__(self, location: str, database: str, username: str, password: str, echo: bool = False):
        """
        :param location: location of the sql server
        :param database: name of the database
        :param username: name of the sql user
        :param password: password of the sql user
        :param echo: whether sql queries should be logged
        """

        if not SQLITE_DATABASE:
            protocol, location = location.split("://")
            self.engine: Engine = create_engine(
                f"{protocol}://{username}:{password}@{location}/{database}",
                pool_pre_ping=True,
                pool_recycle=300,
                pool_size=10,
                max_overflow=20,
                echo=echo,
            )
        else:
            self.engine: Engine = create_engine(
                f"sqlite://{location}",
                echo=echo,
            )

        self._SessionFactory: sessionmaker = sessionmaker(bind=self.engine)
        self._Session = scoped_session(self._SessionFactory)
        self.Base: DeclarativeMeta = declarative_base()

    def add(self, obj: T) -> T:
        """
        Add a new row to the database
        :param obj: the row to insert
        :return: the same row
        """

        self.session.add(obj)
        return obj

    def delete(self, obj: T) -> T:
        """
        Remove a row from the database
        :param obj: the row to remove
        :return: the same row
        """

        self.session.delete(obj)
        return obj

    def query(self, *entities, **kwargs) -> Query:
        """Shortcut for :meth:`sqlalchemy.orm.session.Session.query`"""

        return self.session.query(*entities, **kwargs)

    def commit(self):
        """Shortcut for :meth:`sqlalchemy.orm.session.Session.commit`"""

        self.session.commit()

    def close(self):
        """Close the current session"""

        self._Session.remove()

    @property
    def session(self) -> Session:
        """Get the session object for the current thread"""

        return self._Session()


def get_database() -> DB:
    """
    Create a database connection object using the environment variables
    :return: The DB object
    """

    return DB(
        location=SQL_SERVER_LOCATION,
        database=SQL_DATABASE,
        username=SQL_USERNAME,
        password=SQL_PASSWORD,
        echo=SQL_ECHO_OUTPUT,
    )
