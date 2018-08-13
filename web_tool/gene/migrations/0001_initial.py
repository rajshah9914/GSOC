# Generated by Django 2.0.5 on 2018-06-09 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LuadCisEqtl',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('eqtls', models.TextField(blank=True, db_column='eQTLs', null=True)),
                ('snp_chr', models.TextField(blank=True, db_column='SNP_chr', null=True)),
                ('snp_position', models.IntegerField(blank=True, db_column='SNP_position', null=True)),
                ('snp_alleles', models.TextField(blank=True, db_column='SNP_alleles', null=True)),
                ('egenes', models.TextField(blank=True, null=True)),
                ('gene_position', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'luad_cis_eqtl',
                'managed': True,
            },
        ),
    ]