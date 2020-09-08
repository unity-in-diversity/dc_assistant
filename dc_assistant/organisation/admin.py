from django.contrib import admin
from .models import Region, Location, Rack, Device, DeviceRole, Vendor, VendorModel, Platform
from extend.models import TaggedItem, Tag
from dc_assistant.admin import admin_site


admin_site.register(Region)
admin_site.register(Location)
admin_site.register(Rack)
admin_site.register(Device)
admin_site.register(DeviceRole)
admin_site.register(Vendor)
admin_site.register(VendorModel)
admin_site.register(Platform)
admin_site.register(Tag)
admin_site.register(TaggedItem)
