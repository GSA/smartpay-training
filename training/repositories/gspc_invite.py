from itertools import islice
import logging
from typing import Iterator, List
import uuid
from sqlalchemy import desc, nullslast
from sqlalchemy.orm import Session
from training import models
from datetime import datetime, date, timedelta
from .base import BaseRepository
import time


class GspcInviteRepository(BaseRepository[models.GspcInvite]):

    def __init__(self, session: Session):
        super().__init__(session, models.GspcInvite)

    def create(self, email: str, certification_expiration_date: date) -> models.GspcInvite:
        return self.save(models.GspcInvite(
            email=email,
            certification_expiration_date=certification_expiration_date,
            gspc_invite_id=uuid.uuid4()
        ))

    def bulk_create(self, emails: list[str], certification_expiration_date: date) -> list[models.GspcInvite]:
        """Bulk insert GspcInvite records for multiple emails."""
        logging.info(f"Starting gspc bulk create, number of invites:{len(emails)}")
        invites = [
            models.GspcInvite(
                email=email,
                certification_expiration_date=certification_expiration_date,
                gspc_invite_id=uuid.uuid4()
            )
            for email in emails
        ]

        try:
            # Insert 50 at a time
            for batch in GspcInviteRepository.batch_iterator(invites, 50):
                self.bulk_save(batch)
                time.sleep(1)

            return invites

        except Exception as e:
            raise Exception(f"Batch insert failed: {str(e)}") from e

    def batch_iterator(items: List, batch_size: int) -> Iterator:
        """Create an iterator that yields batches of the specified size."""
        iterator = iter(items)
        batch = list(islice(iterator, batch_size))
        while batch:
            yield batch
            batch = list(islice(iterator, batch_size))

    def get_by_gspc_invite_id(self, gspc_invite_id: uuid.UUID) -> models.GspcInvite:
        """
        retrieves a GspcInvite by its gspc_invite_id
        param gspc_invite_id: (uuid.UUID): The UUID tied to each invite
        returns:models.GspcInvite: The matching invite record
        """
        result = self._session.query(models.GspcInvite).filter(
            models.GspcInvite.gspc_invite_id == gspc_invite_id
        ).first()

        if result is None:
            raise ValueError("No invite found with the given gspc_invite_id")
        return result

    def get_invites_for_second_follow_up(self) -> list[models.GspcInvite]:
        """
        Retrieves and updates GspcInvite records eligible for a second follow-up,
        and updates the second_invite_date

        Criteria:
        - No second invite sent yet (second_invite_date is None)
        - Created within the last 6 months
        - Created more than 12 hours ago
        - Not yet completed (completed_date is None)

        returns: List of updated GspcInvite records
        """

        current_time = datetime.now()
        six_months_ago = current_time - timedelta(days=180)
        twelve_hours_ago = current_time - timedelta(hours=12)

        eligible_invites = self._session.query(models.GspcInvite).filter(
            models.GspcInvite.second_invite_date.is_(None),
            models.GspcInvite.created_date >= six_months_ago,
            models.GspcInvite.created_date < twelve_hours_ago,
            models.GspcInvite.completed_date.is_(None)
        ).all()

        # Update second_invite_date for each eligible invite
        for invite in eligible_invites:
            invite.second_invite_date = current_time

        # Commit the changes
        self._session.commit()

        return eligible_invites

    def get_invites_for_final_follow_up(self) -> list[models.GspcInvite]:
        """
        Retrieves and updates GspcInvite records eligible for a second follow-up,
        and updates the second_invite_date

        Criteria:
        - No final invite sent yet (second_invite_date is None)
        - Second email within the last 6 months
        - Second email more than 12 hours ago
        - Not yet completed (completed_date is None)

        returns: List of updated GspcInvite records
        """

        current_time = datetime.now()
        six_months_ago = current_time - timedelta(days=180)
        twelve_hours_ago = current_time - timedelta(hours=12)

        eligible_invites = self._session.query(models.GspcInvite).filter(
            models.GspcInvite.final_invite_date.is_(None),
            models.GspcInvite.created_date >= six_months_ago,
            models.GspcInvite.second_invite_date < twelve_hours_ago,
            models.GspcInvite.completed_date.is_(None)
        ).all()

        # Update second_invite_date for each eligible invite
        for invite in eligible_invites:
            invite.final_invite_date = current_time

        # Commit the changes
        self._session.commit()

        return eligible_invites

    def set_completion_date(self, id: int) -> None:
        """
        Sets completed_date to now
        :param id: gspc_invite ID to update
        :return: None
        """
        gspc_invite = self.find_by_id(id)
        if gspc_invite is None:
            raise ValueError("invalid gspc invite id")
        gspc_invite.completed_date = datetime.now()
        self._session.commit()

    def get_gspc_completion_report(self):
        result = (
            self._session.query(
                models.GspcInvite.email.label("invitedEmail"),
                models.GspcInvite.gspc_invite_id.label("gspcInviteId"),
                models.GspcInvite.created_date.label("inviteDate"),
                models.GspcInvite.second_invite_date.label("secondInviteDate"),
                models.GspcInvite.final_invite_date.label("finalInviteDate"),
                models.User.email.label("registeredEmail"),
                models.User.name.label("username"),
                models.Agency.name.label("agency"),
                models.Agency.bureau.label("bureau"),
                models.GspcCompletion.passed.label("passed"),
                models.GspcInvite.completed_date.label("completedDate")
            )
            .select_from(models.GspcInvite)
            .outerjoin(models.GspcCompletion, models.GspcCompletion.gspc_invite_id == models.GspcInvite.gspc_invite_id)
            .outerjoin(models.User, models.User.id == models.GspcCompletion.user_id)
            .outerjoin(models.Agency, models.Agency.id == models.User.agency_id)
            .order_by(
                nullslast(models.GspcCompletion.passed.desc()),
                desc(models.GspcCompletion.submit_ts),
                desc(models.GspcInvite.created_date)
            )
        ).all()

        return result
