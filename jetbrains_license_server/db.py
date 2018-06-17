import os
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from jetbrains_license_server.orm import User

print('db')

sql_url = 'mysql://{user}:{password}@{host}:3306/{dbname}?charset=utf8'.format(
    host=os.environ.get('JLS_MYSQL_HOST'),
    dbname=os.environ.get('JLS_MYSQL_DBNAME'),
    user=os.environ.get('JLS_MYSQL_USER'),
    password=os.environ.get('JLS_MYSQL_PASSWORD')
)
engine = create_engine(sql_url)
Session = scoped_session(sessionmaker(bind=engine))


def GetSession():
    return Session()


@contextmanager
def session_scope():
    session = GetSession()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


def get_port_set():
    ports = set()
    with session_scope() as session:
        for row in session.query(User.port):
            ports.add(row.port)
    return ports


def get_username_by_port(port):
    with session_scope() as session:
        user = session.query(User).filter(User.port == port).one()
        return user.name
