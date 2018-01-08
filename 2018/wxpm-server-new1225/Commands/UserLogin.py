from ORM import Session
from ORM.Tables.User import User

from sqlalchemy import func


class UserLogin:

    def process(args):

        session = Session()

        name = args['LOGIN_NAME']
        password = User.encrypt_pass(args['LOGIN_PASS'])

        users = session.query(User).filter_by(login_name=name,login_pass=password,deleted=0).all()


        if len(users) == 0:
            return 'FAILED' #not exists or password error

        if len(users) == 1:
            user = users[0]
            if user.status == User.UserStatusPending:
                return 'PENDING'
            if user.status == User.UserStatusFrozen:
                return 'FROZEN'
            if user.status == User.UserStatusBlack:
                return 'BLACK'
            if user.status == User.UserStatusActive:
                return 'SUCCESS'

        #TODO maybe there are replicate user
        return 'SYSTEM_ERROR'
