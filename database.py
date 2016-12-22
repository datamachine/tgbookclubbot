from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Column,
    String,
    Text,
    Integer,
    DateTime,
    ForeignKey,
)

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    relationship,
    )


class Database(object):
    def __init__(self):
        self.db = create_engine('sqlite:///data.db', echo=True)
        Base.metadata.create_all(self.db, checkfirst=True)
        self.session = scoped_session(sessionmaker(expire_on_commit=False, bind=self.db))

# Models
Base = declarative_base()


class Chat(Base):
    __tablename__ = 'chat'

    id = Column(Integer, primary_key=True)
    type = Column(String)
    title = Column(String)
    username = Column(String)


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    username = Column(String)


class Book(Base):
    __tablename__ = 'book'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    isbn = Column(String)
    goodreads_id = Column(Integer)

    author_id = Column(Integer, ForeignKey('author.id'))
    author = relationship('Author', backref='books')


class Author(Base):
    __tablename__ = 'author'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    goodreads_id = Column(Integer)


class BookReview(Base):
    __tablename__ = 'book_review'

    id = Column(Integer, primary_key=True)
    review_date = Column(DateTime)
    rating = Column(Integer)
    review_text = Column(Text)

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', backref='reviews')
    book_id = Column(Integer, ForeignKey('book.id'))
    book = relationship('Book', backref='reviews')


class BookAssignment(Base):
    __tablename__ = 'book_assignment'

    id = Column(Integer, primary_key=True)
    schedule_type = Column(String)
    start_date = Column(DateTime)

    book_id = Column(Integer, ForeignKey('book.id'))
    book = relationship('Book', backref='assignments')
    chat_id = Column(Integer, ForeignKey('chat.id'))
    chat = relationship('Chat', backref='assignments')


class BookSchedule(Base):
    __tablename__ = 'book_schedule'

    id = Column(Integer, primary_key=True)
    due_date = Column(DateTime)
    start = Column(Integer)
    end = Column(Integer)

    book_assignment_id = Column(Integer, ForeignKey('book_assignment.id'))
    book_assignment = relationship('BookAssignment', backref='schedules')


class UserParticipation(Base):
    __tablename__ = 'user_participation'

    id = Column(Integer, primary_key=True)

    join_date = Column(DateTime)
    edition = Column(String)

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', backref='participation')
    book_assignment_id = Column(Integer, ForeignKey('book_assignment.id'))
    book_assignment = relationship('BookAssignment', backref='participation')


class ProgressUpdate(Base):
    __tablename__ = 'progress_update'

    id = Column(Integer, primary_key=True)

    update_date = Column(DateTime)
    progress = Column(Integer)  # TODO: Progress in pages? Maybe track as percent? Edition is available.

    participation_id = Column(Integer, ForeignKey('user_participation.id'))
    participation = relationship('UserParticipation', backref='updates')
