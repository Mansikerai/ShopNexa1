from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='product_name',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='cartitem',
            name='price',
            field=models.DecimalField(default=0, max_digits=10, decimal_places=2),
        ),
    ]
