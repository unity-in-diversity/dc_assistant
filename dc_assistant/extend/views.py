from django.shortcuts import render
from django.views.generic import View
from django.contrib.contenttypes.models import ContentType

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
    #action_buttons = ('add', 'import', 'export')

    def get(self, request):

        model = self.queryset.model
        content_type = ContentType.objects.get_for_model(model)

        if self.filterset:
            self.queryset = self.filterset(request.GET, self.queryset).qs

        table = self.table(self.queryset)
        if 'pk' in table.base_columns:
            table.columns.show('pk')

        context = {
            'content_type': content_type,
            'table': table,
        }
        return render(request, self.template_name, context)
