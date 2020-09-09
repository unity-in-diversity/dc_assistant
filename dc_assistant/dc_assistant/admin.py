from django.conf import settings
from django.contrib.admin import AdminSite
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.auth.models import Group, User


class DCAdminSite(AdminSite):

    site_header = 'DC Assistant Administration'
    site_title = 'DC Assistant'
    site_url = '/{}'.format(settings.BASE_PATH)
#    index_template = 'django_rq/index.html'

admin_site = DCAdminSite(name='admin')

admin_site.register(Group, GroupAdmin)
admin_site.register(User, UserAdmin)