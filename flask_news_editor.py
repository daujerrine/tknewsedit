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

from tknewsedit import *
from app     import db
from app.dm  import Post

# Example Driver for Flask-SQLAlchemy.
# You may bave to run this in a flask virtual environment first

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
        self.db = db
        self.model = dbmodel
    
    def fetch_all(self):
        return self.model.query.all()

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

if __name__ == '__main__':
    window = FeedEditorWindow(Flask_SQLAlchemyFeedDatabase(db, Post))
