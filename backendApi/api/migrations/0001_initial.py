from django.db import migrations
from api.user.models import User

class Migration(migrations.Migration):
    def seed_data(apps, schema_editor):
        user = CustomUser( email="admin@siterecon.ai", is_staff=True, is_superuser=True, contact_number="7830346973", address="Noida",organisation="SiteRecon")
        user.set_password("siterecon@123")
        user.save()

        dependencies = []
        operations= [migrations.RunPython(seed_data),]