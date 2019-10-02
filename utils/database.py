from contextlib import contextmanager

from sqlalchemy import Column, Integer, BLOB, create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE = 'sqlite:///images.db'

engine = create_engine(DATABASE)
engine.echo = True
Base = declarative_base(metadata=MetaData(bind=engine))
Session = sessionmaker(bind=engine)


class Image(Base):
    __tablename__ = 'image'
    id = Column(Integer, primary_key=True)
    data = Column(BLOB)


Base.metadata.create_all(engine)


@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


def save_to_db(image_path):
    with open(image_path, 'rb') as file:
        image = file.read()

    with session_scope() as session:
        images = Image(data=image)
        session.add(images)
