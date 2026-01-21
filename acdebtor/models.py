from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save
from django.dispatch import receiver
from _lib import panda
from terms.models import Terms
from django.core.exceptions import ValidationError

class AcDebtor(models.Model):
    autokey = models.CharField(primary_key=True, db_column='Autokey',max_length=32, editable=False, unique=True)
    accno = models.CharField(max_length=40,db_column='AccNo', null= False, unique=True)
    companyname = models.CharField(max_length=100,db_column='CompanyName', null= True)
    desc2 = models.CharField(max_length=100,db_column='Desc2', null= True)
    registerno = models.CharField(max_length=30,db_column='RegisterNo', null= True)
    # new udf
    udfispallet = models.SmallIntegerField(db_column='UDF_isPallet',default=0, null=True, blank=True)
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
    salesagent = models.CharField(max_length=12,db_column='SalesAgent', null= True)
    debtortype = models.CharField(max_length=20,db_column='DebtorType', null= True)
    natureofbusiness = models.CharField(max_length=40,db_column='NatureOfBusiness', null= True)
    weburl = models.CharField(max_length=80,db_column='WebURL', null= True)
    emailaddress = models.CharField(max_length=200,db_column='EmailAddress', null= True)
    displayterm = models.CharField(max_length=50,db_column='DisplayTerm', null= True)
    creditlimit = models.DecimalField(db_column='CreditLimit', null=True, max_digits=19, decimal_places=2)
    agingon = models.CharField(max_length=1,db_column='AgingOn', null= True)
    statementtype= models.CharField(max_length=1,db_column='StatementType', null= True)
    currencycode = models.CharField(max_length=5,db_column='CurrencyCode', null= False)
    allowexceedcreditlimit = models.CharField(max_length=5,db_column='AllowExceedCreditLimit', null= False)
    note = models.CharField(max_length=255,db_column='Note', null= True)
    exemptno = models.CharField(max_length=60,db_column='ExemptNo', null= True)
    expirydate = models.DateTimeField(db_column ='ExpiryDate', editable=True, null=True)
    pricecategory = models.CharField(max_length=12,db_column='PriceCategory', null= True)
    discountpercent = models.DecimalField(db_column='DiscountPercent', null=False, max_digits=18, decimal_places=6)
    detaildiscount = models.CharField(max_length=20,db_column='DetailDiscount', null= True)
    lastmodified = models.DateTimeField(db_column ='LastModified', editable=True, null=False)
    lastmodifieduserid = models.CharField(max_length=10,db_column='LastModifiedUserID', null= False)
    createdtimestamp = models.DateTimeField(db_column ='CreatedTimeStamp', editable=False, null=False)
    createduserid = models.CharField(db_column ='CreatedUserID',max_length=30, editable=False, null=False)
    overduelimit = models.DecimalField(db_column='OverdueLimit', null=True, max_digits=19, decimal_places=2)
    hasbonuspoint = models.CharField(db_column ='HasBonusPoint',max_length=1, null=False)
    openingbonuspoint = models.DecimalField(db_column='OpeningBonuspoint', null=True, max_digits=19, decimal_places=2)
    soblockstatus = models.SmallIntegerField(db_column='SOBlockStatus', null=True)
    doblockstatus = models.SmallIntegerField(db_column='DOBlockStatus', null=True)
    ivblockstatus = models.SmallIntegerField(db_column='IVBlockStatus', null=True)
    csblockstatus = models.SmallIntegerField(db_column='CSBlockStatus', null=True)
    qtblockmessage = models.SmallIntegerField(db_column='QTBlockMessage', null=True)
    soblockmessage = models.SmallIntegerField(db_column='SOBlockMessage', null=True)
    doblockmessage = models.SmallIntegerField(db_column='DOBlockMessage', null=True)
    ivblockmessage = models.SmallIntegerField(db_column='IVBlockMessage', null=True)
    csblockmessage = models.SmallIntegerField(db_column='CSBlockMessage', null=True)
    externallink = models.CharField(db_column ='ExternalLink',max_length=255, null=True)
    isgroupcompany = models.CharField(db_column ='IsGroupCompany',max_length=1, null=False)
    isactive = models.CharField(db_column ='IsActive',max_length=1, null=False)
    lastupdate = models.IntegerField(db_column='LastUpdate', null=False)
    contactinfo = models.CharField(db_column ='ContactInfo',max_length=255, null=True)
    accountgroup = models.CharField(db_column ='AccountGroup',max_length=12, null=True)  
    markupratio = models.DecimalField(db_column='MarkupRatio', null=True, max_digits=18, decimal_places=6)
    # taxregisterno = models.CharField(db_column ='TaxRegisterNo',max_length=20, null=True)
    calcdiscountonunitprice = models.CharField(db_column ='CalcDiscountOnUnitPrice',max_length=1, null=True)
    gststatusverifieddate = models.DateTimeField(db_column ='GSTStatusVerifiedDate', editable=False, null=True)
    inclusivetax = models.CharField(db_column ='InclusiveTax',max_length=1, null=False)
    roundingmethod = models.IntegerField(db_column = 'RoundingMethod')
    selfbilledapprovalno =  models.CharField(db_column ='SelfBilledApprovalNo',max_length=1, null=True)
    guid = models.CharField(max_length= 32, unique = True, db_column='Guid', null=False)
    istaxregistered = models.CharField(max_length=5, db_column='IsTaxRegistered', null=True)
    # receiptwithholdingtaxcode = models.CharField(max_length= 14, db_column='ReceiptWithHoldingTaxCode', null=True) 
    # paymentwithholdingtaxcode = models.CharField(max_length= 14,db_column='PaymentWithHoldingTaxCode', null=True) 
    multiprice = models.CharField(db_column ='MultiPrice',max_length=8, null=True)
    allowchangemultiprice = models.CharField(db_column ='AllowChangeMultiPrice',max_length=1, null=True)
    # taxbranchid = models.CharField(db_column ='TaxBranchID',max_length=8, null=True ,)
    # servicetaxregisterno = models.CharField(db_column ='ServiceTaxRegisterNo',max_length=20, null=True)
    mobile = models.CharField(db_column ='Mobile',max_length=25, null=True)
    cgblockstatus = models.SmallIntegerField(db_column='CGBlockStatus', null=True)
    cgblockmessage = models.CharField(db_column ='CGBlockMessage',max_length=40, null=True)

    class Meta:
        # app_label = 'MlItemmaster'
        managed = False
        db_table = "debtor"
        ordering = ("accno",)

    def __str__(self):
        return self.autokey
    
    def get_absolute_url(self):
        return f"/{self.autokey}/"
    
@receiver(pre_save, sender=AcDebtor)
def pre_save_company(sender, instance, **kwargs):
    raise ValidationError("You cannot save a record to autocount mssql.")