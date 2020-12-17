# -*- coding: utf-8 -*-
from datetime import datetime

from demo.extensions import db


class Vote(db.Model):
    __tablename__ = 'votes'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

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