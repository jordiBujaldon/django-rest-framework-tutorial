from rest_framework.serializers import ModelSerializer

from users.models import CustomUser


class RegisterSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('user_name', 'email', 'password')
        # Per seguretat
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Return password or None
        password = validated_data.pop('password', None)
        user = self.Meta.model(**validated_data)
        if password is not None:
            user.set_password(password)
        user.save()
        return user
