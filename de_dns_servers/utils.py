from datetime import datetime
from uuid import uuid4

from de_dns_servers.models import ApiToken


class AuthToken:
    def __init__(self, token):
        self.token = ApiToken.objects.filter(token=token)

    @classmethod
    def create(cls):
        """Generate token from UUI4 first 6 characters"""
        token = ApiToken(token=uuid4().hex[:6])
        token.save()

        return token.token

    def valid(self):
        """Check if token is valid/ not revoked"""
        # token = ApiToken.objects.filter(token=self.token)[0]
        if self.token:
            return self.token[0].is_valid
        else:
            return False

    def revoke(self):
        """Revoke token"""
        # token = ApiToken.objects.filter(token=self.token)[0]
        if self.token:
            self.token[0].is_valid = False
            self.token[0].revoked_at = datetime.utcnow()
            self.token[0].save()
            return True
        else:
            return False

    def __repr__(self) -> str:
        if not self.token:
            return '<Not a valid token>'
        else:
            return f'<Token: {self.token[0].token}, Valid: {self.token[0].is_valid}>'

    def to_dict(self):
        if self.token:
            return {
                'token': self.token[0].token,
                'created_at': self.token[0].created_at.__str__(),
                'is_valid': self.token[0].is_valid,
                'revoked_at': self.token[0].revoked_at.__str__(),
            }
        else:
            return None


class Validator:
    """Check if parameter type is allowed"""

    def __init__(self, target, value):
        self.target = target
        self.value = value

    def allowed_type(self):
        allowed_list = {
            'as_number': int,
            'checked_at': int,
            'name': str,
            'as_org': str,
            'country': str,
            'city': str,
            'version': str,
            'reliability': float,
            'ip_address': str,
        }
        return allowed_list[self.target]

    def check(self):
        try:
            t = self.allowed_type()
            t(self.value)
            return True

        except ValueError:
            return False
