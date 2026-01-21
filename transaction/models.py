from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save
from django.dispatch import receiver
from _lib import panda
from lorry.models import Lorry

class Transaction(models.Model):
    transactionguid = models.CharField(primary_key=True, db_column='TransactionGuid',max_length=32, editable=False, unique=True)
    lorryguid = models.ForeignKey(Lorry,
                                       models.DO_NOTHING,
                                       db_column='LorryGuid',
                                       related_name='TransactionLorryGuid'
                                       )
    docno = models.CharField(max_length=20,db_column='DocNo', null= False)
    docdate = models.DateTimeField(db_column='DocDate', null=False)
    debtorname = models.CharField(max_length=80, db_column='DebtorName', null=False)
    debtorcode = models.CharField(max_length=80, db_column='DebtorCode', null=False)
    share = models.SmallIntegerField(db_column='Share', null=True)
    udfispallet = models.SmallIntegerField(db_column='UdfIsPallet',default=0, null=True, blank=True)
    
    class Meta:
        # app_label = 'MlItemmaster'
        managed = True
        db_table = "transaction"
        ordering = ("transactionguid",)

    def __str__(self):
        return self.transactionguid
    
    def get_absolute_url(self):
        return f"/{self.transactionguid}/"
    
@receiver(pre_save, sender=Transaction)
def pre_save_company(sender, instance, **kwargs):
    print("pre_save")
    # instance.updated_at = panda.panda_today()
    if instance.transactionguid == "":
        instance.transactionguid = panda.panda_uuid()