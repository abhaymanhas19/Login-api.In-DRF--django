from apps.organization.models import *
from apps.users.models import *
from apps.organization.models import *
from faker import Faker

fake = Faker()
fake.random.seed(4321)
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Generate Dummy data  "

    def handle(self, *args, **kwargs):
        list = ["Supervisor", "Reseller", "ResellerAgent", "CustomerAdmin"]
        for i in list:
            UserRoles.objects.create(name=i)
        print("roles add successfully")
