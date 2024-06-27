from django.contrib.auth.mixins import UserPassesTestMixin

from kavenegar import *

try:
    import json
except ImportError:
    import simplejson as json


def send_otp_code(phone_number, otp_code):
    try:
        api = KavenegarAPI('API Key')
        params = {
            'sender': '',
            'receptor': phone_number,
            'message': f'your verification code: \n{otp_code} ',
            'type': 'sms',
        }
        response = api.sms_send(params=params)
        print(response)
    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)


class IsAdminUserMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_admin


class NotAuthenticatedUserMixin(UserPassesTestMixin):
    def test_func(self):
        return not self.request.user.is_authenticated


class IsSellerUserMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_seller
