from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save
from django.dispatch import receiver
from _lib import panda
from company.models import Company
from item.models import Item

# Create your models here.
class ItemBatch(models.Model):
    autokey = models.CharField(primary_key=True, db_column='Autokey',max_length=32, editable=False, unique=True)
    companyautokey = models.ForeignKey(Company,
                                       models.DO_NOTHING,
                                       db_column='CompanyAutoKey',
                                       related_name='ItemBatchCompanyAutokey'
                                       )
    itemcode = models.ForeignKey(Item,
                                       models.DO_NOTHING,
                                       db_column='ItemCode',
                                       related_name='ItemBatchItemCode',
                                       null=False
                                       )
    batchno = models.CharField(max_length=20,db_column='BatchNo', null= False)
    description = models.CharField(max_length=40,db_column='Description', null= True)
    manufactureddate = models.DateTimeField(db_column='ManufacturedDate',editable=False, null=True)
    expirydate = models.DateTimeField(db_column='ExpiryDate',editable=False,null=True)
    lastsaledate = models.DateTimeField(db_column='LastSaleDate',editable=False,null=True)
    guid = models.CharField(max_length=32,db_column='Guid', null= False, unique=True)

    class Meta:
        # app_label = 'MlItemmaster'
        managed = True
        db_table = "itembatch"
        ordering = ("batchno",)

    def __str__(self):
        return self.autokey
    
    def get_absolute_url(self):
        return f"/{self.autokey}/"
    
@receiver(pre_save, sender=ItemBatch)
def pre_save_company(sender, instance, **kwargs):
    print("pre_save")
    # instance.updated_at = panda.panda_today()
    if instance.autokey == "":
        instance.autokey = panda.panda_uuid()