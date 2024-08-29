from database.db_instance import db
from flask_security import Security, SQLAlchemyUserDatastore
from server.server import app
import sys
from flask_security.utils import hash_password


def create_db():
    # Important: The model should be imported before create_all() is called
    with app.app_context():
        # from auth.models import BotAuth, Department, Role, User, RevokedTokenModel, IPModel
        # from bot_page.models import Car, TodoModel, WebUserModel
        # from chatbot.models import Message, Chat, Lead, Group
        # Setup Flask-Security
        # user_datastore = SQLAlchemyUserDatastore(db, User, Role)
        # security = Security(app, user_datastore)
        # from bot_page.models import BotConfiguration
        from auth.models import BotBackendResponse

        db.create_all()

        # user_datastore.create_user(email=email, password=hash_password(password))
        db.session.commit()


if __name__ == '__main__':

    # if len(sys.argv) != 3:
    #     print("Please only call me with 2 parameters: <email> <password>")
    #     sys.exit()
    #
    # email = sys.argv[1]
    # password =sys.argv[2]

    create_db()