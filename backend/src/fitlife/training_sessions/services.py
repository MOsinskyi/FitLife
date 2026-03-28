from uuid import UUID

from fitlife.coaches.repositories import CoachRepository
from fitlife.members.repositories import MemberRepository
from fitlife.training_sessions.models import SessionParticipant, TrainingSession
from fitlife.training_sessions.repositories import TrainingSessionRepository
from fitlife.training_sessions.schemas import TrainingSessionCreateSchema, TrainingSessionUpdateSchema


class TrainingSessionService:
    def __init__(
        self,
        training_session_repository: TrainingSessionRepository,
        coach_repository: CoachRepository,
        member_repository: MemberRepository,
    ):
        self._training_session_repository = training_session_repository
        self._coach_repository = coach_repository
        self._member_repository = member_repository

    async def create_training_session(self, data: TrainingSessionCreateSchema) -> TrainingSession:
        coach = await self._coach_repository.get_user_by_id(data.coach)
        if not coach:
            raise ValueError(f'Coach with id {data.coach} not found')

        training_session = TrainingSession(
            title=data.title,
            description=data.description,
            start_time=data.start_time,
            end_time=data.end_time,
            status=data.status,
            max_participants=data.max_participants,
            coach_id=data.coach,
        )

        created_session = await self._training_session_repository.create_training_session(training_session)

        if data.participants:
            await self.add_participants_to_session(created_session.id, data.participants)

        return await self._training_session_repository.get_training_session_by_id(created_session.id)

    async def get_training_session(self, session_id: UUID) -> TrainingSession:
        training_session = await self._training_session_repository.get_training_session_by_id(session_id)
        if not training_session:
            raise ValueError(f'Training session with id {session_id} not found')
        return training_session

    async def get_all_training_sessions(self) -> list[TrainingSession]:
        return await self._training_session_repository.get_training_sessions()

    async def update_training_session(self, session_id: UUID, data: TrainingSessionUpdateSchema) -> TrainingSession:
        training_session = await self._training_session_repository.get_training_session_by_id(session_id)
        if not training_session:
            raise ValueError(f'Training session with id {session_id} not found')

        if data.coach:
            coach = await self._coach_repository.get_user_by_id(data.coach)
            if not coach:
                raise ValueError(f'Coach with id {data.coach} not found')

        await self._training_session_repository.update_training_session(session_id, data)

        return await self._training_session_repository.get_training_session_by_id(session_id)

    async def delete_training_session(self, session_id: UUID) -> None:
        training_session = await self._training_session_repository.get_training_session_by_id(session_id)
        if not training_session:
            raise ValueError(f'Training session with id {session_id} not found')

        await self._training_session_repository.delete_training_session(session_id)

    async def add_participants_to_session(self, session_id: UUID, member_ids: list[UUID]) -> TrainingSession:
        training_session = await self._training_session_repository.get_training_session_by_id(session_id)
        if not training_session:
            raise ValueError(f'Training session with id {session_id} not found')

        current_participants = len(training_session.participants)
        if current_participants + len(member_ids) > training_session.max_participants:
            raise ValueError(
                f'Cannot add {len(member_ids)} participants. '
                f'Session has {current_participants}/{training_session.max_participants} participants'
            )

        for member_id in member_ids:
            member = await self._member_repository.get_user_by_id(member_id)
            if not member:
                raise ValueError(f'Member with id {member_id} not found')

            is_already_participant = any(p.member_id == member_id for p in training_session.participants)
            if is_already_participant:
                raise ValueError(f'Member with id {member_id} is already participating in this session')

            participant = SessionParticipant(member_id=member_id, session_id=session_id)
            training_session.participants.append(participant)

        return await self._training_session_repository.get_training_session_by_id(session_id)

    async def remove_participant_from_session(self, session_id: UUID, member_id: UUID) -> TrainingSession:
        training_session = await self._training_session_repository.get_training_session_by_id(session_id)
        if not training_session:
            raise ValueError(f'Training session with id {session_id} not found')

        participant_to_remove = None
        for participant in training_session.participants:
            if participant.member_id == member_id:
                participant_to_remove = participant
                break

        if not participant_to_remove:
            raise ValueError(f'Member with id {member_id} is not participating in this session')

        training_session.participants.remove(participant_to_remove)

        return await self._training_session_repository.get_training_session_by_id(session_id)

    async def get_sessions_by_coach(self, coach_id: UUID) -> list[TrainingSession]:
        coach = await self._coach_repository.get_user_by_id(coach_id)
        if not coach:
            raise ValueError(f'Coach with id {coach_id} not found')

        all_sessions = await self._training_session_repository.get_training_sessions()
        return [session for session in all_sessions if session.coach_id == coach_id]

    async def get_sessions_by_member(self, member_id: UUID) -> list[TrainingSession]:
        member = await self._member_repository.get_user_by_id(member_id)
        if not member:
            raise ValueError(f'Member with id {member_id} not found')

        all_sessions = await self._training_session_repository.get_training_sessions()
        return [
            session
            for session in all_sessions
            if any(participant.member_id == member_id for participant in session.participants)
        ]
