from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save
from django.dispatch import receiver
from _lib import panda
from branch.models import Branch
from terms.models import Terms

# Create your models here.
class DN(models.Model):
    autokey = models.CharField(primary_key=True, db_column='Autokey',max_length=32, editable=False, unique=True)
    branchautokey = models.ForeignKey(Branch,
                                       models.DO_NOTHING,
                                       db_column='BranchAutoKey',
                                       related_name='DNBranchAutokey'
                                       )
    displayterm = models.ForeignKey(Terms,
                                       models.DO_NOTHING,
                                       db_column='DisplayTerm',
                                       related_name='DNTermsDisplayTerm'
                                       )
    docno = models.CharField(max_length=20,db_column='DocNo', null= False)
    docdate = models.DateTimeField(db_column='DocDate', null=False)
    debtorcode = models.CharField(max_length=12,db_column='DebtorCode', null= True)
    debtorname = models.CharField(max_length=100,db_column='DebtorName', null= True)
    dntype = models.CharField(max_length=12,db_column='DNType', null= True)
    ref = models.CharField(max_length=40,db_column='Ref', null= True)
    ourinvoiceno = models.CharField(max_length=40,db_column='OurInvoiceNo', null= True)
    description = models.CharField(max_length=80,db_column='Description', null= True)
    salesagent = models.CharField(max_length=12,db_column='SalesAgent', null= True)
    invaddr1 = models.CharField(max_length=40,db_column='InvAddr1', null= True)
    invaddr2 = models.CharField(max_length=40,db_column='InvAddr2', null= True)
    invaddr3 = models.CharField(max_length=40,db_column='InvAddr3', null= True)
    invaddr4 = models.CharField(max_length=40,db_column='InvAddr4', null= True)
    phone1 = models.CharField(max_length=25,db_column='Phone1', null= True)
    fax1 = models.CharField(max_length=25,db_column='Fax1', null= True)
    attention = models.CharField(max_length=40,db_column='Attention', null= True)
    branchcode = models.CharField(max_length=20,db_column='BranchCode', null= True)
    deliveraddr1 = models.CharField(max_length=40,db_column='DeliverAddr1', null= True)
    deliveraddr2 = models.CharField(max_length=40,db_column='DeliverAddr2', null= True)
    deliveraddr3 = models.CharField(max_length=40,db_column='DeliverAddr3', null= True)
    deliveraddr4 = models.CharField(max_length=40,db_column='DeliverAddr4', null= True)
    deliverphone1 = models.CharField(max_length=25,db_column='DeliverPhone1', null= True)
    deliverfax1 = models.CharField(max_length=25,db_column='DeliverFax1', null= True)
    delivercontact = models.CharField(max_length=40,db_column='DeliverContact', null= True)
    salesexemptionno = models.CharField(max_length=60,db_column='SalesExemptionNo', null= True)
    salesexemptionexpirydate = models.DateTimeField(db_column='SalesExemptionExpiryDate', null=True)
    total = models.DecimalField(db_column='Total', max_digits=19, decimal_places=2, null=True)
    footer1param = models.DecimalField(db_column='Footer1Param', max_digits=19, decimal_places=2, null=True)
    footer1Amt = models.DecimalField(db_column='Footer1Amt', max_digits=19, decimal_places=2, null=True)
    footer1localamt = models.DecimalField(db_column='Footer1LocalAmt', max_digits=19, decimal_places=2, null=True)
    footer1taxtype = models.CharField(max_length=14,db_column='Footer1TaxType', null= True)
    footer2param = models.DecimalField(db_column='Footer2Param', max_digits=19, decimal_places=2, null=True)
    footer2Amt = models.DecimalField(db_column='Footer2Amt', max_digits=19, decimal_places=2, null=True)
    footer2localamt = models.DecimalField(db_column='Footer2LocalAmt', max_digits=19, decimal_places=2, null=True)
    footer2taxtype = models.CharField(max_length=14,db_column='Footer2TaxType', null= True)
    footer3param = models.DecimalField(db_column='Footer3Param', max_digits=19, decimal_places=2, null=True)
    footer3Amt = models.DecimalField(db_column='Footer3Amt', max_digits=19, decimal_places=2, null=True)
    footer3localamt = models.DecimalField(db_column='Footer3LocalAmt', max_digits=19, decimal_places=2, null=True)
    footer3taxtype = models.CharField(max_length=14,db_column='Footer3TaxType', null= True)
    currencycode = models.CharField(max_length=5,db_column='CurrencyCode', null= False)
    currencyrate = models.DecimalField(db_column='CurrencyRate', max_digits=19, decimal_places=2, null=False)
    nettotal = models.DecimalField(db_column='NetTotal', max_digits=19, decimal_places=2, null=True)
    localnettotal = models.DecimalField(db_column='LocalNetTotal', max_digits=19, decimal_places=2, null=True)
    analysisnettotal = models.DecimalField(db_column='AnalysisNetTotal', max_digits=19, decimal_places=2, null=True)
    localanalysisnettotal = models.DecimalField(max_digits=19, decimal_places=2, db_column='LocalAnalysisNetTotal', null=True)
    localtotalcost = models.DecimalField(max_digits=25, decimal_places=8, db_column='LocalTotalCost', null=True)
    tax = models.DecimalField(db_column='Tax', max_digits=19, decimal_places=2, null=True)
    localtax = models.DecimalField(db_column='LocalTax', max_digits=19, decimal_places=2, null=True)
    totalbonuspoint = models.DecimalField(db_column='TotalBonusPoint', max_digits=19, decimal_places=2, null=True)
    posttostock = models.CharField(max_length=1,db_column='PostToStock', null= False)
    posttogl = models.CharField(max_length=1,db_column='PostToGL', null= False)
    referdockey = models.BigIntegerField(db_column='ReferDocKey', null=True)
    note = models.CharField(max_length=255,db_column='Note', null= True)
    remark1 = models.CharField(max_length=40,db_column='Remark1', null= True)
    remark2 = models.CharField(max_length=40,db_column='Remark2', null= True)
    remark3 = models.CharField(max_length=40,db_column='Remark3', null= True)
    remark4 = models.CharField(max_length=40,db_column='Remark4', null= True)
    printcount = models.SmallIntegerField(db_column='PrintCount', null=False)
    cancelled = models.CharField(max_length=1,db_column='Cancelled', null= False)
    lastmodified = models.DateTimeField(db_column='LastModified', null = False)
    lastmodifieduserid = models.CharField(max_length=10,db_column='LastModifiedUserID', null= False)
    createdtimestamp = models.DateTimeField(db_column='CreatedTimeStamp', null = False)
    createduserid = models.CharField(max_length=10,db_column='CreatedUserID', null= False)
    externallink = models.CharField(max_length=255,db_column='ExternalLink', null= True)
    refdocno = models.CharField(max_length=20,db_column='RefDocNo', null= True)     
    cansync = models.CharField(max_length=1,db_column='CanSync', null= False)
    lastupdate = models.IntegerField(db_column='LastUpdate', null=False)
    memberno = models.CharField(max_length=20,db_column='MemberNo', null= True)
    reallocatepurchasebyproject = models.CharField(max_length=1,db_column='ReallocatePurchaseByProject', null= False)
    reallocatepurchasebyprojectjedockey = models.BigIntegerField(db_column='ReallocatePurchaseByProjectJEDocKey', null=True)
    refno2 = models.CharField(max_length=20,db_column='RefNo2', null= True)
    saleslocation = models.CharField(max_length=8,db_column='SalesLocation', null= True)
    footer1tax = models.DecimalField(max_digits=19, decimal_places=2, db_column='Footer1Tax', null=True)
    footer1localtax = models.DecimalField(max_digits=19, decimal_places=2, db_column='Footer1LocalTax', null=True)
    footear2tx = models.DecimalField(max_digits=19, decimal_places=2, db_column='Footer2Tax', null=True)
    footer2localtax = models.DecimalField(max_digits=19, decimal_places=2, db_column='Footer2LocalTax', null=True)
    footer3tax = models.DecimalField(max_digits=19, decimal_places=2, db_column='Footer3Tax', null=True)
    footer3localtax = models.DecimalField(max_digits=19, decimal_places=2, db_column='Footer3LocalTax', null=True)
    extax = models.DecimalField(max_digits=19, decimal_places=2, db_column='ExTax', null=True)
    localextax = models.DecimalField(max_digits=19, decimal_places=2, db_column='LocalExTax', null=True)
    yourpono = models.CharField(max_length=25,db_column='YourPONo', null= True)
    yourpodate = models.DateTimeField(db_column='YourPODate', null=True)
    guid = models.CharField(max_length=32,db_column='Guid', null= False, unique=True)
    reallocatepurchasebyprojectno = models.CharField(max_length=10,db_column='ReallocatePurchaseByProjectNo', null= True)
    totaxcurrencyrate = models.DecimalField(max_digits=19, decimal_places=2, db_column='ToTaxCurrencyRate', null=False)
    calcdiscountonunitprice = models.CharField(max_length=1,db_column='CalcDiscountOnUnitPrice', null= True)
    taxdocno = models.CharField(max_length=20,db_column='TaxDocNo', null= True)
    totalextax = models.DecimalField(max_digits=19, decimal_places=2, db_column='TotalExTax', null=True)
    taxableamt = models.DecimalField(max_digits=19, decimal_places=2, db_column='TaxableAmt', null=True)
    reason = models.CharField(max_length=80,db_column='Reason', null= True)
    inclusivetax = models.CharField(max_length=1,db_column='InclusiveTax', null= False)
    footer1taxrate = models.DecimalField(max_digits=18, decimal_places=6, db_column='Footer1TaxRate', null=True)
    footer2taxrate = models.DecimalField(max_digits=18, decimal_places=6, db_column='Footer2TaxRate', null=True)
    footer3taxrate = models.DecimalField(max_digits=18, decimal_places=6, db_column='Footer3TaxRate', null=True)
    taxdate = models.DateTimeField(db_column='TaxDate', null=True)
    roundingmethod = models.IntegerField(db_column='RoundingMethod', null=False)
    localtaxableamt = models.DecimalField(max_digits=19, decimal_places=2, db_column='LocalTaxableAmt', null=True)
    taxcurrencytax = models.DecimalField(max_digits=19, decimal_places=2, db_column='TaxCurrencyTax', null=True)
    taxcurrencytaxableamt = models.DecimalField(max_digits=19, decimal_places=2, db_column='TaxCurrencyTaxableAmt', null=True)
    multiprice = models.CharField(max_length=8,db_column='MultiPrice', null= True)
    taxbranchid = models.CharField(max_length=8,db_column='TaxBranchID', null= True)

    class Meta:
        # app_label = 'MlItemmaster'
        managed = True
        db_table = "dn"
        ordering = ("docno",)

    def __str__(self):
        return self.autokey
    
    def get_absolute_url(self):
        return f"/{self.autokey}/"
    
@receiver(pre_save, sender=DN)
def pre_save_company(sender, instance, **kwargs):
    print("pre_save")
    # instance.updated_at = panda.panda_today()
    if instance.autokey == "":
        instance.autokey = panda.panda_uuid()