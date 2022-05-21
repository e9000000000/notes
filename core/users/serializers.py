from rest_framework.serializers import ModelSerializer, Serializer, CharField
from rest_framework.exceptions import ValidationError
from rest_captcha.serializers import RestCaptchaSerializer

from .models import CustomUser as User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "registration_date"]
        read_only_fields = ["id", "registration_date"]

    def create(self, validated_data):
        raise NotImplementedError()("use RegistrationSerializer for user creation")


class RegistrationSerializer(ModelSerializer, RestCaptchaSerializer):
    class Meta:
        model = User
        fields = ["captcha_key", "captcha_value", "username", "password"]
        extra_kwargs = {
            "password": {"write_only": True},
            "username": {"write_only": True},
        }

    def update(self, instance: User, validated_data):
        raise NotImplementedError("only for user creation")

    def create(self, validated_data):
        instance = super().create(validated_data)
        instance.set_password(validated_data["password"])
        instance.save()
        return instance


class ChangeUserPasswordSerializer(Serializer):
    model = User

    fields_params = {
        "required": True,
        "write_only": True,
    }
    old_password = CharField(**fields_params, help_text="old password")
    new_password = CharField(**fields_params, help_text="new password")

    def validate(self, data):
        if self.instance and not self.instance.check_password(data["old_password"]):
            raise ValidationError("wrong old password")
        return data

    def create(*args, **kwargs):
        raise NotImplementedError("serializer can be used for changing password only")

    def update(self, instance: User, validated_data):
        new = validated_data["new_password"]
        instance.set_password(new)
        instance.save()
        return instance
