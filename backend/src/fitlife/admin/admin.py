from sqladmin import Admin, ModelView

from fitlife.coaches.models import CoachModel
from fitlife.members.models import MemberModel
from fitlife.training_sessions.models import SessionParticipant, TrainingSession


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
        CoachModel.specialization,
        CoachModel.experience,
        CoachModel.created_at,
    ]

    column_searchable_list = [
        CoachModel.email,
        CoachModel.first_name,
        CoachModel.last_name,
        CoachModel.specialization,
    ]

    column_sortable_list = [
        CoachModel.email,
        CoachModel.first_name,
        CoachModel.last_name,
        CoachModel.specialization,
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
        TrainingSession.max_participants,
        TrainingSession.coach_id,
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

    form_excluded_columns = [TrainingSession.participants, TrainingSession.coach]

    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True


class SessionParticipantAdmin(ModelView, model=SessionParticipant):
    name = 'Session Participant'
    name_plural = 'Session Participants'
    icon = 'fa-solid fa-user-check'

    column_list = [
        SessionParticipant.member_id,
        SessionParticipant.session_id,
        SessionParticipant.joined_at,
    ]

    form_excluded_columns = [SessionParticipant.member, SessionParticipant.session]

    can_create = True
    can_edit = False
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

    admin.add_view(MemberAdmin)
    admin.add_view(CoachAdmin)
    admin.add_view(TrainingSessionAdmin)
    admin.add_view(SessionParticipantAdmin)

    return admin
