from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from .models import Account

class AccountBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            account = Account.objects.get(email=email)
            if account.check_password(password):
                try:
                    user = User.objects.get(username=account.username)
                except User.DoesNotExist:
                    user = User.objects.create_user(
                        username=account.username, email=account.email, password=password
                    )
                return user
        except Account.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
