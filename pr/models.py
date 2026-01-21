from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save
from django.dispatch import receiver
from _lib import panda
from branch.models import Branch
from terms.models import Terms
from creditor.models import Creditor

# Create your models here.
class PR(models.Model):
    autokey = models.CharField(primary_key=True, db_column='AutoKey',max_length=32, editable=False, unique=True)
    branchautokey = models.ForeignKey(Branch,
                                       models.DO_NOTHING,
                                       db_column='BranchAutoKey',
                                       related_name='PRBranchAutokey'
                                       )
    displayterm = models.ForeignKey(Terms,
                                       models.DO_NOTHING,
                                       db_column='DisplayTerm',
                                       related_name='PRDisplayTerm',
                                       to_field='displayterm'
                                       )
    creditorcode = models.ForeignKey(Creditor,
                                models.DO_NOTHING,
                                db_column='CreditorCode',
                                related_name='PRCreditorAccNo',
                                null=False,
                                to_field='accno'
                                )
    creditorname = models.ForeignKey(Creditor,
                                models.DO_NOTHING,
                                db_column='CreditorName',
                                related_name='PRCreditorCompanyName',
                                null=False,
                                to_field='companyname'
                                )
    docno = models.CharField(max_length=20,db_column='DocNo', null= False)
    docdate = models.DateTimeField(db_column='DocDate', null=False)
    ref = models.CharField(max_length=40,db_column='Ref', null= True)
    suppliercnno = models.CharField(max_length=20,db_column='SupplierCNNo', null= True)
    description = models.CharField(max_length=80,db_column='Description', null= True)
    purchaseagent = models.CharField(max_length=12,db_column='PurchaseAgent', null= True)
    invaddr1 = models.CharField(max_length=40,db_column='InvAddr1', null= True)
    invaddr2 = models.CharField(max_length=40,db_column='InvAddr2', null= True)
    invaddr3 = models.CharField(max_length=40,db_column='InvAddr3', null= True)
    invaddr4 = models.CharField(max_length=40,db_column='InvAddr4', null= True)
    phone1 = models.CharField(max_length=25,db_column='Phone1', null= True)
    fax1 = models.CharField(max_length=25,db_column='Fax1', null= True)
    attention = models.CharField(max_length=40,db_column='Attention', null= True)
    branchcode = models.CharField(max_length=20,db_column='BranchCode', null= True)
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
    currencycode = models.CharField(max_length=5,db_column='CrrencyCode', null= False)
    currencyrate = models.DecimalField(db_column='CurrencyRate', max_digits=19, decimal_places=2, null=False)
    nettotal = models.DecimalField(db_column='NetTotal', max_digits=19, decimal_places=2, null=True)
    localnettotal = models.DecimalField(db_column='LocalNetTotal', max_digits=19, decimal_places=2, null=True)
    tax = models.DecimalField(db_column='Tax', max_digits=19, decimal_places=2, null=True)
    localtax = models.DecimalField(db_column='LocalTax', max_digits=19, decimal_places=2, null=True)
    posttostock = models.CharField(max_length=1,db_column='PostToStock', null= False)
    posttogl = models.CharField(max_length=1,db_column='PostToGL', null= False)
    referdockey = models.BigIntegerField(db_column='ReferDocKey', null=True)
    note = models.CharField(max_length=255,db_column='Note', null= True)
    remark1 = models.CharField(max_length=40,db_column='Remark1', null= True)
    remark2 = models.CharField(max_length=40,db_column='Remark2', null= True)
    remark3 = models.CharField(max_length=40,db_column='Remark3', null= True)
    remark4 = models.CharField(max_length=40,db_column='Remark4', null= True)
    printcount = models.SmallIntegerField(db_column='PrintCOunt', null=False)
    cancelled = models.CharField(max_length=1,db_column='Cancelled', null= False)
    lastmodified = models.DateTimeField(db_column='LastModified', null = False)
    lastmodifieduserid = models.CharField(max_length=10,db_column='LastModifiedUserID', null= False)
    createdtimestamp = models.DateTimeField(db_column='CreatedTimeStamp', null = False)
    createduserid = models.CharField(max_length=10,db_column='CreatedUserID', null= False)
    externallink = models.CharField(max_length=255,db_column='ExternalLink', null= True)
    refdocno = models.CharField(max_length=20,db_column='RefDocNo', null= True)
    cansync = models.CharField(max_length=1,db_column='CanSync', null= False)
    lastupdate = models.IntegerField(db_column='LastUpdate', null=False)
    refno2 = models.CharField(max_length=20,db_column='RefNo2', null= True)
    purchaselocation = models.CharField(max_length=8,db_column='PurchaseLocation', null= True)
    footer1tax = models.DecimalField(max_digits=19, decimal_places=2, db_column='Footer1Tax', null=True)
    footer1localtax = models.DecimalField(max_digits=19, decimal_places=2, db_column='Footer1LocalTax', null=True)
    footear2tx = models.DecimalField(max_digits=19, decimal_places=2, db_column='Footer2Tax', null=True)
    footer2localtax = models.DecimalField(max_digits=19, decimal_places=2, db_column='Footer2LocalTax', null=True)
    footer3tax = models.DecimalField(max_digits=19, decimal_places=2, db_column='Footer3Tax', null=True)
    footer3localtax = models.DecimalField(max_digits=19, decimal_places=2, db_column='Footer3LocalTax', null=True)
    extax = models.DecimalField(max_digits=19, decimal_places=2, db_column='ExTax', null=True)
    localextax = models.DecimalField(max_digits=19, decimal_places=2, db_column='LocalExTax', null=True)
    analysisnettotal = models.DecimalField(max_digits=19, decimal_places=2, db_column='AnalysisNetTotal', null=True)
    localanalysisnettotal = models.DecimalField(max_digits=19, decimal_places=2, db_column='LocalAnalysisNetTotal', null=True)
    guid = models.CharField(max_length=32,db_column='Guid', null= False, unique=True)
    totaxcurrencyrate = models.DecimalField(max_digits=19, decimal_places=12, db_column='ToTaxCurrencyRate', null=False)
    calcdiscountonunitprice = models.CharField(max_length=1,db_column='CalcDiscountOnUnitPrice', null= True)
    taxdocno = models.CharField(max_length=20,db_column='TaxDocNo', null= True)
    totalextax = models.DecimalField(max_digits=19, decimal_places=2, db_column='TotalExTax', null=True)
    taxableamt = models.DecimalField(max_digits=19, decimal_places=2, db_column='TaxableAmt', null=True)
    supplierinvoiceno = models.CharField(max_length=40,db_column='SupplierInvoiceNo', null= True)
    reason = models.CharField(max_length=80,db_column='Reason', null= True)
    inclusivetax = models.CharField(max_length=1,db_column='InclusiveTax', null= False)
    footer1taxrate = models.DecimalField(max_digits=18, decimal_places=6, db_column='Footer1TaxRate', null=True)
    footer2taxrate = models.DecimalField(max_digits=18, decimal_places=6, db_column='Footer2TaxRate', null=True)
    footer3taxrate = models.DecimalField(max_digits=18, decimal_places=6, db_column='Footer3TaxRate', null=True)
    taxdate = models.DateTimeField(db_column='TaxDate', null=True)
    isroundadj = models.CharField(max_length=1,db_column='IsRoundAdj', null= False)
    roundadj = models.DecimalField(max_digits=19, decimal_places=2, db_column='RoundedAdj', null=True)
    finaltotal = models.DecimalField(max_digits=19, decimal_places=2, db_column='FinalTotal', null=True)
    roundingmethod = models.IntegerField(db_column='RoundingMethod', null=False)
    localtaxableamt = models.DecimalField(max_digits=19, decimal_places=2, db_column='LocalTaxableAmt', null=True)
    taxcurrencytax = models.DecimalField(max_digits=19, decimal_places=2, db_column='TaxCurrencyTax', null=True)
    taxcurrencytaxableamt = models.DecimalField(max_digits=19, decimal_places=2, db_column='TaxCurrencyTaxableAmt', null=True)
    docdate2 = models.DateTimeField(db_column='DocDate2', null=True)
    taxbranchid = models.CharField(max_length=8,db_column='TaxBranchID', null= True)

    class Meta:
        # app_label = 'MlItemmaster'
        managed = True
        db_table = "pr"
        ordering = ("docno",)

    def __str__(self):
        return self.autokey
    
    def get_absolute_url(self):
        return f"/{self.autokey}/"
    
@receiver(pre_save, sender=PR)
def pre_save_company(sender, instance, **kwargs):
    print("pre_save")
    # instance.updated_at = panda.panda_today()
    if instance.autokey == "":
        instance.autokey = panda.panda_uuid()