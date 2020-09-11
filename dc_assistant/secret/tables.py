import django_tables2 as tables
from django_tables2.utils import Accessor
from .models import Secret


class SecretTable(tables.Table):
    device = tables.LinkColumn()

    class Meta:
        model = Secret
        fields = ('name', 'role', 'device')
        attrs = {'class': 'table table-hover table-headings'}