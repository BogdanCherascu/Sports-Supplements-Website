

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categorie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nume', models.CharField(max_length=100, unique=True)),
                ('descriere', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nume', models.CharField(max_length=100)),
                ('descriere', models.TextField()),
                ('tip', models.CharField(choices=[('activ', 'Activ'), ('aroma', 'Aromă'), ('vitamina', 'Vitamină'), ('altul', 'Altul')], default='altul', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Oferta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_incepere', models.DateField()),
                ('data_finalizare', models.DateField()),
                ('procentaj', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Producator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nume', models.CharField(max_length=100, unique=True)),
                ('tara_origine', models.CharField(max_length=100)),
                ('an_infiintare', models.IntegerField()),
                ('cifra_afaceri', models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Produs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nume', models.CharField(max_length=150)),
                ('pret', models.FloatField()),
                ('stoc', models.IntegerField(default=0)),
                ('activ', models.BooleanField(default=True)),
                ('data_adaugare', models.DateTimeField(auto_now_add=True)),
                ('categorie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='produse', to='magazin.categorie')),
                ('ingrediente', models.ManyToManyField(blank=True, to='magazin.ingredient')),
                ('oferte', models.ManyToManyField(blank=True, to='magazin.oferta')),
                ('producator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='produse', to='magazin.producator')),
            ],
        ),
    ]
