import pytest
from appchance.redlink.models import (
    DeviceNotificationSettings,
    RedlinkDevice,
)
from appchance.redlink.serializers import RedlinkDeviceSerializer
from appchance.redlink.tests.factories import RedlinkDeviceFactory


@pytest.mark.django_db
class TestRedlinkDeviceSerializer:
    def test_serialize(self):
        device: RedlinkDevice = RedlinkDeviceFactory()
        DeviceNotificationSettings.objects.create(device=device)
        serializer = RedlinkDeviceSerializer(device)
        assert serializer.data == {
            "id": str(device.id),
            "registration_id": device.registration_id,
            "user": device.user_id,
            "name": device.name,
            "active": device.active,
            "type": device.type,
            "created": device.created.strftime("%Y-%m-%d %H:%M:%S"),
            "updated": device.created.strftime("%Y-%m-%d %H:%M:%S"),
            "settings": {
                "id": device.settings.id,
                "marketing": device.settings.marketing,
                "transactional": device.settings.transactional,
            },
        }
