# Generated by Django 2.0.3 on 2018-04-04 18:04

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Curriculum',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('personalData', models.CharField(blank=True, max_length=1000, verbose_name='Datos personales')),
                ('experience', models.CharField(blank=True, max_length=300, verbose_name='Experiencia')),
                ('education', models.CharField(blank=True, max_length=100, verbose_name='Educación')),
                ('misc', models.CharField(blank=True, max_length=300, verbose_name='Miscellaneous')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(verbose_name='Descripción')),
                ('created', models.DateField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('price', models.DecimalField(decimal_places=2, max_digits=20, verbose_name='Precio')),
                ('avaliability', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(10)], verbose_name='Disponibilidad')),
                ('category', models.CharField(choices=[('Cuidado parcial', 'Cuidado parcial'), ('Cuidado completo', 'Cuidado completo'), ('Cuidado nocturno', 'Cuidado nocturno'), ('Cuidado hospitalario', 'Cuidado hospitalario'), ('Recados', 'Recados'), ('Sin especificar', 'Sin especificar')], max_length=50, verbose_name='Categoría')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Autor')),
                ('offerer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='offerer', to=settings.AUTH_USER_MODEL, verbose_name='Solicitante')),
            ],
        ),
        migrations.CreateModel(
            name='UserDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('birthday', models.DateField(verbose_name='Fecha de nacimiento')),
                ('phone', models.CharField(blank=True, max_length=17, validators=[django.core.validators.RegexValidator(message="El número debe seguir el siguiente patrón: '+999999999'. Máximo 15 dígitos.", regex='^\\+?1?\\d{9,15}$')], verbose_name='Teléfono')),
                ('postalAddress', models.CharField(max_length=100, verbose_name='Domicilio')),
                ('gender', models.CharField(choices=[('M', 'Mujer'), ('H', 'Hombre'), ('O', 'Otro')], max_length=1, verbose_name='Género')),
                ('occupation', models.CharField(max_length=100, verbose_name='Profesión')),
                ('photo', models.URLField(max_length=600, verbose_name='Foto')),
                ('socialReferences', models.CharField(blank=True, max_length=600, null=True, verbose_name='Redes Sociales')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
            ],
        ),
    ]
