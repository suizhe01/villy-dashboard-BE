from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save
from django.dispatch import receiver
from _lib import panda
from company.models import Company

# Create your models here.
class TaxType(models.Model):
    autokey = models.CharField(primary_key=True, db_column='Autokey',max_length=32, editable=False, unique=True)
    companyautokey = models.ForeignKey(Company,
                                       models.DO_NOTHING,
                                       db_column='CompanyAutoKey',
                                       related_name='TaxTypeCompanyAutokey'
                                       )
    taxtype = models.CharField(max_length=14,db_column='TaxType', null= False)
    description = models.CharField(max_length=120,db_column='Description', null= True)
    taxrate = models.DecimalField(max_digits=18, decimal_places=6, db_column='TaxRate', null=False)
    inclusive = models.CharField(max_length=1,db_column='Inclusive', null= False)
    isactive = models.CharField(max_length=1,db_column='IsActive', null= False)
    lastupdate = models.IntegerField(db_column='LastUpdate', null=False)
    govtaxcode = models.CharField(max_length=8,db_column='GovTaxCode', null= True)
    supplypurchase = models.CharField(max_length=1,db_column='SupplyPurchase', null= False)
    isdefault = models.CharField(max_length=1,db_column='Isdefault', null= False)
    taxaccno = models.CharField(max_length=12,db_column='TaxAccNo', null= True)
    iszerorate = models.CharField(max_length=1,db_column='IsZeroRate', null= False)
    usetrxtaxaccno = models.CharField(max_length=1,db_column='UseTrxTaxAccNo', null= False)
    accountingbasis = models.IntegerField(db_column='AccountingBasis', null=False)
    addtocost = models.CharField(max_length=1,db_column='AddToCost', null= False)
    guid = models.CharField(max_length=32,db_column='Guid', null= False, unique=True)
    taxsystem = models.CharField(max_length=50,db_column='TaxSystem', null= True)

    class Meta:
        # app_label = 'MlItemmaster'
        managed = True
        db_table = "taxtype"
        ordering = ("taxtype",)

    def __str__(self):
        return self.autokey
    
    def get_absolute_url(self):
        return f"/{self.autokey}/"
    
@receiver(pre_save, sender=TaxType)
def pre_save_company(sender, instance, **kwargs):
    print("pre_save")
    # instance.updated_at = panda.panda_today()
    if instance.autokey == "":
        instance.autokey = panda.panda_uuid()