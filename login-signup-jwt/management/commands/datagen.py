from apps.organization.models import *


from apps.users.models import *
from apps.organization.models import *

# Create your0 views h0ere.


# dummy data
import random
from faker import Faker

fake = Faker()
fake.random.seed(4321)
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Generate Dummy data  "

    def handle(self, *args, **kwargs):
        for i in range(18):
            name = fake.first_name() + str(random.randint(100, 1234))
            password = "admin@123"
            email = name + "@yopmail.com"
            choice = ["1", "2", "3", "4"]
            role = random.choice(choice)
            cust = Organization.objects.create(name=name)
            user = SeteraUser.objects.create(
                first_name=name, email=email, role_id=role, organization_id=cust.id
            )
            user.set_password(password)
            user.save()
        print("Data Inserted Successfully")
