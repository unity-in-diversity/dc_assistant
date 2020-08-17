from django.shortcuts import render
from django.views.generic import View
from django.contrib.contenttypes.models import ContentType
from django_tables2 import RequestConfig
from django.core.paginator import Paginator, Page
from django.conf import settings
from organisation.models import Rack, Location

from dal import autocomplete


class ListObjectsView(View):
    """
    List View таблицы объектов.

    queryset: запрос для отображения
    filter: фильр django-filter примененый к запросу
    table: таблица django-tables2 используется для отрисовки списка объектов
    template_name: html шаблон для ренедеринга
    """
    queryset = None
    filterset = None
    table = None
    template_name = None
    #template_name = 'utilities/obj_list.html'

    def get(self, request):

        model = self.queryset.model
        content_type = ContentType.objects.get_for_model(model)

        if self.filterset:
            self.queryset = self.filterset(request.GET, self.queryset).qs

        table = self.table(self.queryset)
        if 'pk' in table.base_columns:
            table.columns.show('pk')

        paginate = {
            'paginator_class': Paginator,
            'per_page': request.GET.get('per_page', settings.PAGINATE_COUNT)
        }
        RequestConfig(request, paginate).configure(table)

        context = {
            'content_type': content_type,
            'table': table,
        }
        return render(request, self.template_name, context)

class TagListView(View):
    pass

class RackAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # if not self.request.user.is_authenticated:
        #     return Rack.objects.none()

        qs = Rack.objects.all()
        #print(qs)

        location = self.forwarded.get('location', None)
        print(location)

        if location:
            qs = qs.filter(location=location)

        # if self.q:
        #     qs = qs.filter(name__istartswith=self.q)

        return qs
