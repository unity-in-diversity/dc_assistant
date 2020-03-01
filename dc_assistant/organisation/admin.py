from django.contrib import admin
from .models import Region, Location, Rack, Device, DeviceRole, Vendor, VendorModel, Platform
from extend.models import TaggedItem, Tag

admin.site.register(Region)
admin.site.register(Location)
admin.site.register(Rack)
admin.site.register(Device)
admin.site.register(DeviceRole)
admin.site.register(Vendor)
admin.site.register(VendorModel)
admin.site.register(Platform)

admin.site.register(Tag)
admin.site.register(TaggedItem)
