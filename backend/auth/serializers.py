from rest_framework.serializers import ModelSerializer
from rest_framework.authtoken.models import Token
from .models import User

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email", "password", "first_name", "last_name", "phone_number", "birth", "is_senior")

    def save(self, **kwargs):
        new_user = User.objects.create_user(
            username = self.validated_data.get('username'),
            email = self.validated_data.get('email'),
            first_name = self.validated_data.get('first_name'),
            last_name = self.validated_data.get('last_name'),
            phone_number = self.validated_data.get('phone_number'),
            birth = self.validated_data.get('birth'),
            is_senior = self.validated_data.get('is_senior')
        )
        new_user.set_password(self.validated_data.get('password'))
        new_user.save()
        new_token = Token.objects.create(user=new_user)