# These paths have to be edited to be relative to the package name/folder
# these are present in.

from tknewsedit import *
from flask_driver import *

from app import db
from app.dm import Post

# Example usage of the given driver assuming a flask application in module `app`
# with SQLAlchemy session `db` and datamodel `Post`.

window = FeedEditorWindow(Flask_SQLAlchemyFeedDatabase(db, Post))
