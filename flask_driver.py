"""
    Copyright (c) 2020 Anamitra Ghorui
    This file is part of tknewsedit

    tknewsedit is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    
    tknewsedit is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    
    You should have received a copy of the GNU General Public License
    along with tknewsedit.  If not, see <https://www.gnu.org/licenses/>.
"""

# Example Driver for Flask-SQLAlchemy.
# You may have to run this in a flask virtual environment first.

from .tknewsedit import *

class Flask_SQLAlchemyFeedDatabase(FeedDatabase):
    """
This driver assumes the given elements are present in the input model:
    1. ID
    2. title
    3. date
    4. content

The generic record class isn't used for this driver and mixing the two isn't
recommended.
    """
    database_name = "Flask_SQLAlchemy"
    database_driver_version = "1.0"

    def __init__(self, dbsession, dbmodel):
        self.db = dbsession
        self.model = dbmodel

    def delete_by_id(self, _id):
        post = self.model.query.filter_by(id = _id)
        post.delete()

    def get_by_id(self, _id):
        return self.model.query.get(_id)
    
    def fetch_all(self):
        return self.model.query.order_by(self.model.id).all()

    def commit(self):
        self.db.session.commit()

    def rollback(self):
        self.db.session.rollback()

    def add(self, record):
        self.db.session.add(record)

    def delete(self, record):
        self.db.session.delete(record)

    def close(self):
        pass
