from django.core.management.base import BaseCommand
from polls.models import LstUsd, Users, Project
from datetime import datetime

class Command(BaseCommand):
    def handle(self, *args, **options):
        for UnqId in LstUsd.objects.all():
            try:
                DteOfObj = UnqId.dte
                DteUnqKey = UnqId.unqKey
                DteOfObj = DteOfObj.date()
                now = datetime.now().date()
                diff = now-DteOfObj
                diff = diff.days
                if diff > 30:
                    Project.objects.filter(unqKey=DteUnqKey).delete()
                    Users.objects.filter(unqKey=DteUnqKey).delete()
                    LstUsd.objects.filter(unqKey=DteUnqKey).delete()
            except Exception as e:
                print(e.message)
                pass
        exit()