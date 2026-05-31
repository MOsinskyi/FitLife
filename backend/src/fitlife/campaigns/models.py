from datetime import datetime, time
from enum import Enum
from typing import Optional

from sqlalchemy import Boolean, Column, Enum as SQLEnum, Integer, String, Text, Time, DateTime
from fitlife.models import Base


class CampaignFrequency(str, Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    ONCE = "once"


class EmailCampaign(Base):
    __tablename__ = "email_campaigns"

    title = Column(String, nullable=False)
    subject = Column(String, nullable=False)
    body = Column(Text, nullable=False)
    
    frequency = Column(SQLEnum(CampaignFrequency), nullable=False, default=CampaignFrequency.ONCE)
    send_time = Column(Time, nullable=False, default=time(hour=9, minute=0))
    send_day = Column(Integer, nullable=True)  # 1-7 for weekly, 1-31 for monthly
    
    is_active = Column(Boolean, nullable=False, default=False)
    last_sent_at = Column(DateTime(timezone=True), nullable=True)

    def __repr__(self) -> str:
        return f"<EmailCampaign(title='{self.title}', frequency='{self.frequency}')>"
