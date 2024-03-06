from pydantic import BaseModel, field_validator
from datetime import datetime, timezone
from typing import List, Optional
import re


class GspcInvite(BaseModel):
    email_addresses: str
    certification_expiration_date: datetime
    valid_emails: Optional[List[str]] = []
    invalid_emails: Optional[List[str]] = []

    @field_validator('certification_expiration_date')
    @classmethod
    def check_certification_expiration_date(cls, value):
        value is datetime
        if value < datetime.now(timezone.utc):
            raise ValueError("Certification expiration date cannot be in the past")
        return value

    def parse(self):
        if not self.email_addresses:
            return

        emails = self.email_addresses.split(',')

        # Instantiate list
        self.valid_emails = []
        self.invalid_emails = []

        # Regex for validating an Email
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

        # Sort
        for email in emails:
            # Remove whitespace
            email = email.strip()
            if email == "":
                continue
            if (re.fullmatch(regex, email)):
                self.valid_emails.append(email)
            else:
                self.invalid_emails.append(email)
