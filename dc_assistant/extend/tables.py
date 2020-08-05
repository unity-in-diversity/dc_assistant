import django_tables2 as tables

# class BaseTable(tables.Table):
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#
#         if self.empty_text is None:
#             #self.empty_text = 'No {} found'.format(self._meta.model._meta.verbose_name_plural)
#             self.empty_text = 'Not found'
#
#     class Meta:
#         attrs = {
#             'class': 'table table-hover table-headings'}
