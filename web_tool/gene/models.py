from django.db import models

# Create your models here.
class CisEqtl(models.Model):
    eqtls = models.TextField(db_column='eQTLs', blank=True, null=True)  # Field name made lowercase.
    snp_chr = models.TextField(db_column='SNP_chr', blank=True, null=True)  # Field name made lowercase.
    snp_position = models.IntegerField(db_column='SNP_position', blank=True, null=True)  # Field name made lowercase.
    snp_alleles = models.TextField(db_column='SNP_alleles', blank=True, null=True)  # Field name made lowercase.
    egenes = models.TextField(blank=True, null=True)
    gene_position = models.TextField(blank=True, null=True)
    cancer_type = models.TextField(blank=True)

    class Meta:
        managed = True
        db_table = 'cis_eqtl'

class DrugList(models.Model):
    name = models.TextField(db_column='Name', blank=True, null=True)  # Field name made lowercase.
    synonyms = models.TextField(db_column='Synonyms', blank=True, null=True)  # Field name made lowercase.
    targets = models.TextField(db_column='Targets', blank=True, null=True)  # Field name made lowercase.
    target_pathway = models.TextField(db_column='Target pathway', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.

    class Meta:
        managed = True
        db_table = 'drug_list'