# Generated by Django 5.2 on 2025-06-24 15:38

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('APP_PRINCIPAL', '0014_calificacion_cliente_calificacion_evento_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='HaircutRecommendation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('frente', models.ImageField(upload_to='recomendaciones/frente/')),
                ('lado_izq', models.ImageField(upload_to='recomendaciones/lado_izq/')),
                ('lado_der', models.ImageField(upload_to='recomendaciones/lado_der/')),
                ('atras', models.ImageField(upload_to='recomendaciones/atras/')),
                ('recomendacion', models.TextField()),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recomendaciones', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
