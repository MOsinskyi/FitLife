from typing import Any

from sqladmin import Admin, ModelView
from sqlalchemy.orm import selectinload
from starlette.requests import Request

from fitlife.admin.models import AdminModel
from fitlife.coaches.models import CoachModel
from fitlife.gallery.models import GalleryModel
from fitlife.members.models import MemberModel
from fitlife.training_sessions.models import SessionParticipant, TrainingSession


class AdminAdmin(ModelView, model=AdminModel):
    name = 'Admin'
    name_plural = 'Admins'
    icon = 'fa-solid fa-user-shield'

    column_list = [
        AdminModel.id,
        AdminModel.email,
        AdminModel.first_name,
        AdminModel.last_name,
        AdminModel.phone_number,
        AdminModel.role,
        AdminModel.created_at,
    ]

    column_searchable_list = [
        AdminModel.email,
        AdminModel.first_name,
        AdminModel.last_name,
        AdminModel.phone_number,
    ]

    column_sortable_list = [
        AdminModel.email,
        AdminModel.first_name,
        AdminModel.last_name,
        AdminModel.created_at,
    ]

    column_details_exclude_list = [AdminModel.password]
    form_excluded_columns = [AdminModel.password]

    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True


class MemberAdmin(ModelView, model=MemberModel):
    name = 'Member'
    name_plural = 'Members'
    icon = 'fa-solid fa-users'

    column_list = [
        MemberModel.id,
        MemberModel.email,
        MemberModel.first_name,
        MemberModel.last_name,
        MemberModel.phone_number,
        MemberModel.role,
        MemberModel.created_at,
    ]

    column_searchable_list = [
        MemberModel.email,
        MemberModel.first_name,
        MemberModel.last_name,
        MemberModel.phone_number,
    ]

    column_sortable_list = [
        MemberModel.email,
        MemberModel.first_name,
        MemberModel.last_name,
        MemberModel.created_at,
    ]

    column_details_exclude_list = [MemberModel.password]
    form_excluded_columns = [MemberModel.password, MemberModel.participations]

    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True


class CoachAdmin(ModelView, model=CoachModel):
    name = 'Coach'
    name_plural = 'Coaches'
    icon = 'fa-solid fa-chalkboard-user'

    column_list = [
        CoachModel.id,
        CoachModel.email,
        CoachModel.first_name,
        CoachModel.last_name,
        CoachModel.specializations,
        CoachModel.experience,
        CoachModel.created_at,
    ]

    column_searchable_list = [
        CoachModel.email,
        CoachModel.first_name,
        CoachModel.last_name,
    ]

    column_sortable_list = [
        CoachModel.email,
        CoachModel.first_name,
        CoachModel.last_name,
        CoachModel.experience,
        CoachModel.created_at,
    ]

    column_details_exclude_list = [CoachModel.password]
    form_excluded_columns = [CoachModel.password, CoachModel.sessions]

    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True


class TrainingSessionAdmin(ModelView, model=TrainingSession):
    name = 'Training Session'
    name_plural = 'Training Sessions'
    icon = 'fa-solid fa-dumbbell'

    column_list = [
        TrainingSession.id,
        TrainingSession.title,
        TrainingSession.start_time,
        TrainingSession.end_time,
        TrainingSession.status,
        TrainingSession.coach,
        TrainingSession.created_at,
    ]

    column_searchable_list = [TrainingSession.title]

    column_sortable_list = [
        TrainingSession.title,
        TrainingSession.start_time,
        TrainingSession.end_time,
        TrainingSession.status,
        TrainingSession.created_at,
    ]

    # Eager load coach and participants with their members
    column_select_related_list = ['coach']

    # Override how we fetch data to include eager loading of participants and their members
    async def get_query(self, request, stmt):
        stmt = stmt.options(
            selectinload(TrainingSession.coach),
            selectinload(TrainingSession.participants).selectinload(SessionParticipant.member),
        )
        return await super().get_query(request, stmt)

    async def get_model_objects(self, stmt):
        """Override to ensure eager loading when fetching model objects for forms"""
        stmt = stmt.options(
            selectinload(TrainingSession.coach),
            selectinload(TrainingSession.participants).selectinload(SessionParticipant.member),
        )
        return await super().get_model_objects(stmt)

    # Include coach and participants in the form
    form_columns = [
        'title',
        'description',
        'start_time',
        'end_time',
        'status',
        'max_participants',
        'coach',
        'participants',
    ]

    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True


class SessionParticipantAdmin(ModelView, model=SessionParticipant):
    name = 'Session Participant'
    name_plural = 'Session Participants'
    icon = 'fa-solid fa-user-check'

    column_list = [
        SessionParticipant.member,
        SessionParticipant.session,
        SessionParticipant.joined_at,
    ]

    column_select_related_list = ['member', 'session']

    column_labels = {
        SessionParticipant.member: 'Member',
        SessionParticipant.session: 'Training Session',
    }

    async def get_object_for_details(self, request: Request) -> Any:
        await super().get_object_for_details(request)

    form_columns = [
        'member',
        'session',
    ]

    can_create = True
    can_edit = False
    can_delete = True
    can_view_details = True


class GalleryAdmin(ModelView, model=GalleryModel):
    name = 'Gallery'
    name_plural = 'Gallery'
    icon = 'fa-solid fa-image'

    column_list = [
        GalleryModel.id,
        GalleryModel.image_url,
        GalleryModel.title,
        GalleryModel.display_order,
        GalleryModel.created_at,
    ]

    column_searchable_list = [
        GalleryModel.title,
        GalleryModel.description,
    ]

    column_sortable_list = [
        GalleryModel.display_order,
        GalleryModel.created_at,
    ]

    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True


def setup_admin(app, engine, authentication_backend):
    admin = Admin(
        app,
        engine,
        title='FitLife Admin',
        base_url='/admin',
        authentication_backend=authentication_backend,
    )

    admin.add_view(AdminAdmin)
    admin.add_view(MemberAdmin)
    admin.add_view(CoachAdmin)
    admin.add_view(TrainingSessionAdmin)
    admin.add_view(SessionParticipantAdmin)
    admin.add_view(GalleryAdmin)

    return admin
