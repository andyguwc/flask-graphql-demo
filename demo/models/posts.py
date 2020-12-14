# -*- coding: utf-8 -*-
from datetime import datetime

from demo.extensions import db


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def to_dict(self):
        return {
            'id': self.id,
            'body': self.body,
        }

    def from_dict(self, data, author=None, new_post=False):
        for field in ['body']:
            if field in data:
                setattr(self, field, data[field])
        if new_post and author:
            self.author = author