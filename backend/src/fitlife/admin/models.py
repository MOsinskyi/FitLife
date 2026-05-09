from sqlalchemy import Column, String
from fitlife.models import UserBase

class AdminModel(UserBase):
    __tablename__ = 'admins'

    def __str__(self):
        return f'Admin: {self.first_name} {self.last_name} ({self.email})'
