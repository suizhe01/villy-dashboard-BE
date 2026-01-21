from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save
from django.dispatch import receiver
from _lib import panda
from transaction.models import Transaction
from itemclass.models import ItemClass

class TransactionDtl(models.Model):
    transactiondtlguid = models.CharField(primary_key=True, db_column='TransactionDtlGuid',max_length=32, editable=False, unique=True)
    transactionguid = models.ForeignKey(Transaction,
                                       models.DO_NOTHING,
                                       db_column='TransactionGuid',
                                       related_name='TransactionDtlTransactionGuid'
                                            )
    itemclass = models.ForeignKey(ItemClass,
                                       models.DO_NOTHING,
                                       db_column='ItemClass',
                                       related_name='TransactionDtlItemClass',
                                       to_field='itemclass'
                                            )
    itemcode = models.CharField(max_length=80,db_column='ItemCode', null=False)
    description = models.CharField(max_length=100,db_column='Description', null= True)
    qty = models.DecimalField(db_column='Qty', max_digits=25, decimal_places=8, null=True)
    subtotal = models.DecimalField(db_column='SubTotal', max_digits=19, decimal_places=2, null=True)
    uom = models.CharField(max_length=30,db_column='Uom', null= True)
    commtype = models.CharField(max_length=30,db_column='CommType', null= True)
    # commvalue = models.CharField(max_length=30,db_column='CommValue', null= True)
    udfcalmethod = models.CharField(max_length=8,db_column='UdfCalMethod', null= True)
    udfcalrate = models.DecimalField(db_column='UdfCalRate', max_digits=2, decimal_places=2, null=True)
    isqtyupdated = models.BooleanField(db_column='IsQtyUpdated', default=False)
    udfispallet = models.SmallIntegerField(db_column='UdfIsPallet',default=0, null=True, blank=True)

    class Meta:
        # app_label = 'MlItemmaster'
        managed = True
        db_table = "transactiondtl"
        ordering = ("transactiondtlguid",)

    def __str__(self):
        return self.transactiondtlguid
    
    def get_absolute_url(self):
        return f"/{self.transactiondtlguid}/"
    
@receiver(pre_save, sender=TransactionDtl)
def pre_save_company(sender, instance, **kwargs):
    print("pre_save")
    # instance.updated_at = panda.panda_today()
    if instance.transactiondtlguid == "":
        instance.transactiondtlguid = panda.panda_uuid()
    
