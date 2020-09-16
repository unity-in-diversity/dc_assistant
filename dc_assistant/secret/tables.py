import django_tables2 as tables
from .models import Secret, SecretRole


SECRETROLE_ACTIONS = """
<a href="{% url 'secret:secretrole_edit' slug=record.slug %}" class="btn btn-warning btn-sm"><i class="m-r-10 mdi mdi-grease-pencil" aria-hidden="true"></i></a>
"""


class SecretRoleTable(tables.Table):
    name = tables.LinkColumn()
    secret_count = tables.Column(verbose_name='Secrets')
    actions = tables.TemplateColumn(
        template_code=SECRETROLE_ACTIONS, attrs={'td': {'class': 'text-right noprint'}}, verbose_name=''
    )

    class Meta:
        model = SecretRole
        fields = ('name', 'secret_count', 'description', 'actions')
        attrs = {'class': 'table table-hover table-headings'}


class SecretTable(tables.Table):
    device = tables.LinkColumn()

    class Meta:
        model = Secret
        fields = ('name', 'role', 'device')
        attrs = {'class': 'table table-hover table-headings'}