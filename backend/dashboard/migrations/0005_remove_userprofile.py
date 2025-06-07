from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_alter_progressentry_options_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ] 