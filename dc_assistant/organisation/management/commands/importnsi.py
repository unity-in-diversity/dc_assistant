from django.core.management.base import BaseCommand
from organisation.models import Vendor
from dc_assistant import settings
import csv
import os

print(os.path.dirname)
BASE_DIR = settings.BASE_DIR

class Command(BaseCommand):

    def handle(self, *args, **options):
        vendors = str(BASE_DIR + "\\initializers\\vendors.csv")
        with open(vendors, newline='') as f:
            reader = csv.reader(f, delimiter=';')
            for row in reader:
                if row[0] != 'name':
                    vendor = Vendor()
                    vendor.name = row[0]
                    vendor.slug = row[1]
                    vendor.save()
        print('Import success')

