from sqlalchemy import Column, String, Numeric, Text, TIMESTAMP, JSON, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
import enum
from app.db.database import Base

class Group(Base):
    __tablename__ = 'groups'

    group_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    group_name = Column(String, nullable=False)

class TransactionType(enum.Enum):
    group = "group"
    individual = "individual"

class SettlementStatus(enum.Enum):
    pending = "pending"
    settled = "settled"

class TransactionDetails(Base):
    __tablename__ = 'transaction_details'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    transaction_type = Column(Enum(TransactionType), nullable=False)
    group_id = Column(UUID(as_uuid=True))
    user_id = Column(UUID(as_uuid=True))
    net_amount = Column(Numeric(10, 2), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp(), nullable=False)
    amount_due_on = Column(JSON, nullable=True)
    amount_owed_to = Column(JSON, nullable=True)
    due_balance = Column(Numeric(10, 2), default=0.00, nullable=True)
    owed_balance = Column(Numeric(10, 2), default=0.00, nullable=True)
    settlement_status = Column(String(20), default='pending', nullable=True)
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp(), nullable=False)

class User(Base):
    __tablename__ = 'users'

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, default='CURRENT_TIMESTAMP')

    def __repr__(self):
        return f"<User(user_id={self.user_id}, name='{self.name}', created_at={self.created_at})>"