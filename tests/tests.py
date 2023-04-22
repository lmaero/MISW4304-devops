import unittest
from unittest.mock import patch
from unittest.mock import Mock, MagicMock
from src.endpoints.blacklist import blackmail_info_get, post_add_email_to_blacklist


class TestGet(unittest.TestCase):

    def test_blackmail_info_get_no_db(self):
        email = 'alonsodaniel10@hotmail.com'
        db = ''
        request = ''
        info = blackmail_info_get(email, db, request)
        response_expected = ({'msg': "'str' object has no attribute 'headers'"} , 500)
        self.assertEqual(info, response_expected)


    def test_blackmail_info_get_no_bearer(self):
        email = 'alonsodaniel10@hotmail.com'
        db = ''
        request = MagicMock()
        request.headers.get.return_value = ""
        info = blackmail_info_get(email, db, request)
        response_expected = ({"msg": "Authorization header is not in the headers or bearer value is wrong"}, 400)
        self.assertEqual(info, response_expected)

    def test_blackmail_info_get_bearear_less_than_2(self):
        email = 'alonsodaniel10@hotmail.com'
        db = ''
        request = MagicMock()
        request.headers.get.return_value = "bearer"
        info = blackmail_info_get(email, db, request)
        response_expected = ({"msg": "Token is not in the headers"}, 400)
        self.assertEqual(info, response_expected)

    def test_blackmail_info_no_email(self):
        email = ''
        db = ''
        request = MagicMock()
        request.headers.get.return_value = "bearer 1234"
        info = blackmail_info_get(email, db, request)
        response_expected = ({"msg": "The email is missing, please provide a valid email"}, 400)
        self.assertEqual(info, response_expected)

    def test_blackmail_info_no_email_in_db(self):
        email = '1234@email.com'
        db = ''
        request = MagicMock()
        request.headers.get.return_value = "bearer 1234"
        db = MagicMock()
        db.session.query.return_value = {'email': '1234@email.com'}
        info = blackmail_info_get(email, db, request)
        response_expected = ({"is_in_blacklist": 0, "cause": ""}, 200)
        self.assertEqual(info, response_expected)


    def test_post_add_email_to_blacklist(self):
        db = ''
        request = ''
        info = post_add_email_to_blacklist(db, request)
        response_expected = (({'msg': "'str' object has no attribute 'get_json'"}, 500))
        self.assertEqual(info, response_expected)

    def test_post_add_email_to_blacklist_bearer_less_than_2(self):
        request = MagicMock()
        request.get_json.return_value = ''
        request.headers.get.return_value = ''
        db = MagicMock()
        db.session.query.return_value = {'email': '1234@email.com'}
        info = post_add_email_to_blacklist(db, request)
        response_expected = ({"msg": "Authorization header is not in the headers or bearer value is wrong"}, 400)
        self.assertEqual(info, response_expected)

    def test_post_add_email_to_blacklist_incorrect_token(self):
        request = MagicMock()
        request.get_json.return_value = ''
        request.headers.get.return_value = 'bearer'
        db = MagicMock()
        db.session.query.return_value = {'email': '1234@email.com'}
        info = post_add_email_to_blacklist(db, request)
        response_expected = ({"msg": "Token is not in the headers"}, 400)
        self.assertEqual(info, response_expected)
    @patch('src.endpoints.blacklist.STATIC_TOKEN', '12345')
    def test_post_add_email_to_blacklist_empty_email(self):
        request = MagicMock()
        request.get_json.return_value = {'email': ''}
        request.headers.get.return_value = 'bearer 12345'
        db = MagicMock()
        db.session.query.return_value = {'email': '1234@email.com'}
        info = post_add_email_to_blacklist(db, request)
        response_expected = ({"msg": "The email is missing, please provide a valid email"}, 400)
        self.assertEqual(info, response_expected)

    @patch('src.endpoints.blacklist.STATIC_TOKEN', '12345')
    def test_post_add_email_to_blacklist_empty_blocked(self):
        request = MagicMock()
        request.get_json.return_value = {'email': '123@123.com'}
        request.headers.get.return_value = 'bearer 12345'
        db = MagicMock()
        db.session.query.filter_by.first.return_value = {'email': '1234@email.com'}
        info = post_add_email_to_blacklist(db, request)
        response_expected = ({"msg": "This email was already blacklisted"}, 400)
        self.assertEqual(info, response_expected)

    @patch('src.endpoints.blacklist.STATIC_TOKEN', '12345')
    def test_post_add_email_to_blacklist_app_uuid_not_valid(self):
        request = MagicMock()
        request.get_json.return_value = {'email': '123@123.com', 'app_uuid': ''}
        request.headers.get.return_value = 'bearer 12345'
        db = MagicMock()
        email = ''
        Blacklisted = ''
        db.session.query(Blacklisted).filter_by(email=email).first.return_value = False
        info = post_add_email_to_blacklist(db, request)
        response_expected = ({"msg": "The app_uuid is missing, please provide a valid app id"}, 400)
        self.assertEqual(info, response_expected)

    @patch('src.endpoints.blacklist.STATIC_TOKEN', '12345')
    def test_post_add_email_to_blacklist_blocked_reason_not_valid(self):
        request = MagicMock()
        request.remote_addr.return_value = '12345'
        request.get_json.return_value = {'email': '123@123.com', 'app_uuid': '12345', 'blocked_reason':
            """12345123451234512345123451234512345123451234512345123451234512345123451234512345123451234512345123451234512345123451234512345123451234512345123451234512345123451234512345123451234
            5123451234512345123451234512345123451234512345
            123451234512345123451234512345123451234512345
            123451234512345123451234512345123451234512345"""
                                         }
        request.headers.get.return_value = 'bearer 12345'
        db = MagicMock()
        email = ''
        Blacklisted = ''
        db.session.query(Blacklisted).filter_by(email=email).first.return_value = False
        info = post_add_email_to_blacklist(db, request)
        response_expected = ({"msg": "The block reason has to be less than 255 characters"}, 400)
        self.assertEqual(info, response_expected)