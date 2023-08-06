import factory
from appchance.redlink.models import (
    DeviceNotificationSettings,
    RedlinkDevice,
)
from factory import Faker


class RedlinkDeviceFactory(factory.DjangoModelFactory):
    name = Faker("pystr", max_chars=10)
    registration_id = Faker("pystr", max_chars=10)
    type = factory.Iterator(["android", "ios"])

    class Meta:
        model = RedlinkDevice


class DeviceNotificationSettingsFactory(factory.DjangoModelFactory):
    marketing = Faker("pybool")
    transactional = Faker("pybool")
    device = factory.SubFactory(RedlinkDeviceFactory)

    class Meta:
        model = DeviceNotificationSettings
