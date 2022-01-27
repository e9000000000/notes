from rest_framework.serializers import ModelSerializer, Serializer, CharField
from rest_framework.exceptions import ValidationError

from .models import CustomUser as User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "info", "is_stuff", "registration_date", "password"]
        read_only_fields = ["id", "is_stuff", "registration_date"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, data):
        if self.instance and "password" in data:
            raise ValidationError("password can't be changed here")
        return data

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
        raise NotImplemented("only for changing password")

    def update(self, instance: User, validated_data):
        new = validated_data["new_password"]
        instance.set_password(new)
        instance.save()
        return instance
