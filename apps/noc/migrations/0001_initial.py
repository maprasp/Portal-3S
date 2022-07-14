# Generated by Django 3.2 on 2021-06-10 14:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('infra', '0002_auto_20210610_1145'),
    ]

    operations = [
        migrations.CreateModel(
            name='Checklist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('turno', models.CharField(max_length=20)),
                ('criado', models.DateTimeField(auto_now_add=True, verbose_name='criado em')),
                ('outros', models.TextField(blank=True, null=True, verbose_name='outros')),
            ],
            options={
                'ordering': ['-criado', '-turno'],
            },
        ),
        migrations.CreateModel(
            name='ChecklistServidorNagiosServico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alerta_monitoramento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='infra.servidornagiosservico')),
                ('checklist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='noc.checklist')),
            ],
        ),
        migrations.CreateModel(
            name='ChecklistResponsaveis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('checklist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='noc.checklist')),
                ('responsavel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ChecklistOcorrencia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alerta_equipamento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='infra.ocorrencia')),
                ('checklist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='noc.checklist')),
            ],
        ),
        migrations.AddField(
            model_name='checklist',
            name='alerta_equipamento',
            field=models.ManyToManyField(blank=True, through='noc.ChecklistOcorrencia', to='infra.Ocorrencia'),
        ),
        migrations.AddField(
            model_name='checklist',
            name='alerta_monitoramento',
            field=models.ManyToManyField(blank=True, through='noc.ChecklistServidorNagiosServico', to='infra.ServidorNagiosServico'),
        ),
        migrations.AddField(
            model_name='checklist',
            name='responsaveis',
            field=models.ManyToManyField(blank=True, through='noc.ChecklistResponsaveis', to=settings.AUTH_USER_MODEL),
        ),
    ]
