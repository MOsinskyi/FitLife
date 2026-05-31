from datetime import datetime, UTC
import asyncio
from celery import Celery
from celery.schedules import crontab
from sqlalchemy import select, and_, or_
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from fitlife.config import settings
from fitlife.campaigns.models import EmailCampaign, CampaignFrequency
from fitlife.members.models import MemberModel
from fitlife.campaigns.services import EmailService

# Ensure all models are imported for SQLAlchemy mapper initialization
from fitlife.coaches.models import CoachModel # noqa
from fitlife.admin.models import AdminModel # noqa
from fitlife.gallery.models import GalleryModel # noqa
from fitlife.passes.models import PassModel, PassFeatureModel # noqa
from fitlife.specializations.models import SpecializationModel # noqa
from fitlife.training_sessions.models import TrainingSession, SessionParticipant # noqa

celery_app = Celery(
    "fitlife",
    broker=f"redis://{settings.redis.effective_host}:{settings.redis.port}/{settings.redis.db.cache}",
    backend=f"redis://{settings.redis.effective_host}:{settings.redis.port}/{settings.redis.db.cache}"
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

engine = create_async_engine(settings.postgres.url)
async_session = async_sessionmaker(engine, expire_on_commit=False)

def run_async(coro):
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(coro)

@celery_app.task
def send_single_email(email: str, subject: str, body: str):
    return EmailService.send_email(email, subject, body)

@celery_app.task
def dispatch_campaign(campaign_id: str):
    async def _dispatch():
        async with async_session() as session:
            campaign = await session.get(EmailCampaign, campaign_id)
            if not campaign:
                return

            result = await session.execute(select(MemberModel.email))
            emails = result.scalars().all()
            
            for email in emails:
                if email:
                    send_single_email.delay(email, campaign.subject, campaign.body)
            
            campaign.last_sent_at = datetime.now(UTC)
            await session.commit()

    run_async(_dispatch())

@celery_app.task
def trigger_scheduled_campaigns():
    async def _trigger():
        now = datetime.now(UTC)
        current_time = now.time()
        current_day_week = now.weekday() + 1 # 1-7
        current_day_month = now.day
        
        async with async_session() as session:
            stmt = select(EmailCampaign).where(
                and_(
                    EmailCampaign.is_active == True,
                    or_(
                        EmailCampaign.last_sent_at == None,
                        EmailCampaign.last_sent_at < now.replace(hour=0, minute=0, second=0, microsecond=0)
                    )
                )
            )
            result = await session.execute(stmt)
            campaigns = result.scalars().all()
            
            for campaign in campaigns:
                if current_time >= campaign.send_time:
                    should_send = False
                    
                    if campaign.frequency == CampaignFrequency.DAILY:
                        should_send = True
                    elif campaign.frequency == CampaignFrequency.WEEKLY:
                        if campaign.send_day == current_day_week:
                            should_send = True
                    elif campaign.frequency == CampaignFrequency.MONTHLY:
                        if campaign.send_day == current_day_month:
                            should_send = True
                    elif campaign.frequency == CampaignFrequency.ONCE:
                        should_send = True
                        campaign.is_active = False # Disable after one-time send
                    
                    if should_send:
                        dispatch_campaign.delay(str(campaign.id))

    run_async(_trigger())

celery_app.conf.beat_schedule = {
    "check-campaigns-every-minute": {
        "task": "fitlife.worker.trigger_scheduled_campaigns",
        "schedule": crontab(minute="*"),
    },
}
