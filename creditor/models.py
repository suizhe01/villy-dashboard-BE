from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save
from django.dispatch import receiver
from _lib import panda
from company.models import Company

class Creditor(models.Model):
    autokey = models.CharField(primary_key=True, db_column='Autokey',max_length=32, editable=False, unique=True)
    companyautokey = models.ForeignKey(Company,
                                       models.DO_NOTHING,
                                       db_column='CompanyAutoKey',
                                       related_name='CreditorCompanyAutokey'
                                       )
    accno = models.CharField(max_length=12,db_column='AccNo', null= False, unique=True)
    companyname = models.CharField(max_length=100,db_column='CompanyName', null= True, unique=True)
    desc2 = models.CharField(max_length=100,db_column='Desc2', null= True)
    registorno = models.CharField(max_length=30,db_column='RegistorNo', null= True)
    address1 = models.CharField(max_length=40,db_column='Address1', null= True)
    address2 = models.CharField(max_length=40,db_column='Address2', null= True)
    address3 = models.CharField(max_length=40,db_column='Address3', null= True)
    address4 = models.CharField(max_length=40,db_column='Address4', null= True)
    postcode = models.CharField(max_length=10,db_column='PostCode', null= True)
    deliveraddr1 = models.CharField(max_length=40,db_column='DeliverAddr1', null= True)
    deliveraddr2 = models.CharField(max_length=40,db_column='DeliverAddr2', null= True)
    deliveraddr3 = models.CharField(max_length=40,db_column='DeliverAddr3', null= True)
    deliveraddr4 = models.CharField(max_length=40,db_column='DeliverAddr4', null= True)
    deliverpostcode = models.CharField(max_length=10,db_column='DeliverPostCode', null= True)
    attention = models.CharField(max_length=40,db_column='Attention', null= True)
    phone1 = models.CharField(max_length=25,db_column='Phone1', null= True)
    phone2 = models.CharField(max_length=25,db_column='Phone2', null= True)
    fax1 = models.CharField(max_length=25,db_column='Fax1', null= True)
    fax2 = models.CharField(max_length=25,db_column='Fax2', null= True)
    areacode = models.CharField(max_length=12,db_column='AreaCode', null= True)
    purchaseagent = models.CharField(max_length=12,db_column='PurchaseAgent', null= True)
    creditortype = models.CharField(max_length=20,db_column='CreditorType', null= True)
    natureofbusiness = models.CharField(max_length=40,db_column='NatureOfBusiness', null= True)
    weburl = models.CharField(max_length=80,db_column='WebURL', null= True)
    emailaddress = models.CharField(max_length=200,db_column='EmailAddress', null= True)
    displayterm = models.CharField(max_length=30,db_column='DisplayTerm', null= True)
    creditlimit = models.DecimalField(db_column='CreditLimit', null=True, max_digits=19, decimal_places=2)
    agingon = models.CharField(max_length=1,db_column='AgingOn', null= True)
    statementtype= models.CharField(max_length=1,db_column='StatementType', null= True)
    currencycode = models.CharField(max_length=5,db_column='CurrencyCode', null= False)
    allowexceedcreditlimit = models.CharField(max_length=1,db_column='AllowExceedCreditLimit', null= False)
    note = models.CharField(max_length=255,db_column='Note', null= True)
    exemptno = models.CharField(max_length=60,db_column='ExemptNo', null= False)
    expirydate = models.DateTimeField(db_column ='ExpiryDate', editable=True, null=True)
    pricecategory = models.CharField(max_length=12,db_column='PriceCategory', null= True)
    taxtype = models.CharField(max_length=14,db_column='TaxType', null= True)
    discountpercent = models.DecimalField(db_column='DiscountPercent', null=False, max_digits=18, decimal_places=6)
    detaildiscount = models.CharField(max_length=20,db_column='DetailDiscount', null= True)
    lastmodified = models.DateTimeField(db_column ='LastModified', editable=True, null=False)
    lastmodifieduserid = models.CharField(max_length=10,db_column='LastModifiedUserID', null= False)
    createdtimestamp = models.DateTimeField(db_column ='CreatedTimeStamp', editable=False, null=False, auto_now=True)
    createduserid = models.CharField(db_column ='CreatedUserID',max_length=30, editable=False, null=False)
    overduelimit = models.DecimalField(db_column='OverdueLimit', null=True, max_digits=19, decimal_places=2)
    poblockstatus = models.SmallIntegerField(db_column='POBlockStatus', null=True)
    gnblockstatus = models.SmallIntegerField(db_column='GNBlockStatus', null=True)
    piblockstatus = models.SmallIntegerField(db_column='PIBlockStatus', null=True)
    cpblockstatus = models.SmallIntegerField(db_column='CPBlockStatus', null=True)
    poblockmessage = models.SmallIntegerField(db_column='POBlockMessage', null=True)
    gnblockmessage = models.SmallIntegerField(db_column='GNBlockMessage', null=True)
    piblockmessage = models.SmallIntegerField(db_column='PIBlockMessage', null=True)
    cpblockmessage = models.SmallIntegerField(db_column='CPBlockMessage', null=True)
    externallink = models.CharField(db_column ='ExternalLink',max_length=255, null=True)
    isgroupcompany = models.CharField(db_column ='IsGroupCompany',max_length=1, null=False)
    isactive = models.CharField(db_column ='IsActive',max_length=1, null=False)
    lastupdate = models.IntegerField(db_column='LastUpdate', null=False)
    contactinfo = models.CharField(db_column ='ContactInfo',max_length=255, null=True)
    accountgroup = models.CharField(db_column ='AccountGroup',max_length=12, null=True)  
    markupratio = models.DecimalField(db_column='MarkupRatio', null=True, max_digits=18, decimal_places=6)
    taxregisterno = models.CharField(db_column ='TaxRegisterNo',max_length=20, null=True)
    calcdiscountonunitprice = models.CharField(db_column ='CalcDiscountOnUnitPrice',max_length=1, null=True)
    gststatusverifieddate = models.DateTimeField(db_column ='GSTStatusVerifiedDate', editable=True, null=True)
    inclusivetax = models.CharField(db_column ='InclusiveTax',max_length=1, null=False)
    selfbilledapprovalno =  models.CharField(db_column ='SelfBilledApprovalNo',max_length=1, null=False)
    roundingmethod = models.IntegerField(db_column = 'RoundingMethod', null=False)
    receiptwithholdingtaxcode = models.CharField(max_length= 14, db_column='ReceiptWithHoldingTaxCode', null=True) 
    paymentwithholdingtaxcode = models.CharField(max_length= 14,db_column='PaymentWithHoldingTaxCode', null=True) 
    taxbranchid = models.CharField(max_length= 8,db_column='TaxBranchID', null=True) 
    mobile = models.CharField(db_column ='Mobile',max_length=25, null=True)
    pgblockstatus = models.SmallIntegerField(db_column='PGBlockStatus', null=True)
    pgblockmessage = models.CharField(db_column ='PGBlockMessage',max_length=40, null=True)

    class Meta:
        # app_label = 'MlItemmaster'
        managed = True
        db_table = "creditor"
        ordering = ("companyname",)

    def __str__(self):
        return self.autokey
    
    def get_absolute_url(self):
        return f"/{self.autokey}/"
    
@receiver(pre_save, sender=Creditor)
def pre_save_company(sender, instance, **kwargs):
    print("pre_save")
    # instance.updated_at = panda.panda_today()
    if instance.autokey == "":
        instance.autokey = panda.panda_uuid()