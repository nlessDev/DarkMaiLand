from sqlalchemy import create_engine, Column, String, LargeBinary, DateTime, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
import uuid

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    username = Column(String(64), primary_key=True)
    password_hash = Column(String(128))
    public_key = Column(LargeBinary)
    emails = relationship("Email", back_populates="user")

class Email(Base):
    __tablename__ = 'emails'
    message_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    thread_id = Column(UUID(as_uuid=True), index=True)
    references = Column(ARRAY(UUID(as_uuid=True)))
    sender = Column(String(256))
    recipients = Column(ARRAY(String(256)))
    subject = Column(String(256))
    content = Column(Text)
    timestamp = Column(DateTime)
    user_id = Column(String(64), ForeignKey('users.username'))
    user = relationship("User", back_populates="emails")
    attachments = relationship("Attachment", back_populates="email")
    receipts = relationship("DeliveryReceipt", back_populates="email")

class Attachment(Base):
    __tablename__ = 'attachments'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    filename = Column(String(256))
    content_type = Column(String(128))
    content = Column(LargeBinary)
    email_id = Column(UUID(as_uuid=True), ForeignKey('emails.message_id'))
    email = relationship("Email", back_populates="attachments")

class DeliveryReceipt(Base):
    __tablename__ = 'receipts'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email_id = Column(UUID(as_uuid=True), ForeignKey('emails.message_id'))
    status = Column(String(32))
    timestamp = Column(DateTime)
    email = relationship("Email", back_populates="receipts")

def init_db(connection_string='sqlite:///smtpx.db'):
    engine = create_engine(connection_string)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)
