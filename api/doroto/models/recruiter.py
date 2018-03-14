from flask import url_for, current_app
from ..exceptions import ValidationError
from ..utils import split_url
from . import Base
from .. import db

class Recruiter(Base):
    __tablename__ = "recruiters"
    name = db.Column(db.String(256))
    address = db.Column(db.Text)
    description = db.Column(db.Text)
    phone = db.Column(db.String(256))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
    user = db.relationship('User', lazy=True)

    def get_url(self):
        return url_for('api.get_recruiter', id=self.id, _external=True)

    def export_data(self):
        return {
            'self_url': self.get_url(),
            'name': self.name,
            'id': self.id,
            'address':self.address,
            'description':self.description,
            'phone':self.phone
        }

    def import_data(self, data):
        try:
            self.name = data['name']
        except KeyError as e:
            raise ValidationError('Invalid recruiter: missing ' + e.args[0])
        return self