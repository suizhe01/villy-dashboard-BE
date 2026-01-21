from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save
from django.dispatch import receiver
from _lib import panda
from branch.models import Branch

# Create your models here.
class Location(models.Model):
    autokey = models.CharField(primary_key=True, db_column='Autokey',max_length=32, editable=False, unique=True)
    branchautokey = models.ForeignKey(Branch,
                                       models.DO_NOTHING,
                                       db_column='BranchAutoKey',
                                       related_name='LocationBranchAutokey'
                                       )
    location = models.CharField(max_length=30,db_column='Location', null= False,unique=True)
    description = models.CharField(max_length=80, db_column = 'Description', null=True)
    desc2 = models.CharField(max_length=80, db_column='Desc2', null=True)
    address1 = models.CharField(max_length=40, db_column='Address1', null=True)
    address2 = models.CharField(max_length=40, db_column='Address2', null=True)
    address3 = models.CharField(max_length=40, db_column='Address3', null=True)
    address4 = models.CharField(max_length=40, db_column='Address4', null=True)
    postcode = models.CharField(max_length=10, db_column='PostCode', null=True)
    phone1 = models.CharField(max_length=25, db_column='Phone1', null=True)
    phone2 = models.CharField(max_length=25, db_column='Phone2', null=True)
    fax1 = models.CharField(max_length=25, db_column='Fax1', null=True)
    fax2 = models.CharField(max_length=25, db_column='Fax2', null=True)
    contact = models.CharField(max_length=40, db_column='Contact', null=True)
    note = models.CharField(max_length=255,  db_column='Note', null=True)
    isactive = models.CharField(max_length=5,  db_column='IsActive', null=False)
    lastupdate = models.IntegerField( db_column='LastUpdate', null=False)
    areacode = models.CharField(max_length=12, db_column='AreaCode', null=True)
    cashpaymentmethod = models.CharField(max_length=20, db_column='CashPayment', null=True)
    debitcardpayment = models.CharField(max_length=20, db_column='DebitCardPayment', null=True)
    voucherpaymentmethod = models.CharField(max_length=20, db_column='VoucherPaymentMethod', null=True)
    chequepaymentmethod = models.CharField(max_length=20, db_column='ChequePaymentMethod', null=True)
    pointpaymentmethod = models.CharField(max_length=20, db_column='PointPaymentMethod', null=True)
    roundingaccno = models.CharField(max_length=12, db_column='RoundingAccNo', null=True)
    depositaccno = models.CharField(max_length=12, db_column='DepositAccNo', null=True)
    forfeitedaccno = models.CharField(max_length=12, db_column='ForfeitedAccNo', null=True)
    creditcardchargesaccno = models.CharField(max_length=12, db_column='CreditCardChargesAccNo', null=True)
    pointpaymentaccno = models.CharField(max_length=12, db_column='PointPaymentAccNo', null=True)
    servicechargeaccno = models.CharField(max_length=12, db_column='ServiceChargeAccNo', null=True)
    voucherforfitedaccno = models.CharField(max_length=12, db_column='VoucherForfeitedAccNo', null=True)
    guid = models.CharField(max_length=32, unique=True, db_column='Guid', null=True)
    tipaccno = models.CharField(max_length=12, null=True, db_column='TipAccNo')

    class Meta:
        # app_label = 'MlItemmaster'
        managed = True
        db_table = "location"
        ordering = ("location",)

    def __str__(self):
        return self.autokey
    
    def get_absolute_url(self):
        return f"/{self.autokey}/"
    
@receiver(pre_save, sender=Location)
def pre_save_company(sender, instance, **kwargs):
    print("pre_save")
    # instance.updated_at = panda.panda_today()
    if not instance.autokey:
        instance.autokey = panda.panda_uuid()

    if not instance.guid:
        instance.guid = panda.panda_uuid()