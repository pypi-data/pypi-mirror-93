from appchance.redlink.models import (
    DeviceNotificationSettings,
    RedlinkDevice,
)
from django.contrib import admin


class DeviceNotificationSettingsInline(admin.StackedInline):
    model = DeviceNotificationSettings


class RedlinkDeviceAdminAbstract:
    list_display = (
        "id",
        "registration_id",
        "user",
        "name",
        "type",
        "created",
        "updated",
    )
    readonly_fields = ("user",)
    search_fields = ("id", "registration_id", "user__id")
    list_filter = ("settings__marketing", "settings__transactional")
    inlines = (DeviceNotificationSettingsInline,)


@admin.register(RedlinkDevice)
class RedlinkDeviceAdmin(RedlinkDeviceAdminAbstract, admin.ModelAdmin):
    pass
