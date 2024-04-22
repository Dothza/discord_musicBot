import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase


class Song(SqlAlchemyBase):
    __tablename__ = 'songs'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    link = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    playlist_name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    playlist_link = sqlalchemy.Column(sqlalchemy.String, nullable=True)
