from appchance.redlink.models import (
    DeviceNotificationSettings,
    RedlinkDevice,
)
from rest_framework.serializers import ModelSerializer


class DeviceNotificationSettingsSerializer(ModelSerializer):
    class Meta:
        model = DeviceNotificationSettings
        exclude = ("device",)
        extra_kwargs = {"id": {"read_only": True}}


class RedlinkDeviceSerializer(ModelSerializer):
    settings = DeviceNotificationSettingsSerializer(read_only=True)

    class Meta:
        model = RedlinkDevice
        fields = "__all__"
        extra_kwargs = {"id": {"read_only": True, "required": False}}

    def validate(self, attrs):
        self.Meta.model.objects.filter()
        return attrs
