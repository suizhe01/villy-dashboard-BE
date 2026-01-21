# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Adj(models.Model):
    autokey = models.CharField(db_column='Autokey', primary_key=True, max_length=32)  # Field name made lowercase.
    docno = models.CharField(db_column='DocNo', max_length=20)  # Field name made lowercase.
    docdate = models.DateTimeField(db_column='DocDate')  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=80, blank=True, null=True)  # Field name made lowercase.
    total = models.DecimalField(db_column='Total', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    note = models.CharField(db_column='Note', max_length=255, blank=True, null=True)  # Field name made lowercase.
    remark1 = models.CharField(db_column='Remark1', max_length=40, blank=True, null=True)  # Field name made lowercase.
    remark2 = models.CharField(db_column='Remark2', max_length=40, blank=True, null=True)  # Field name made lowercase.
    remark3 = models.CharField(db_column='Remark3', max_length=40, blank=True, null=True)  # Field name made lowercase.
    remark4 = models.CharField(db_column='Remark4', max_length=40, blank=True, null=True)  # Field name made lowercase.
    printcount = models.SmallIntegerField(db_column='PrintCount')  # Field name made lowercase.
    cancelled = models.CharField(db_column='Cancelled', max_length=1)  # Field name made lowercase.
    lastmodified = models.DateTimeField(db_column='LastModified')  # Field name made lowercase.
    lastmodifieduserid = models.CharField(db_column='LastModifiedUserID', max_length=10)  # Field name made lowercase.
    createdtimestamp = models.DateTimeField(db_column='CreatedTimeStamp')  # Field name made lowercase.
    createduserid = models.CharField(db_column='CreatedUserID', max_length=10)  # Field name made lowercase.
    externallink = models.CharField(db_column='ExternalLink', max_length=255, blank=True, null=True)  # Field name made lowercase.
    refdocno = models.CharField(db_column='RefDocNo', max_length=20, blank=True, null=True)  # Field name made lowercase.
    lastupdate = models.IntegerField(db_column='LastUpdate')  # Field name made lowercase.
    cansync = models.CharField(db_column='CanSync', max_length=1)  # Field name made lowercase.
    guid = models.CharField(db_column='Guid', unique=True, max_length=32)  # Field name made lowercase.
    branchautokey = models.ForeignKey('Branch', models.DO_NOTHING, db_column='BranchAutoKey')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'adj'


class Adjdtl(models.Model):
    autokey = models.CharField(db_column='Autokey', primary_key=True, max_length=32)  # Field name made lowercase.
    seq = models.IntegerField(db_column='Seq')  # Field name made lowercase.
    numbering = models.CharField(db_column='Numbering', max_length=6, blank=True, null=True)  # Field name made lowercase.
    batchno = models.CharField(db_column='BatchNo', max_length=20, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=100, blank=True, null=True)  # Field name made lowercase.
    furtherdescription = models.CharField(db_column='FurtherDescription', max_length=255, blank=True, null=True)  # Field name made lowercase.
    projno = models.CharField(db_column='ProjNo', max_length=10, blank=True, null=True)  # Field name made lowercase.
    deptno = models.CharField(db_column='DeptNo', max_length=10, blank=True, null=True)  # Field name made lowercase.
    qty = models.DecimalField(db_column='Qty', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    uom = models.CharField(db_column='UOM', max_length=8, blank=True, null=True)  # Field name made lowercase.
    subtotal = models.DecimalField(db_column='SubTotal', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    printout = models.CharField(db_column='PrintOut', max_length=1)  # Field name made lowercase.
    serialnolist = models.CharField(db_column='SerialNoList', max_length=255, blank=True, null=True)  # Field name made lowercase.
    guid = models.CharField(db_column='Guid', unique=True, max_length=32)  # Field name made lowercase.
    desc2 = models.CharField(db_column='Desc2', max_length=100, blank=True, null=True)  # Field name made lowercase.
    adjautokey = models.ForeignKey(Adj, models.DO_NOTHING, db_column='ADJAutokey')  # Field name made lowercase.
    itemcode = models.ForeignKey('Item', models.DO_NOTHING, db_column='ItemCode', blank=True, null=True)  # Field name made lowercase.
    location = models.ForeignKey('Location', models.DO_NOTHING, db_column='Location', blank=True, null=True)  # Field name made lowercase.
    unitcost = models.DecimalField(db_column='UnitCost', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'adjdtl'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class AuthtokenToken(models.Model):
    key = models.CharField(primary_key=True, max_length=40)
    created = models.DateTimeField()
    user = models.OneToOneField(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'authtoken_token'


class AutocountDebtor(models.Model):
    accno = models.CharField(db_column='AccNo', primary_key=True, max_length=20)  # Field name made lowercase.
    companyname = models.CharField(db_column='CompanyName', max_length=500, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'autocount_debtor'


class Branch(models.Model):
    autokey = models.CharField(db_column='Autokey', primary_key=True, max_length=32)  # Field name made lowercase.
    code = models.CharField(db_column='Code', max_length=32)  # Field name made lowercase.
    address = models.CharField(db_column='Address', unique=True, max_length=255)  # Field name made lowercase.
    companyautokey = models.ForeignKey('Company', models.DO_NOTHING, db_column='CompanyAutoKey')  # Field name made lowercase.
    registorno = models.CharField(db_column='RegistorNo', max_length=32)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'branch'


class Cn(models.Model):
    autokey = models.CharField(db_column='Autokey', primary_key=True, max_length=32)  # Field name made lowercase.
    docno = models.CharField(db_column='DocNo', max_length=255)  # Field name made lowercase.
    docdate = models.DateTimeField(db_column='DocDate')  # Field name made lowercase.
    debtorcode = models.ForeignKey('Debtor', models.DO_NOTHING, db_column='DebtorCode', to_field='AccNo')  # Field name made lowercase.
    debtorname = models.CharField(db_column='DebtorName', max_length=80)  # Field name made lowercase.
    cntype = models.CharField(db_column='CNType', max_length=12, blank=True, null=True)  # Field name made lowercase.
    ref = models.CharField(db_column='Ref', max_length=40, blank=True, null=True)  # Field name made lowercase.
    ourinvoiceno = models.CharField(db_column='OurInvoiceNo', max_length=40, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=80, blank=True, null=True)  # Field name made lowercase.
    salesagent = models.ForeignKey('Salesagent', models.DO_NOTHING, db_column='SalesAgent', to_field='SalesAgent')  # Field name made lowercase.
    invaddr1 = models.CharField(db_column='InvAddr1', max_length=40, blank=True, null=True)  # Field name made lowercase.
    invaddr2 = models.CharField(db_column='InvAddr2', max_length=40, blank=True, null=True)  # Field name made lowercase.
    invaddr3 = models.CharField(db_column='InvAddr3', max_length=40, blank=True, null=True)  # Field name made lowercase.
    invaddr4 = models.CharField(db_column='InvAddr4', max_length=40, blank=True, null=True)  # Field name made lowercase.
    phone1 = models.CharField(db_column='Phone1', max_length=25, blank=True, null=True)  # Field name made lowercase.
    fax1 = models.CharField(db_column='Fax1', max_length=25, blank=True, null=True)  # Field name made lowercase.
    attention = models.CharField(db_column='Attention', max_length=40, blank=True, null=True)  # Field name made lowercase.
    branchcode = models.CharField(db_column='BranchCode', max_length=20, blank=True, null=True)  # Field name made lowercase.
    deliveraddr1 = models.CharField(db_column='DeliverAddr1', max_length=40, blank=True, null=True)  # Field name made lowercase.
    deliveraddr2 = models.CharField(db_column='DeliverAddr2', max_length=40, blank=True, null=True)  # Field name made lowercase.
    deliveraddr3 = models.CharField(db_column='DeliverAddr3', max_length=40, blank=True, null=True)  # Field name made lowercase.
    deliveraddr4 = models.CharField(db_column='DeliverAddr4', max_length=40, blank=True, null=True)  # Field name made lowercase.
    deliverphone1 = models.CharField(db_column='DeliverPhone1', max_length=25, blank=True, null=True)  # Field name made lowercase.
    deliverfax1 = models.CharField(db_column='DeliverFax1', max_length=25, blank=True, null=True)  # Field name made lowercase.
    delivercontact = models.CharField(db_column='DeliverContact', max_length=40, blank=True, null=True)  # Field name made lowercase.
    salesexemptionno = models.CharField(db_column='SalesExemptionNo', max_length=60, blank=True, null=True)  # Field name made lowercase.
    salesexemptionexpirydate = models.DateTimeField(db_column='SalesExemptionExpiryDate', blank=True, null=True)  # Field name made lowercase.
    total = models.DecimalField(db_column='Total', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer1param = models.DecimalField(db_column='Footer1Param', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer1amt = models.DecimalField(db_column='Footer1Amt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer1localamt = models.DecimalField(db_column='Footer1LocalAmt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer1taxtype = models.CharField(db_column='Footer1TaxType', max_length=14, blank=True, null=True)  # Field name made lowercase.
    footer2param = models.DecimalField(db_column='Footer2Param', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer2amt = models.DecimalField(db_column='Footer2Amt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer2localamt = models.DecimalField(db_column='Footer2LocalAmt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer2taxtype = models.CharField(db_column='Footer2TaxType', max_length=14, blank=True, null=True)  # Field name made lowercase.
    footer3param = models.DecimalField(db_column='Footer3Param', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer3amt = models.DecimalField(db_column='Footer3Amt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer3localamt = models.DecimalField(db_column='Footer3LocalAmt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer3taxtype = models.CharField(db_column='Footer3TaxType', max_length=14, blank=True, null=True)  # Field name made lowercase.
    crrencycode = models.CharField(db_column='CrrencyCode', max_length=5)  # Field name made lowercase.
    currencyrate = models.DecimalField(db_column='CurrencyRate', max_digits=19, decimal_places=2)  # Field name made lowercase.
    nettotal = models.DecimalField(db_column='NetTotal', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    localnettotal = models.DecimalField(db_column='LocalNetTotal', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    analysisnettotal = models.DecimalField(db_column='AnalysisNetTotal', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    localanalysisnettotal = models.DecimalField(db_column='LocalAnalysisNetTotal', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    localtotalcost = models.DecimalField(db_column='LocalTotalCost', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    tax = models.DecimalField(db_column='Tax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    localtax = models.DecimalField(db_column='LocalTax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    totalbonuspoint = models.DecimalField(db_column='TotalBonusPoint', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    posttostock = models.CharField(db_column='PostToStock', max_length=1)  # Field name made lowercase.
    posttogl = models.CharField(db_column='PostToGL', max_length=1)  # Field name made lowercase.
    referdockey = models.BigIntegerField(db_column='ReferDocKey', blank=True, null=True)  # Field name made lowercase.
    note = models.CharField(db_column='Note', max_length=255, blank=True, null=True)  # Field name made lowercase.
    remark1 = models.CharField(db_column='Remark1', max_length=40, blank=True, null=True)  # Field name made lowercase.
    remark2 = models.CharField(db_column='Remark2', max_length=40, blank=True, null=True)  # Field name made lowercase.
    remark3 = models.CharField(db_column='Remark3', max_length=40, blank=True, null=True)  # Field name made lowercase.
    remark4 = models.CharField(db_column='Remark4', max_length=40, blank=True, null=True)  # Field name made lowercase.
    printcount = models.SmallIntegerField(db_column='PrintCOunt')  # Field name made lowercase.
    cancelled = models.CharField(db_column='Cancelled', max_length=1)  # Field name made lowercase.
    lastmodified = models.DateTimeField(db_column='LastModified')  # Field name made lowercase.
    lastmodifieduserid = models.CharField(db_column='LastModifiedUserID', max_length=10)  # Field name made lowercase.
    createdtimestamp = models.DateTimeField(db_column='CreatedTimeStamp')  # Field name made lowercase.
    createduserid = models.CharField(db_column='CreatedUserID', max_length=10)  # Field name made lowercase.
    externallink = models.CharField(db_column='ExternalLink', max_length=255, blank=True, null=True)  # Field name made lowercase.
    refdocno = models.CharField(db_column='RefDocNo', max_length=20, blank=True, null=True)  # Field name made lowercase.
    cansync = models.CharField(db_column='CanSync', max_length=1)  # Field name made lowercase.
    lastupdate = models.IntegerField(db_column='LastUpdate')  # Field name made lowercase.
    memberno = models.CharField(db_column='MemberNo', max_length=20, blank=True, null=True)  # Field name made lowercase.
    refno2 = models.CharField(db_column='RefNo2', max_length=20, blank=True, null=True)  # Field name made lowercase.
    saleslocation = models.CharField(db_column='SalesLocation', max_length=8, blank=True, null=True)  # Field name made lowercase.
    footer1tax = models.DecimalField(db_column='Footer1Tax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer1localtax = models.DecimalField(db_column='Footer1LocalTax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer2tax = models.DecimalField(db_column='Footer2Tax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer2localtax = models.DecimalField(db_column='Footer2LocalTax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer3tax = models.DecimalField(db_column='Footer3Tax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer3localtax = models.DecimalField(db_column='Footer3LocalTax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    extax = models.DecimalField(db_column='ExTax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    localextax = models.DecimalField(db_column='LocalExTax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    yourpono = models.CharField(db_column='YourPONo', max_length=25, blank=True, null=True)  # Field name made lowercase.
    yourpodate = models.DateTimeField(db_column='YourPODate', blank=True, null=True)  # Field name made lowercase.
    guid = models.CharField(db_column='Guid', unique=True, max_length=32)  # Field name made lowercase.
    totaxcurrencyrate = models.DecimalField(db_column='ToTaxCurrencyRate', max_digits=19, decimal_places=2)  # Field name made lowercase.
    calcdiscountonunitprice = models.CharField(db_column='CalcDiscountOnUnitPrice', max_length=1, blank=True, null=True)  # Field name made lowercase.
    taxdocno = models.CharField(db_column='TaxDocNo', max_length=20, blank=True, null=True)  # Field name made lowercase.
    totalextax = models.DecimalField(db_column='TotalExTax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    taxableamt = models.DecimalField(db_column='TaxableAmt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    reason = models.CharField(db_column='Reason', max_length=80, blank=True, null=True)  # Field name made lowercase.
    inclusivetax = models.CharField(db_column='InclusiveTax', max_length=1)  # Field name made lowercase.
    footer1taxrate = models.DecimalField(db_column='Footer1TaxRate', max_digits=18, decimal_places=6, blank=True, null=True)  # Field name made lowercase.
    footer2taxrate = models.DecimalField(db_column='Footer2TaxRate', max_digits=18, decimal_places=6, blank=True, null=True)  # Field name made lowercase.
    footer3taxrate = models.DecimalField(db_column='Footer3TaxRate', max_digits=18, decimal_places=6, blank=True, null=True)  # Field name made lowercase.
    taxdate = models.DateTimeField(db_column='TaxDate', blank=True, null=True)  # Field name made lowercase.
    isroundadj = models.CharField(db_column='IsRoundAdj', max_length=5)  # Field name made lowercase.
    roundadj = models.DecimalField(db_column='RoundAdj', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    finaltotal = models.DecimalField(db_column='FinalTotal', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    roundingmethod = models.IntegerField(db_column='RoundingMethod')  # Field name made lowercase.
    localtaxableamt = models.DecimalField(db_column='LocalTaxableAmt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    taxcurrencytax = models.DecimalField(db_column='TaxCurrencyTax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    taxcurrencytaxableamt = models.DecimalField(db_column='TaxCurrencyTaxableAmt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    multiprice = models.CharField(db_column='MultiPrice', max_length=8, blank=True, null=True)  # Field name made lowercase.
    taxbranchid = models.CharField(db_column='TaxBranchID', max_length=8, blank=True, null=True)  # Field name made lowercase.
    branchautokey = models.CharField(db_column='BranchAutoKey', max_length=255)  # Field name made lowercase.
    displayterm = models.ForeignKey('Terms', models.DO_NOTHING, db_column='DisplayTerm')  # Field name made lowercase.
    lorrydriver = models.ForeignKey('Lorrydriver', models.DO_NOTHING, db_column='LorryDriver', to_field='LorryDriver')  # Field name made lowercase.
    udfbook = models.PositiveSmallIntegerField(db_column='UdfBook', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'cn'


class Cndtl(models.Model):
    autokey = models.CharField(db_column='Autokey', primary_key=True, max_length=32)  # Field name made lowercase.
    focdtlkey = models.BigIntegerField(db_column='FOCDtlKey', blank=True, null=True)  # Field name made lowercase.
    seq = models.IntegerField(db_column='Seq')  # Field name made lowercase.
    indent = models.SmallIntegerField(db_column='Indent', blank=True, null=True)  # Field name made lowercase.
    fontstyle = models.CharField(db_column='FontStyle', max_length=8, blank=True, null=True)  # Field name made lowercase.
    mainitem = models.CharField(db_column='MainItem', max_length=5)  # Field name made lowercase.
    numbering = models.CharField(db_column='Numbering', max_length=6, blank=True, null=True)  # Field name made lowercase.
    batchno = models.CharField(db_column='BatchNo', max_length=20, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=100, blank=True, null=True)  # Field name made lowercase.
    furtherdescription = models.CharField(db_column='FurtherDescription', max_length=255, blank=True, null=True)  # Field name made lowercase.
    posttostockdate = models.DateTimeField(db_column='PostToStockDate', blank=True, null=True)  # Field name made lowercase.
    projno = models.CharField(db_column='ProjNo', max_length=10, blank=True, null=True)  # Field name made lowercase.
    deptno = models.CharField(db_column='DeptNo', max_length=10, blank=True, null=True)  # Field name made lowercase.
    uom = models.CharField(db_column='UOM', max_length=8, blank=True, null=True)  # Field name made lowercase.
    useruom = models.CharField(db_column='UserUOM', max_length=8, blank=True, null=True)  # Field name made lowercase.
    qty = models.DecimalField(db_column='Qty', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    rate = models.DecimalField(db_column='Rate', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    smallestqty = models.DecimalField(db_column='SmallestQty', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    focqty = models.DecimalField(max_digits=25, decimal_places=8, blank=True, null=True)
    smallestunitprice = models.DecimalField(db_column='SmallestUnitPrice', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    unitprice = models.DecimalField(db_column='UnitPrice', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    unitcost = models.DecimalField(db_column='UnitCost', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    focunitcost = models.DecimalField(db_column='FOCUnitCost', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    discount = models.CharField(db_column='Discount', max_length=20, blank=True, null=True)  # Field name made lowercase.
    discountamt = models.DecimalField(db_column='DiscountAmt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    taxtype = models.CharField(db_column='TaxType', max_length=14, blank=True, null=True)  # Field name made lowercase.
    tax = models.DecimalField(db_column='Tax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    subtotal = models.DecimalField(db_column='SubTotal', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    localsubtotal = models.DecimalField(db_column='LocalSubTotal', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    bonuspoint = models.DecimalField(db_column='BonusPoint', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    printout = models.CharField(db_column='PrintOut', max_length=1)  # Field name made lowercase.
    dtltype = models.CharField(db_column='DtlType', max_length=1, blank=True, null=True)  # Field name made lowercase.
    calcbypercent = models.DecimalField(db_column='CalcByPercent', max_digits=18, decimal_places=6, blank=True, null=True)  # Field name made lowercase.
    addtosubtotal = models.CharField(db_column='AddToSubTotal', max_length=1)  # Field name made lowercase.
    fromdoctype = models.CharField(db_column='FromDocType', max_length=2, blank=True, null=True)  # Field name made lowercase.
    fromdocno = models.CharField(db_column='FromDocNo', max_length=255, blank=True, null=True)  # Field name made lowercase.
    fromdocdtlkey = models.BigIntegerField(db_column='FromDocDtlKey', blank=True, null=True)  # Field name made lowercase.
    accno = models.CharField(db_column='AccNo', max_length=12, blank=True, null=True)  # Field name made lowercase.
    fulltransferoption = models.CharField(db_column='FullTransferOption', max_length=1, blank=True, null=True)  # Field name made lowercase.
    fulltransferfromdoclist = models.CharField(db_column='FullTransferFromDocList', max_length=255, blank=True, null=True)  # Field name made lowercase.
    serialnolist = models.CharField(db_column='SerialNoList', max_length=255, blank=True, null=True)  # Field name made lowercase.
    packagedockey = models.BigIntegerField(db_column='PackageDocKey', blank=True, null=True)  # Field name made lowercase.
    packagedtlkey = models.BigIntegerField(db_column='PackageDtlKey', blank=True, null=True)  # Field name made lowercase.
    subqty = models.DecimalField(db_column='SubQty', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    iscalcbonuspoint = models.CharField(db_column='IsCalcBonusPoint', max_length=1, blank=True, null=True)  # Field name made lowercase.
    subtotalextax = models.DecimalField(db_column='SubTotalExTax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    localtax = models.DecimalField(db_column='LocalTax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    yourpono = models.CharField(db_column='YourPONo', max_length=25, blank=True, null=True)  # Field name made lowercase.
    yourpodate = models.DateTimeField(db_column='YourPODate', blank=True, null=True)  # Field name made lowercase.
    guid = models.CharField(db_column='Guid', unique=True, max_length=32)  # Field name made lowercase.
    ruleno = models.BigIntegerField(db_column='RuleNo', blank=True, null=True)  # Field name made lowercase.
    goodsreturn = models.CharField(db_column='GoodsReturn', max_length=1, blank=True, null=True)  # Field name made lowercase.
    taxableamt = models.DecimalField(db_column='TaxableAmt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    taxadjustment = models.DecimalField(db_column='TaxAdjustment', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    taxexportcountry = models.CharField(db_column='TaxExportCountry', max_length=50, blank=True, null=True)  # Field name made lowercase.
    localsubtotalextax = models.DecimalField(db_column='LocalSubTotalExTax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    extradiscountamt = models.DecimalField(db_column='ExtraDiscountAmt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    taxrate = models.DecimalField(db_column='TaxRate', max_digits=18, decimal_places=6, blank=True, null=True)  # Field name made lowercase.
    localtaxadjustment = models.DecimalField(db_column='LocalTaxAdjustment', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    localtaxableamt = models.DecimalField(db_column='LocalTaxableAmt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    taxcurrencytax = models.DecimalField(db_column='TaxCurrencyTax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    taxcurrencytaxableamt = models.DecimalField(db_column='TaxCurrencyTaxableAmt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    taxpermitno = models.CharField(db_column='TaxPermitNo', max_length=20, blank=True, null=True)  # Field name made lowercase.
    salesexemtionno = models.CharField(db_column='SalesExemtionNo', max_length=60, blank=True, null=True)  # Field name made lowercase.
    supplypurchase = models.CharField(db_column='SupplyPurchase', max_length=1, blank=True, null=True)  # Field name made lowercase.
    tarrifcode = models.CharField(db_column='TarrifCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    desc2 = models.CharField(db_column='Desc2', max_length=100, blank=True, null=True)  # Field name made lowercase.
    headerautokey = models.ForeignKey(Cn, models.DO_NOTHING, db_column='HeaderAutoKey')  # Field name made lowercase.
    itemcode = models.ForeignKey('Item', models.DO_NOTHING, db_column='ItemCode', to_field='ItemCode', blank=True, null=True)  # Field name made lowercase.
    location = models.ForeignKey('Location', models.DO_NOTHING, db_column='Location')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'cndtl'


class Commissionitemclass(models.Model):
    commissionitemclassguid = models.CharField(db_column='CommissionItemClassGuid', primary_key=True, max_length=32)  # Field name made lowercase.
    commtype = models.CharField(db_column='CommType', max_length=20)  # Field name made lowercase.
    itemclassguid = models.ForeignKey('Itemclass', models.DO_NOTHING, db_column='ItemClassGuid')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'commissionitemclass'


class Company(models.Model):
    autokey = models.CharField(db_column='Autokey', primary_key=True, max_length=32)  # Field name made lowercase.
    code = models.CharField(db_column='Code', unique=True, max_length=32)  # Field name made lowercase.
    address = models.CharField(db_column='Address', max_length=255)  # Field name made lowercase.
    registrationnum = models.CharField(db_column='RegistrationNum', unique=True, max_length=32)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=255)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'company'


class Creditor(models.Model):
    autokey = models.CharField(db_column='Autokey', primary_key=True, max_length=32)  # Field name made lowercase.
    accno = models.CharField(db_column='AccNo', unique=True, max_length=12)  # Field name made lowercase.
    companyname = models.CharField(db_column='CompanyName', unique=True, max_length=100, blank=True, null=True)  # Field name made lowercase.
    desc2 = models.CharField(db_column='Desc2', max_length=100, blank=True, null=True)  # Field name made lowercase.
    registorno = models.CharField(db_column='RegistorNo', max_length=30, blank=True, null=True)  # Field name made lowercase.
    address1 = models.CharField(db_column='Address1', max_length=40, blank=True, null=True)  # Field name made lowercase.
    address2 = models.CharField(db_column='Address2', max_length=40, blank=True, null=True)  # Field name made lowercase.
    address3 = models.CharField(db_column='Address3', max_length=40, blank=True, null=True)  # Field name made lowercase.
    address4 = models.CharField(db_column='Address4', max_length=40, blank=True, null=True)  # Field name made lowercase.
    postcode = models.CharField(db_column='PostCode', max_length=10, blank=True, null=True)  # Field name made lowercase.
    deliveraddr1 = models.CharField(db_column='DeliverAddr1', max_length=40, blank=True, null=True)  # Field name made lowercase.
    deliveraddr2 = models.CharField(db_column='DeliverAddr2', max_length=40, blank=True, null=True)  # Field name made lowercase.
    deliveraddr3 = models.CharField(db_column='DeliverAddr3', max_length=40, blank=True, null=True)  # Field name made lowercase.
    deliveraddr4 = models.CharField(db_column='DeliverAddr4', max_length=40, blank=True, null=True)  # Field name made lowercase.
    deliverpostcode = models.CharField(db_column='DeliverPostCode', max_length=10, blank=True, null=True)  # Field name made lowercase.
    attention = models.CharField(db_column='Attention', max_length=40, blank=True, null=True)  # Field name made lowercase.
    phone1 = models.CharField(db_column='Phone1', max_length=25, blank=True, null=True)  # Field name made lowercase.
    phone2 = models.CharField(db_column='Phone2', max_length=25, blank=True, null=True)  # Field name made lowercase.
    fax1 = models.CharField(db_column='Fax1', max_length=25, blank=True, null=True)  # Field name made lowercase.
    fax2 = models.CharField(db_column='Fax2', max_length=25, blank=True, null=True)  # Field name made lowercase.
    areacode = models.CharField(db_column='AreaCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    purchaseagent = models.CharField(db_column='PurchaseAgent', max_length=12, blank=True, null=True)  # Field name made lowercase.
    creditortype = models.CharField(db_column='CreditorType', max_length=20, blank=True, null=True)  # Field name made lowercase.
    natureofbusiness = models.CharField(db_column='NatureOfBusiness', max_length=40, blank=True, null=True)  # Field name made lowercase.
    weburl = models.CharField(db_column='WebURL', max_length=80, blank=True, null=True)  # Field name made lowercase.
    emailaddress = models.CharField(db_column='EmailAddress', max_length=200, blank=True, null=True)  # Field name made lowercase.
    displayterm = models.CharField(db_column='DisplayTerm', max_length=30, blank=True, null=True)  # Field name made lowercase.
    creditlimit = models.DecimalField(db_column='CreditLimit', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    agingon = models.CharField(db_column='AgingOn', max_length=1, blank=True, null=True)  # Field name made lowercase.
    statementtype = models.CharField(db_column='StatementType', max_length=1, blank=True, null=True)  # Field name made lowercase.
    currencycode = models.CharField(db_column='CurrencyCode', max_length=5)  # Field name made lowercase.
    allowexceedcreditlimit = models.CharField(db_column='AllowExceedCreditLimit', max_length=1)  # Field name made lowercase.
    note = models.CharField(db_column='Note', max_length=255, blank=True, null=True)  # Field name made lowercase.
    exemptno = models.CharField(db_column='ExemptNo', max_length=60)  # Field name made lowercase.
    expirydate = models.DateTimeField(db_column='ExpiryDate', blank=True, null=True)  # Field name made lowercase.
    pricecategory = models.CharField(db_column='PriceCategory', max_length=12, blank=True, null=True)  # Field name made lowercase.
    taxtype = models.CharField(db_column='TaxType', max_length=14, blank=True, null=True)  # Field name made lowercase.
    discountpercent = models.DecimalField(db_column='DiscountPercent', max_digits=18, decimal_places=6)  # Field name made lowercase.
    detaildiscount = models.CharField(db_column='DetailDiscount', max_length=20, blank=True, null=True)  # Field name made lowercase.
    lastmodified = models.DateTimeField(db_column='LastModified')  # Field name made lowercase.
    lastmodifieduserid = models.CharField(db_column='LastModifiedUserID', max_length=10)  # Field name made lowercase.
    createdtimestamp = models.DateTimeField(db_column='CreatedTimeStamp')  # Field name made lowercase.
    createduserid = models.CharField(db_column='CreatedUserID', max_length=30)  # Field name made lowercase.
    overduelimit = models.DecimalField(db_column='OverdueLimit', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    poblockstatus = models.SmallIntegerField(db_column='POBlockStatus', blank=True, null=True)  # Field name made lowercase.
    gnblockstatus = models.SmallIntegerField(db_column='GNBlockStatus', blank=True, null=True)  # Field name made lowercase.
    piblockstatus = models.SmallIntegerField(db_column='PIBlockStatus', blank=True, null=True)  # Field name made lowercase.
    cpblockstatus = models.SmallIntegerField(db_column='CPBlockStatus', blank=True, null=True)  # Field name made lowercase.
    poblockmessage = models.SmallIntegerField(db_column='POBlockMessage', blank=True, null=True)  # Field name made lowercase.
    gnblockmessage = models.SmallIntegerField(db_column='GNBlockMessage', blank=True, null=True)  # Field name made lowercase.
    piblockmessage = models.SmallIntegerField(db_column='PIBlockMessage', blank=True, null=True)  # Field name made lowercase.
    cpblockmessage = models.SmallIntegerField(db_column='CPBlockMessage', blank=True, null=True)  # Field name made lowercase.
    externallink = models.CharField(db_column='ExternalLink', max_length=255, blank=True, null=True)  # Field name made lowercase.
    isgroupcompany = models.CharField(db_column='IsGroupCompany', max_length=1)  # Field name made lowercase.
    isactive = models.CharField(db_column='IsActive', max_length=1)  # Field name made lowercase.
    lastupdate = models.IntegerField(db_column='LastUpdate')  # Field name made lowercase.
    contactinfo = models.CharField(db_column='ContactInfo', max_length=255, blank=True, null=True)  # Field name made lowercase.
    accountgroup = models.CharField(db_column='AccountGroup', max_length=12, blank=True, null=True)  # Field name made lowercase.
    markupratio = models.DecimalField(db_column='MarkupRatio', max_digits=18, decimal_places=6, blank=True, null=True)  # Field name made lowercase.
    taxregisterno = models.CharField(db_column='TaxRegisterNo', max_length=20, blank=True, null=True)  # Field name made lowercase.
    calcdiscountonunitprice = models.CharField(db_column='CalcDiscountOnUnitPrice', max_length=1, blank=True, null=True)  # Field name made lowercase.
    gststatusverifieddate = models.DateTimeField(db_column='GSTStatusVerifiedDate', blank=True, null=True)  # Field name made lowercase.
    inclusivetax = models.CharField(db_column='InclusiveTax', max_length=1)  # Field name made lowercase.
    selfbilledapprovalno = models.CharField(db_column='SelfBilledApprovalNo', max_length=1)  # Field name made lowercase.
    roundingmethod = models.IntegerField(db_column='RoundingMethod')  # Field name made lowercase.
    receiptwithholdingtaxcode = models.CharField(db_column='ReceiptWithHoldingTaxCode', max_length=14, blank=True, null=True)  # Field name made lowercase.
    paymentwithholdingtaxcode = models.CharField(db_column='PaymentWithHoldingTaxCode', max_length=14, blank=True, null=True)  # Field name made lowercase.
    taxbranchid = models.CharField(db_column='TaxBranchID', max_length=8, blank=True, null=True)  # Field name made lowercase.
    mobile = models.CharField(db_column='Mobile', max_length=25, blank=True, null=True)  # Field name made lowercase.
    pgblockstatus = models.SmallIntegerField(db_column='PGBlockStatus', blank=True, null=True)  # Field name made lowercase.
    pgblockmessage = models.CharField(db_column='PGBlockMessage', max_length=40, blank=True, null=True)  # Field name made lowercase.
    companyautokey = models.ForeignKey(Company, models.DO_NOTHING, db_column='CompanyAutoKey')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'creditor'


class Creditortype(models.Model):
    autokey = models.CharField(db_column='Autokey', primary_key=True, max_length=32)  # Field name made lowercase.
    creditortype = models.CharField(db_column='CreditorType', max_length=20)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=40, blank=True, null=True)  # Field name made lowercase.
    desc2 = models.CharField(db_column='Desc2', max_length=40, blank=True, null=True)  # Field name made lowercase.
    isactive = models.CharField(db_column='IsActive', max_length=1)  # Field name made lowercase.
    lastupdate = models.IntegerField(db_column='LastUpdate')  # Field name made lowercase.
    companyautokey = models.ForeignKey(Company, models.DO_NOTHING, db_column='CompanyAutoKey')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'creditortype'


class Crew(models.Model):
    crewguid = models.CharField(db_column='CrewGuid', primary_key=True, max_length=32)  # Field name made lowercase.
    crewtype = models.CharField(db_column='CrewType', max_length=55, blank=True, null=True)  # Field name made lowercase.
    lorryguid = models.ForeignKey('Lorry', models.DO_NOTHING, db_column='LorryGuid')  # Field name made lowercase.
    crewid = models.CharField(db_column='CrewId', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'crew'


class Crewdtl(models.Model):
    crewdtlguid = models.CharField(db_column='CrewDtlGuid', primary_key=True, max_length=32)  # Field name made lowercase.
    itemclass = models.ForeignKey('Itemclass', models.DO_NOTHING, db_column='ItemClass', to_field='ItemClass')  # Field name made lowercase.
    commtype = models.CharField(db_column='CommType', max_length=100, blank=True, null=True)  # Field name made lowercase.
    commvalue = models.DecimalField(db_column='CommValue', max_digits=8, decimal_places=7, blank=True, null=True)  # Field name made lowercase.
    documentsum = models.DecimalField(db_column='DocumentSum', max_digits=25, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    calculatedcomm = models.DecimalField(db_column='CalculatedComm', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    crewguid = models.ForeignKey(Crew, models.DO_NOTHING, db_column='CrewGuid')  # Field name made lowercase.
    calculationtype = models.CharField(db_column='CalculationType', max_length=100, blank=True, null=True)  # Field name made lowercase.
    totalamount = models.DecimalField(db_column='TotalAmount', max_digits=20, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    totalqty = models.DecimalField(db_column='TotalQty', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    share = models.SmallIntegerField(db_column='Share', blank=True, null=True)  # Field name made lowercase.
    uom = models.CharField(db_column='Uom', max_length=10, blank=True, null=True)  # Field name made lowercase.
    udfcalmethod = models.CharField(db_column='UdfCalMethod', max_length=8, blank=True, null=True)  # Field name made lowercase.
    udfcalrate = models.DecimalField(db_column='UdfCalRate', max_digits=2, decimal_places=2, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'crewdtl'


class Crewrate(models.Model):
    crewrateguid = models.CharField(db_column='CrewRateGuid', primary_key=True, max_length=32)  # Field name made lowercase.
    crewname = models.CharField(db_column='CrewName', max_length=88, blank=True, null=True)  # Field name made lowercase.
    isactive = models.CharField(db_column='IsActive', max_length=1)  # Field name made lowercase.
    crewid = models.CharField(db_column='CrewId', unique=True, max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'crewrate'


class Crewratedtl(models.Model):
    crewratedtlguid = models.CharField(db_column='CrewRateDtlGuid', primary_key=True, max_length=32)  # Field name made lowercase.
    crewtype = models.CharField(db_column='CrewType', max_length=50, blank=True, null=True)  # Field name made lowercase.
    commvalue = models.DecimalField(db_column='CommValue', max_digits=8, decimal_places=7, blank=True, null=True)  # Field name made lowercase.
    commissionitemclassguid = models.ForeignKey(Commissionitemclass, models.DO_NOTHING, db_column='CommissionItemClassGuid')  # Field name made lowercase.
    crewrateguid = models.ForeignKey(Crewrate, models.DO_NOTHING, db_column='CrewRateGuid')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'crewratedtl'


class Debtor(models.Model):
    autokey = models.CharField(db_column='Autokey', primary_key=True, max_length=32)  # Field name made lowercase.
    accno = models.CharField(db_column='AccNo', unique=True, max_length=40)  # Field name made lowercase.
    companyname = models.CharField(db_column='CompanyName', max_length=100, blank=True, null=True)  # Field name made lowercase.
    desc2 = models.CharField(db_column='Desc2', max_length=100, blank=True, null=True)  # Field name made lowercase.
    registorno = models.CharField(db_column='RegistorNo', max_length=30, blank=True, null=True)  # Field name made lowercase.
    address1 = models.CharField(db_column='Address1', max_length=40, blank=True, null=True)  # Field name made lowercase.
    address2 = models.CharField(db_column='Address2', max_length=40, blank=True, null=True)  # Field name made lowercase.
    address3 = models.CharField(db_column='Address3', max_length=40, blank=True, null=True)  # Field name made lowercase.
    address4 = models.CharField(db_column='Address4', max_length=40, blank=True, null=True)  # Field name made lowercase.
    postcode = models.CharField(db_column='PostCode', max_length=10, blank=True, null=True)  # Field name made lowercase.
    deliveraddr1 = models.CharField(db_column='DeliverAddr1', max_length=40, blank=True, null=True)  # Field name made lowercase.
    deliveraddr2 = models.CharField(db_column='DeliverAddr2', max_length=40, blank=True, null=True)  # Field name made lowercase.
    deliveraddr3 = models.CharField(db_column='DeliverAddr3', max_length=40, blank=True, null=True)  # Field name made lowercase.
    deliveraddr4 = models.CharField(db_column='DeliverAddr4', max_length=40, blank=True, null=True)  # Field name made lowercase.
    deliverpostcode = models.CharField(db_column='DeliverPostCode', max_length=10, blank=True, null=True)  # Field name made lowercase.
    attention = models.CharField(db_column='Attention', max_length=40, blank=True, null=True)  # Field name made lowercase.
    phone1 = models.CharField(db_column='Phone1', max_length=25, blank=True, null=True)  # Field name made lowercase.
    phone2 = models.CharField(db_column='Phone2', max_length=25, blank=True, null=True)  # Field name made lowercase.
    fax1 = models.CharField(db_column='Fax1', max_length=25, blank=True, null=True)  # Field name made lowercase.
    fax2 = models.CharField(db_column='Fax2', max_length=25, blank=True, null=True)  # Field name made lowercase.
    areacode = models.CharField(db_column='AreaCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    salesagent = models.CharField(db_column='SalesAgent', max_length=12, blank=True, null=True)  # Field name made lowercase.
    debtortype = models.CharField(db_column='DebtorType', max_length=20, blank=True, null=True)  # Field name made lowercase.
    natureofbusiness = models.CharField(db_column='NatureOfBusiness', max_length=40, blank=True, null=True)  # Field name made lowercase.
    weburl = models.CharField(db_column='WebURL', max_length=80, blank=True, null=True)  # Field name made lowercase.
    emailaddress = models.CharField(db_column='EmailAddress', max_length=200, blank=True, null=True)  # Field name made lowercase.
    displayterm = models.ForeignKey('Terms', models.DO_NOTHING, db_column='DisplayTerm')  # Field name made lowercase.
    creditlimit = models.DecimalField(db_column='CreditLimit', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    agingon = models.CharField(db_column='AgingOn', max_length=1, blank=True, null=True)  # Field name made lowercase.
    statementtype = models.CharField(db_column='StatementType', max_length=1, blank=True, null=True)  # Field name made lowercase.
    currencycode = models.CharField(db_column='CurrencyCode', max_length=5)  # Field name made lowercase.
    allowexceedcreditlimit = models.CharField(db_column='AllowExceedCreditLimit', max_length=5)  # Field name made lowercase.
    note = models.CharField(db_column='Note', max_length=255, blank=True, null=True)  # Field name made lowercase.
    exemptno = models.CharField(db_column='ExemptNo', max_length=60, blank=True, null=True)  # Field name made lowercase.
    expirydate = models.DateTimeField(db_column='ExpiryDate', blank=True, null=True)  # Field name made lowercase.
    pricecategory = models.CharField(db_column='PriceCategory', max_length=12, blank=True, null=True)  # Field name made lowercase.
    taxtype = models.CharField(db_column='TaxType', max_length=14, blank=True, null=True)  # Field name made lowercase.
    discountpercent = models.DecimalField(db_column='DiscountPercent', max_digits=18, decimal_places=6)  # Field name made lowercase.
    detaildiscount = models.CharField(db_column='DetailDiscount', max_length=20, blank=True, null=True)  # Field name made lowercase.
    lastmodified = models.DateTimeField(db_column='LastModified')  # Field name made lowercase.
    lastmodifieduserid = models.CharField(db_column='LastModifiedUserID', max_length=10)  # Field name made lowercase.
    createduserid = models.CharField(db_column='CreatedUserID', max_length=30)  # Field name made lowercase.
    overduelimit = models.DecimalField(db_column='OverdueLimit', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    hasbonuspoint = models.CharField(db_column='HasBonusPoint', max_length=1)  # Field name made lowercase.
    openingbonuspoint = models.DecimalField(db_column='OpeningBonuspoint', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    otblockstatus = models.SmallIntegerField(db_column='OTBlockStatus', blank=True, null=True)  # Field name made lowercase.
    soblockstatus = models.SmallIntegerField(db_column='SOBlockStatus', blank=True, null=True)  # Field name made lowercase.
    doblockstatus = models.SmallIntegerField(db_column='DOBlockStatus', blank=True, null=True)  # Field name made lowercase.
    ivblockstatus = models.SmallIntegerField(db_column='IVBlockStatus', blank=True, null=True)  # Field name made lowercase.
    csblockstatus = models.SmallIntegerField(db_column='CSBlockStatus', blank=True, null=True)  # Field name made lowercase.
    qtblockmessage = models.SmallIntegerField(db_column='QTBlockMessage', blank=True, null=True)  # Field name made lowercase.
    soblockmessage = models.SmallIntegerField(db_column='SOBlockMessage', blank=True, null=True)  # Field name made lowercase.
    doblockmessage = models.SmallIntegerField(db_column='DOBlockMessage', blank=True, null=True)  # Field name made lowercase.
    ivblockmessage = models.SmallIntegerField(db_column='IVBlockMessage', blank=True, null=True)  # Field name made lowercase.
    csblockmessage = models.SmallIntegerField(db_column='CSBlockMessage', blank=True, null=True)  # Field name made lowercase.
    externallink = models.CharField(db_column='ExternalLink', max_length=255, blank=True, null=True)  # Field name made lowercase.
    isgroupcompany = models.CharField(db_column='IsGroupCompany', max_length=1)  # Field name made lowercase.
    isactive = models.CharField(db_column='IsActive', max_length=1)  # Field name made lowercase.
    lastupdate = models.IntegerField(db_column='LastUpdate')  # Field name made lowercase.
    contactinfo = models.CharField(db_column='ContactInfo', max_length=255, blank=True, null=True)  # Field name made lowercase.
    accountgroup = models.CharField(db_column='AccountGroup', max_length=12, blank=True, null=True)  # Field name made lowercase.
    markupratio = models.DecimalField(db_column='MarkupRatio', max_digits=18, decimal_places=6, blank=True, null=True)  # Field name made lowercase.
    taxregisterno = models.CharField(db_column='TaxRegisterNo', max_length=20, blank=True, null=True)  # Field name made lowercase.
    calcdiscountonunitprice = models.CharField(db_column='CalcDiscountOnUnitPrice', max_length=1, blank=True, null=True)  # Field name made lowercase.
    gststatusverifieddate = models.DateTimeField(db_column='GSTStatusVerifiedDate', blank=True, null=True)  # Field name made lowercase.
    inclusivetax = models.CharField(db_column='InclusiveTax', max_length=1)  # Field name made lowercase.
    roundingmethod = models.IntegerField(db_column='RoundingMethod')  # Field name made lowercase.
    selfbilledapprovalno = models.CharField(db_column='SelfBilledApprovalNo', max_length=1)  # Field name made lowercase.
    guid = models.CharField(db_column='Guid', unique=True, max_length=32)  # Field name made lowercase.
    istaxregistered = models.CharField(db_column='IsTaxRegistered', max_length=5, blank=True, null=True)  # Field name made lowercase.
    receiptwithholdingtaxcode = models.CharField(db_column='ReceiptWithHoldingTaxCode', max_length=14, blank=True, null=True)  # Field name made lowercase.
    paymentwithholdingtaxcode = models.CharField(db_column='PaymentWithHoldingTaxCode', max_length=14, blank=True, null=True)  # Field name made lowercase.
    multiprice = models.CharField(db_column='MultiPrice', max_length=8, blank=True, null=True)  # Field name made lowercase.
    allowchangemultiprice = models.CharField(db_column='AllowChangeMultiPrice', max_length=1, blank=True, null=True)  # Field name made lowercase.
    taxbranchid = models.CharField(db_column='TaxBranchID', max_length=8, blank=True, null=True)  # Field name made lowercase.
    servicetaxregisterno = models.CharField(db_column='ServiceTaxRegisterNo', max_length=20, blank=True, null=True)  # Field name made lowercase.
    mobile = models.CharField(db_column='Mobile', max_length=25, blank=True, null=True)  # Field name made lowercase.
    cgblockstatus = models.SmallIntegerField(db_column='CGBlockStatus', blank=True, null=True)  # Field name made lowercase.
    cgblockmessage = models.CharField(db_column='CGBlockMessage', max_length=40, blank=True, null=True)  # Field name made lowercase.
    companyautokey = models.ForeignKey(Company, models.DO_NOTHING, db_column='CompanyAutoKey')  # Field name made lowercase.
    autocountacccode = models.CharField(db_column='autoCountAccCode', max_length=20, blank=True, null=True)  # Field name made lowercase.
    udfispallet = models.SmallIntegerField(db_column='UdfIsPallet', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'debtor'


class Debtortype(models.Model):
    autokey = models.CharField(db_column='Autokey', primary_key=True, max_length=32)  # Field name made lowercase.
    debtortype = models.CharField(db_column='DebtorType', max_length=20)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=40, blank=True, null=True)  # Field name made lowercase.
    desc2 = models.CharField(db_column='Desc2', max_length=40, blank=True, null=True)  # Field name made lowercase.
    isactive = models.CharField(db_column='IsActive', max_length=1)  # Field name made lowercase.
    lastupdate = models.IntegerField(db_column='LastUpdate')  # Field name made lowercase.
    guid = models.CharField(db_column='Guid', max_length=32, blank=True, null=True)  # Field name made lowercase.
    companyautokey = models.ForeignKey(Company, models.DO_NOTHING, db_column='CompanyAutoKey')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'debtortype'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Dn(models.Model):
    autokey = models.CharField(db_column='Autokey', primary_key=True, max_length=32)  # Field name made lowercase.
    docno = models.CharField(db_column='DocNo', max_length=20)  # Field name made lowercase.
    docdate = models.DateTimeField(db_column='DocDate')  # Field name made lowercase.
    debtorcode = models.CharField(db_column='DebtorCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    debtorname = models.CharField(db_column='DebtorName', max_length=100, blank=True, null=True)  # Field name made lowercase.
    dntype = models.CharField(db_column='DNType', max_length=12, blank=True, null=True)  # Field name made lowercase.
    ref = models.CharField(db_column='Ref', max_length=40, blank=True, null=True)  # Field name made lowercase.
    ourinvoiceno = models.CharField(db_column='OurInvoiceNo', max_length=40, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=80, blank=True, null=True)  # Field name made lowercase.
    salesagent = models.CharField(db_column='SalesAgent', max_length=12, blank=True, null=True)  # Field name made lowercase.
    invaddr1 = models.CharField(db_column='InvAddr1', max_length=40, blank=True, null=True)  # Field name made lowercase.
    invaddr2 = models.CharField(db_column='InvAddr2', max_length=40, blank=True, null=True)  # Field name made lowercase.
    invaddr3 = models.CharField(db_column='InvAddr3', max_length=40, blank=True, null=True)  # Field name made lowercase.
    invaddr4 = models.CharField(db_column='InvAddr4', max_length=40, blank=True, null=True)  # Field name made lowercase.
    phone1 = models.CharField(db_column='Phone1', max_length=25, blank=True, null=True)  # Field name made lowercase.
    fax1 = models.CharField(db_column='Fax1', max_length=25, blank=True, null=True)  # Field name made lowercase.
    attention = models.CharField(db_column='Attention', max_length=40, blank=True, null=True)  # Field name made lowercase.
    branchcode = models.CharField(db_column='BranchCode', max_length=20, blank=True, null=True)  # Field name made lowercase.
    deliveraddr1 = models.CharField(db_column='DeliverAddr1', max_length=40, blank=True, null=True)  # Field name made lowercase.
    deliveraddr2 = models.CharField(db_column='DeliverAddr2', max_length=40, blank=True, null=True)  # Field name made lowercase.
    deliveraddr3 = models.CharField(db_column='DeliverAddr3', max_length=40, blank=True, null=True)  # Field name made lowercase.
    deliveraddr4 = models.CharField(db_column='DeliverAddr4', max_length=40, blank=True, null=True)  # Field name made lowercase.
    deliverphone1 = models.CharField(db_column='DeliverPhone1', max_length=25, blank=True, null=True)  # Field name made lowercase.
    deliverfax1 = models.CharField(db_column='DeliverFax1', max_length=25, blank=True, null=True)  # Field name made lowercase.
    delivercontact = models.CharField(db_column='DeliverContact', max_length=40, blank=True, null=True)  # Field name made lowercase.
    salesexemptionno = models.CharField(db_column='SalesExemptionNo', max_length=60, blank=True, null=True)  # Field name made lowercase.
    salesexemptionexpirydate = models.DateTimeField(db_column='SalesExemptionExpiryDate', blank=True, null=True)  # Field name made lowercase.
    total = models.DecimalField(db_column='Total', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer1param = models.DecimalField(db_column='Footer1Param', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer1amt = models.DecimalField(db_column='Footer1Amt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer1localamt = models.DecimalField(db_column='Footer1LocalAmt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer1taxtype = models.CharField(db_column='Footer1TaxType', max_length=14, blank=True, null=True)  # Field name made lowercase.
    footer2param = models.DecimalField(db_column='Footer2Param', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer2amt = models.DecimalField(db_column='Footer2Amt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer2localamt = models.DecimalField(db_column='Footer2LocalAmt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer2taxtype = models.CharField(db_column='Footer2TaxType', max_length=14, blank=True, null=True)  # Field name made lowercase.
    footer3param = models.DecimalField(db_column='Footer3Param', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer3amt = models.DecimalField(db_column='Footer3Amt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer3localamt = models.DecimalField(db_column='Footer3LocalAmt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer3taxtype = models.CharField(db_column='Footer3TaxType', max_length=14, blank=True, null=True)  # Field name made lowercase.
    currencycode = models.CharField(db_column='CurrencyCode', max_length=5)  # Field name made lowercase.
    currencyrate = models.DecimalField(db_column='CurrencyRate', max_digits=19, decimal_places=2)  # Field name made lowercase.
    nettotal = models.DecimalField(db_column='NetTotal', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    localnettotal = models.DecimalField(db_column='LocalNetTotal', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    analysisnettotal = models.DecimalField(db_column='AnalysisNetTotal', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    localanalysisnettotal = models.DecimalField(db_column='LocalAnalysisNetTotal', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    localtotalcost = models.DecimalField(db_column='LocalTotalCost', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    tax = models.DecimalField(db_column='Tax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    localtax = models.DecimalField(db_column='LocalTax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    totalbonuspoint = models.DecimalField(db_column='TotalBonusPoint', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    posttostock = models.CharField(db_column='PostToStock', max_length=1)  # Field name made lowercase.
    posttogl = models.CharField(db_column='PostToGL', max_length=1)  # Field name made lowercase.
    referdockey = models.BigIntegerField(db_column='ReferDocKey', blank=True, null=True)  # Field name made lowercase.
    note = models.CharField(db_column='Note', max_length=255, blank=True, null=True)  # Field name made lowercase.
    remark1 = models.CharField(db_column='Remark1', max_length=40, blank=True, null=True)  # Field name made lowercase.
    remark2 = models.CharField(db_column='Remark2', max_length=40, blank=True, null=True)  # Field name made lowercase.
    remark3 = models.CharField(db_column='Remark3', max_length=40, blank=True, null=True)  # Field name made lowercase.
    remark4 = models.CharField(db_column='Remark4', max_length=40, blank=True, null=True)  # Field name made lowercase.
    printcount = models.SmallIntegerField(db_column='PrintCount')  # Field name made lowercase.
    cancelled = models.CharField(db_column='Cancelled', max_length=1)  # Field name made lowercase.
    lastmodified = models.DateTimeField(db_column='LastModified')  # Field name made lowercase.
    lastmodifieduserid = models.CharField(db_column='LastModifiedUserID', max_length=10)  # Field name made lowercase.
    createdtimestamp = models.DateTimeField(db_column='CreatedTimeStamp')  # Field name made lowercase.
    createduserid = models.CharField(db_column='CreatedUserID', max_length=10)  # Field name made lowercase.
    externallink = models.CharField(db_column='ExternalLink', max_length=255, blank=True, null=True)  # Field name made lowercase.
    refdocno = models.CharField(db_column='RefDocNo', max_length=20, blank=True, null=True)  # Field name made lowercase.
    cansync = models.CharField(db_column='CanSync', max_length=1)  # Field name made lowercase.
    lastupdate = models.IntegerField(db_column='LastUpdate')  # Field name made lowercase.
    memberno = models.CharField(db_column='MemberNo', max_length=20, blank=True, null=True)  # Field name made lowercase.
    reallocatepurchasebyproject = models.CharField(db_column='ReallocatePurchaseByProject', max_length=1)  # Field name made lowercase.
    reallocatepurchasebyprojectjedockey = models.BigIntegerField(db_column='ReallocatePurchaseByProjectJEDocKey', blank=True, null=True)  # Field name made lowercase.
    refno2 = models.CharField(db_column='RefNo2', max_length=20, blank=True, null=True)  # Field name made lowercase.
    saleslocation = models.CharField(db_column='SalesLocation', max_length=8, blank=True, null=True)  # Field name made lowercase.
    footer1tax = models.DecimalField(db_column='Footer1Tax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer1localtax = models.DecimalField(db_column='Footer1LocalTax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer2tax = models.DecimalField(db_column='Footer2Tax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer2localtax = models.DecimalField(db_column='Footer2LocalTax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer3tax = models.DecimalField(db_column='Footer3Tax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer3localtax = models.DecimalField(db_column='Footer3LocalTax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    extax = models.DecimalField(db_column='ExTax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    localextax = models.DecimalField(db_column='LocalExTax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    yourpono = models.CharField(db_column='YourPONo', max_length=25, blank=True, null=True)  # Field name made lowercase.
    yourpodate = models.DateTimeField(db_column='YourPODate', blank=True, null=True)  # Field name made lowercase.
    guid = models.CharField(db_column='Guid', unique=True, max_length=32)  # Field name made lowercase.
    reallocatepurchasebyprojectno = models.CharField(db_column='ReallocatePurchaseByProjectNo', max_length=10, blank=True, null=True)  # Field name made lowercase.
    totaxcurrencyrate = models.DecimalField(db_column='ToTaxCurrencyRate', max_digits=19, decimal_places=2)  # Field name made lowercase.
    calcdiscountonunitprice = models.CharField(db_column='CalcDiscountOnUnitPrice', max_length=1, blank=True, null=True)  # Field name made lowercase.
    taxdocno = models.CharField(db_column='TaxDocNo', max_length=20, blank=True, null=True)  # Field name made lowercase.
    totalextax = models.DecimalField(db_column='TotalExTax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    taxableamt = models.DecimalField(db_column='TaxableAmt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    reason = models.CharField(db_column='Reason', max_length=80, blank=True, null=True)  # Field name made lowercase.
    inclusivetax = models.CharField(db_column='InclusiveTax', max_length=1)  # Field name made lowercase.
    footer1taxrate = models.DecimalField(db_column='Footer1TaxRate', max_digits=18, decimal_places=6, blank=True, null=True)  # Field name made lowercase.
    footer2taxrate = models.DecimalField(db_column='Footer2TaxRate', max_digits=18, decimal_places=6, blank=True, null=True)  # Field name made lowercase.
    footer3taxrate = models.DecimalField(db_column='Footer3TaxRate', max_digits=18, decimal_places=6, blank=True, null=True)  # Field name made lowercase.
    taxdate = models.DateTimeField(db_column='TaxDate', blank=True, null=True)  # Field name made lowercase.
    roundingmethod = models.IntegerField(db_column='RoundingMethod')  # Field name made lowercase.
    localtaxableamt = models.DecimalField(db_column='LocalTaxableAmt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    taxcurrencytax = models.DecimalField(db_column='TaxCurrencyTax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    taxcurrencytaxableamt = models.DecimalField(db_column='TaxCurrencyTaxableAmt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    multiprice = models.CharField(db_column='MultiPrice', max_length=8, blank=True, null=True)  # Field name made lowercase.
    taxbranchid = models.CharField(db_column='TaxBranchID', max_length=8, blank=True, null=True)  # Field name made lowercase.
    branchautokey = models.ForeignKey(Branch, models.DO_NOTHING, db_column='BranchAutoKey')  # Field name made lowercase.
    displayterm = models.ForeignKey('Terms', models.DO_NOTHING, db_column='DisplayTerm')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'dn'


class Dndtl(models.Model):
    autokey = models.CharField(db_column='Autokey', primary_key=True, max_length=32)  # Field name made lowercase.
    focdtlkey = models.BigIntegerField(db_column='FOCDtlKey', blank=True, null=True)  # Field name made lowercase.
    seq = models.IntegerField(db_column='Seq')  # Field name made lowercase.
    indent = models.SmallIntegerField(db_column='Indent', blank=True, null=True)  # Field name made lowercase.
    fontstyle = models.CharField(db_column='FontStyle', max_length=8, blank=True, null=True)  # Field name made lowercase.
    mainitem = models.CharField(db_column='MainItem', max_length=1)  # Field name made lowercase.
    numbering = models.CharField(db_column='Numbering', max_length=6, blank=True, null=True)  # Field name made lowercase.
    batchno = models.CharField(db_column='BatchNo', max_length=20, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=100, blank=True, null=True)  # Field name made lowercase.
    furtherdescription = models.CharField(db_column='FurtherDescription', max_length=255, blank=True, null=True)  # Field name made lowercase.
    posttostockdate = models.DateTimeField(db_column='PostToStockDate', blank=True, null=True)  # Field name made lowercase.
    projno = models.CharField(db_column='ProjNo', max_length=10, blank=True, null=True)  # Field name made lowercase.
    deptno = models.CharField(db_column='DeptNo', max_length=10, blank=True, null=True)  # Field name made lowercase.
    uom = models.CharField(db_column='UOM', max_length=8, blank=True, null=True)  # Field name made lowercase.
    useruom = models.CharField(db_column='UserUOM', max_length=8, blank=True, null=True)  # Field name made lowercase.
    qty = models.DecimalField(db_column='Qty', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    rate = models.DecimalField(db_column='Rate', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    smallestqty = models.DecimalField(db_column='SmallestQty', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    focqty = models.DecimalField(db_column='FOCQty', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    smallestunitprice = models.DecimalField(db_column='SmallestUnitPrice', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    unitprice = models.DecimalField(db_column='UnitPrice', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    discount = models.CharField(db_column='Discount', max_length=20, blank=True, null=True)  # Field name made lowercase.
    discountamt = models.DecimalField(db_column='DiscountAmt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    taxtype = models.CharField(db_column='TaxType', max_length=14, blank=True, null=True)  # Field name made lowercase.
    tax = models.DecimalField(db_column='Tax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    subtotal = models.DecimalField(db_column='SubTotal', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    localsubtotal = models.DecimalField(db_column='LocalSubTotal', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    localtotalcost = models.DecimalField(db_column='LocalTotalCost', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    localfoctotalcost = models.DecimalField(db_column='LocalFOCTotalCost', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    bonuspoint = models.DecimalField(db_column='BonusPoint', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    printout = models.CharField(db_column='PrintOut', max_length=1)  # Field name made lowercase.
    dtltype = models.CharField(db_column='DtlType', max_length=1, blank=True, null=True)  # Field name made lowercase.
    calcbypercent = models.DecimalField(db_column='CalcByPercent', max_digits=18, decimal_places=6, blank=True, null=True)  # Field name made lowercase.
    addtosubtotal = models.CharField(db_column='AddToSubTotal', max_length=1)  # Field name made lowercase.
    accno = models.CharField(db_column='AccNo', max_length=12, blank=True, null=True)  # Field name made lowercase.
    serialnolist = models.CharField(db_column='SerialNoList', max_length=255, blank=True, null=True)  # Field name made lowercase.
    packagedockey = models.BigIntegerField(db_column='PackageDocKey', blank=True, null=True)  # Field name made lowercase.
    packagedtlkey = models.BigIntegerField(db_column='PackageDtlKey', blank=True, null=True)  # Field name made lowercase.
    subqty = models.DecimalField(db_column='SubQty', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    iscalcbonuspoint = models.CharField(db_column='IsCalcBonusPoint', max_length=1, blank=True, null=True)  # Field name made lowercase.
    subtotalextax = models.DecimalField(db_column='SubTotalExTax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    localtax = models.DecimalField(db_column='LocalTax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    yourpono = models.CharField(db_column='YourPONo', max_length=25, blank=True, null=True)  # Field name made lowercase.
    yourpodate = models.DateTimeField(db_column='YourPODate', blank=True, null=True)  # Field name made lowercase.
    guid = models.CharField(db_column='Guid', unique=True, max_length=32)  # Field name made lowercase.
    ruleno = models.BigIntegerField(db_column='RuleNo', blank=True, null=True)  # Field name made lowercase.
    taxableamt = models.DecimalField(db_column='TaxableAmt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    taxadjustment = models.DecimalField(db_column='TaxAdjustment', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    taxexportcountry = models.CharField(db_column='TaxExportCountry', max_length=50, blank=True, null=True)  # Field name made lowercase.
    localsubtotalextax = models.DecimalField(db_column='LocalSubTotalExTax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    extradiscountamt = models.DecimalField(db_column='ExtraDiscountAmt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    taxrate = models.DecimalField(db_column='TaxRate', max_digits=18, decimal_places=6, blank=True, null=True)  # Field name made lowercase.
    localtaxadjustment = models.DecimalField(db_column='LocalTaxAdjustment', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    localtaxableamt = models.DecimalField(db_column='LocalTaxableAmt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    taxcurrencytax = models.DecimalField(db_column='TaxCurrencyTax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    taxcurrencytaxableamt = models.DecimalField(db_column='TaxCurrencyTaxableAmt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    taxpermitno = models.CharField(db_column='TaxPermitNo', max_length=20, blank=True, null=True)  # Field name made lowercase.
    salesexemptionno = models.CharField(db_column='SalesExemptionNo', max_length=60, blank=True, null=True)  # Field name made lowercase.
    supplypurchase = models.CharField(db_column='SupplyPurchase', max_length=1, blank=True, null=True)  # Field name made lowercase.
    tarrifcode = models.CharField(db_column='TarrifCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    desc2 = models.CharField(db_column='Desc2', max_length=100, blank=True, null=True)  # Field name made lowercase.
    dnautokey = models.ForeignKey(Cn, models.DO_NOTHING, db_column='DNAutokey')  # Field name made lowercase.
    itemcode = models.ForeignKey('Item', models.DO_NOTHING, db_column='ItemCode', blank=True, null=True)  # Field name made lowercase.
    location = models.ForeignKey('Location', models.DO_NOTHING, db_column='Location', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'dndtl'


class Gr(models.Model):
    autokey = models.CharField(db_column='AutoKey', primary_key=True, max_length=32)  # Field name made lowercase.
    docno = models.CharField(db_column='DocNo', max_length=20)  # Field name made lowercase.
    docdate = models.DateTimeField(db_column='DocDate')  # Field name made lowercase.
    ref = models.CharField(db_column='Ref', max_length=40, blank=True, null=True)  # Field name made lowercase.
    supplierdono = models.CharField(db_column='SupplierDONo', max_length=20, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=80, blank=True, null=True)  # Field name made lowercase.
    purchaseagent = models.CharField(db_column='PurchaseAgent', max_length=12, blank=True, null=True)  # Field name made lowercase.
    invaddr1 = models.CharField(db_column='InvAddr1', max_length=40, blank=True, null=True)  # Field name made lowercase.
    invaddr2 = models.CharField(db_column='InvAddr2', max_length=40, blank=True, null=True)  # Field name made lowercase.
    invaddr3 = models.CharField(db_column='InvAddr3', max_length=40, blank=True, null=True)  # Field name made lowercase.
    invaddr4 = models.CharField(db_column='InvAddr4', max_length=40, blank=True, null=True)  # Field name made lowercase.
    phone1 = models.CharField(db_column='Phone1', max_length=25, blank=True, null=True)  # Field name made lowercase.
    fax1 = models.CharField(db_column='Fax1', max_length=25, blank=True, null=True)  # Field name made lowercase.
    attention = models.CharField(db_column='Attention', max_length=40, blank=True, null=True)  # Field name made lowercase.
    branchcode = models.CharField(db_column='BranchCode', max_length=20, blank=True, null=True)  # Field name made lowercase.
    total = models.DecimalField(db_column='Total', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer1param = models.DecimalField(db_column='Footer1Param', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer1amt = models.DecimalField(db_column='Footer1Amt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer1localamt = models.DecimalField(db_column='Footer1LocalAmt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer1taxtype = models.CharField(db_column='Footer1TaxType', max_length=14, blank=True, null=True)  # Field name made lowercase.
    footer2param = models.DecimalField(db_column='Footer2Param', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer2amt = models.DecimalField(db_column='Footer2Amt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer2localamt = models.DecimalField(db_column='Footer2LocalAmt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer2taxtype = models.CharField(db_column='Footer2TaxType', max_length=14, blank=True, null=True)  # Field name made lowercase.
    footer3param = models.DecimalField(db_column='Footer3Param', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer3amt = models.DecimalField(db_column='Footer3Amt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer3localamt = models.DecimalField(db_column='Footer3LocalAmt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer3taxtype = models.CharField(db_column='Footer3TaxType', max_length=14, blank=True, null=True)  # Field name made lowercase.
    crrencycode = models.CharField(db_column='CrrencyCode', max_length=5)  # Field name made lowercase.
    currencyrate = models.DecimalField(db_column='CurrencyRate', max_digits=19, decimal_places=2)  # Field name made lowercase.
    nettotal = models.DecimalField(db_column='NetTotal', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    localnettotal = models.DecimalField(db_column='LocalNetTotal', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    tax = models.DecimalField(db_column='Tax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    localtax = models.DecimalField(db_column='LocalTax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    foreigncharges = models.DecimalField(db_column='ForeignCharges', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    localcharges = models.DecimalField(db_column='LocalCharges', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    landedcostmethod = models.CharField(db_column='LandedCostMethod', max_length=1, blank=True, null=True)  # Field name made lowercase.
    posttostock = models.CharField(db_column='PostToStock', max_length=1)  # Field name made lowercase.
    transferable = models.CharField(db_column='Transferable', max_length=1)  # Field name made lowercase.
    todoctype = models.CharField(db_column='ToDocType', max_length=2, blank=True, null=True)  # Field name made lowercase.
    todockey = models.BigIntegerField(db_column='ToDocKey', blank=True, null=True)  # Field name made lowercase.
    note = models.CharField(db_column='Note', max_length=255, blank=True, null=True)  # Field name made lowercase.
    remark1 = models.CharField(db_column='Remark1', max_length=40, blank=True, null=True)  # Field name made lowercase.
    remark2 = models.CharField(db_column='Remark2', max_length=40, blank=True, null=True)  # Field name made lowercase.
    remark3 = models.CharField(db_column='Remark3', max_length=40, blank=True, null=True)  # Field name made lowercase.
    remark4 = models.CharField(db_column='Remark4', max_length=40, blank=True, null=True)  # Field name made lowercase.
    printcount = models.SmallIntegerField(db_column='PrintCount')  # Field name made lowercase.
    cancelled = models.CharField(db_column='Cancelled', max_length=1)  # Field name made lowercase.
    lastmodified = models.DateTimeField(db_column='LastModified')  # Field name made lowercase.
    lastmodifieduserid = models.CharField(db_column='LastModifiedUserID', max_length=10)  # Field name made lowercase.
    createdtimestamp = models.DateTimeField(db_column='CreatedTimeStamp')  # Field name made lowercase.
    createduserid = models.CharField(db_column='CreatedUserID', max_length=10)  # Field name made lowercase.
    externallink = models.CharField(db_column='ExternalLink', max_length=255, blank=True, null=True)  # Field name made lowercase.
    refdocno = models.CharField(db_column='RefDocNo', max_length=20, blank=True, null=True)  # Field name made lowercase.
    cansync = models.CharField(db_column='CanSync', max_length=1)  # Field name made lowercase.
    lastupdate = models.IntegerField(db_column='LastUpdate')  # Field name made lowercase.
    todtlkey = models.BigIntegerField(db_column='ToDtlKey', blank=True, null=True)  # Field name made lowercase.
    fulltransferoption = models.CharField(db_column='FullTransferOption', max_length=1, blank=True, null=True)  # Field name made lowercase.
    shipvia = models.CharField(db_column='ShipVia', max_length=20, blank=True, null=True)  # Field name made lowercase.
    shipinfo = models.CharField(db_column='ShipInfo', max_length=40, blank=True, null=True)  # Field name made lowercase.
    purchaselocation = models.CharField(db_column='PurchaseLocation', max_length=8, blank=True, null=True)  # Field name made lowercase.
    footer1tax = models.DecimalField(db_column='Footer1Tax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer1localtax = models.DecimalField(db_column='Footer1LocalTax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer2tax = models.DecimalField(db_column='Footer2Tax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer2localtax = models.DecimalField(db_column='Footer2LocalTax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer3tax = models.DecimalField(db_column='Footer3Tax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer3localtax = models.DecimalField(db_column='Footer3LocalTax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    extax = models.DecimalField(db_column='ExTax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    localextax = models.DecimalField(db_column='LocalExTax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    analysisnettotal = models.DecimalField(db_column='AnalysisNetTotal', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    localanalysisnettotal = models.DecimalField(db_column='LocalAnalysisNetTotal', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    guid = models.CharField(db_column='Guid', unique=True, max_length=32)  # Field name made lowercase.
    totaxcurrencyrate = models.DecimalField(db_column='ToTaxCurrencyRate', max_digits=19, decimal_places=2)  # Field name made lowercase.
    calcdiscountonunitprice = models.CharField(db_column='CalcDiscountOnUnitPrice', max_length=1, blank=True, null=True)  # Field name made lowercase.
    totalextax = models.DecimalField(db_column='TotalExTax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    taxableamt = models.DecimalField(db_column='TaxableAmt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    inclusivetax = models.CharField(db_column='InclusiveTax', max_length=1)  # Field name made lowercase.
    footer1taxrate = models.DecimalField(db_column='Footer1TaxRate', max_digits=18, decimal_places=6, blank=True, null=True)  # Field name made lowercase.
    footer2taxrate = models.DecimalField(db_column='Footer2TaxRate', max_digits=18, decimal_places=6, blank=True, null=True)  # Field name made lowercase.
    footer3taxrate = models.DecimalField(db_column='Footer3TaxRate', max_digits=18, decimal_places=6, blank=True, null=True)  # Field name made lowercase.
    roundingmethod = models.IntegerField(db_column='RoundingMethod')  # Field name made lowercase.
    localtaxableamt = models.DecimalField(db_column='LocalTaxableAmt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    taxcurrencytax = models.DecimalField(db_column='TaxCurrencyTax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    taxcurrencytaxableamt = models.DecimalField(db_column='TaxCurrencyTaxableAmt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    taxbranchid = models.CharField(db_column='TaxBranchID', max_length=8, blank=True, null=True)  # Field name made lowercase.
    branchautokey = models.ForeignKey(Branch, models.DO_NOTHING, db_column='BranchAutoKey')  # Field name made lowercase.
    creditorcode = models.ForeignKey(Creditor, models.DO_NOTHING, db_column='CreditorCode', to_field='AccNo')  # Field name made lowercase.
    creditorname = models.ForeignKey(Creditor, models.DO_NOTHING, db_column='CreditorName', to_field='CompanyName', related_name='gr_creditorname_set')  # Field name made lowercase.
    displayterm = models.ForeignKey('Terms', models.DO_NOTHING, db_column='DisplayTerm', to_field='DisplayTerm')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'gr'


class Grdtl(models.Model):
    autokey = models.CharField(db_column='AutoKey', primary_key=True, max_length=32)  # Field name made lowercase.
    focdtlkey = models.BigIntegerField(db_column='FOCDtlKey', blank=True, null=True)  # Field name made lowercase.
    seq = models.IntegerField(db_column='Seq')  # Field name made lowercase.
    indent = models.SmallIntegerField(db_column='Indent', blank=True, null=True)  # Field name made lowercase.
    fontstyle = models.CharField(db_column='FontStyle', max_length=8, blank=True, null=True)  # Field name made lowercase.
    mainitem = models.CharField(db_column='Mainitem', max_length=5)  # Field name made lowercase.
    numbering = models.CharField(db_column='Numbering', max_length=6, blank=True, null=True)  # Field name made lowercase.
    batchno = models.CharField(db_column='BatchNo', max_length=20, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=100, blank=True, null=True)  # Field name made lowercase.
    furtherdescription = models.CharField(db_column='FurtherDescription', max_length=255, blank=True, null=True)  # Field name made lowercase.
    projno = models.CharField(db_column='ProjNo', max_length=10, blank=True, null=True)  # Field name made lowercase.
    deptno = models.CharField(db_column='DeptNo', max_length=10, blank=True, null=True)  # Field name made lowercase.
    ourpono = models.CharField(db_column='OurPONo', max_length=20, blank=True, null=True)  # Field name made lowercase.
    ourpodate = models.DateTimeField(db_column='OurPODate', blank=True, null=True)  # Field name made lowercase.
    posttostockdate = models.DateTimeField(db_column='PostToStockDate', blank=True, null=True)  # Field name made lowercase.
    uom = models.CharField(db_column='UOM', max_length=8, blank=True, null=True)  # Field name made lowercase.
    useruom = models.CharField(db_column='UserUOM', max_length=8, blank=True, null=True)  # Field name made lowercase.
    qty = models.DecimalField(db_column='Qty', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    rate = models.DecimalField(db_column='Rate', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    smallestqty = models.DecimalField(db_column='SmallestQty', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    transferedqty = models.DecimalField(db_column='TransferedQty', max_digits=25, decimal_places=8)  # Field name made lowercase.
    focqty = models.DecimalField(db_column='FOCQty', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    foctransferedqty = models.DecimalField(db_column='FOCTransferedQty', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    smallestunitprice = models.DecimalField(db_column='SmallestUnitPrice', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    unitprice = models.DecimalField(db_column='UnitPrice', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    discount = models.CharField(db_column='Discount', max_length=20, blank=True, null=True)  # Field name made lowercase.
    discountamt = models.DecimalField(db_column='DiscountAmt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    taxtype = models.CharField(db_column='TaxType', max_length=14, blank=True, null=True)  # Field name made lowercase.
    tax = models.DecimalField(db_column='Tax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    subtotal = models.DecimalField(db_column='SubTotal', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    localsubtotal = models.DecimalField(db_column='LocalSubTotal', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    transferable = models.CharField(db_column='Transferable', max_length=1)  # Field name made lowercase.
    printout = models.CharField(db_column='PrintOut', max_length=1)  # Field name made lowercase.
    dtltype = models.CharField(db_column='DTLType', max_length=1, blank=True, null=True)  # Field name made lowercase.
    calcbypercent = models.DecimalField(db_column='CalcByPercent', max_digits=18, decimal_places=6, blank=True, null=True)  # Field name made lowercase.
    addtosubtotal = models.CharField(db_column='AddToSubTotal', max_length=1)  # Field name made lowercase.
    fromdoctype = models.CharField(db_column='FromDocType', max_length=2, blank=True, null=True)  # Field name made lowercase.
    fromdocno = models.CharField(db_column='FromDocNo', max_length=255, blank=True, null=True)  # Field name made lowercase.
    fromdocdtlkey = models.BigIntegerField(db_column='FromDocDtlKey', blank=True, null=True)  # Field name made lowercase.
    fulltransferoption = models.CharField(db_column='FullTransferOption', max_length=1, blank=True, null=True)  # Field name made lowercase.
    foreigncharges = models.DecimalField(db_column='ForeignCharges', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    localcharges = models.DecimalField(db_column='LocalCharges', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    duty = models.DecimalField(db_column='Duty', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    accno = models.CharField(db_column='AccNo', max_length=12, blank=True, null=True)  # Field name made lowercase.
    fulltransferfromdoclist = models.CharField(db_column='FullTransferFromDocList', max_length=255, blank=True, null=True)  # Field name made lowercase.
    serialnolist = models.CharField(db_column='SerialNoList', max_length=255, blank=True, null=True)  # Field name made lowercase.
    estimateddeliverydate = models.CharField(db_column='EstimatedDeliveryDate', max_length=20, blank=True, null=True)  # Field name made lowercase.
    packagedockey = models.BigIntegerField(db_column='PackageDocKey', blank=True, null=True)  # Field name made lowercase.
    parentdtlkey = models.BigIntegerField(db_column='ParentDtlKey', blank=True, null=True)  # Field name made lowercase.
    subqty = models.DecimalField(db_column='SubQty', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    subtotalextax = models.DecimalField(db_column='SubTotalExTax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    localtax = models.DecimalField(db_column='LocalTax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    guid = models.CharField(db_column='Guid', unique=True, max_length=32)  # Field name made lowercase.
    deliverydate = models.DateTimeField(db_column='DeliveryDate', blank=True, null=True)  # Field name made lowercase.
    cnamt = models.DecimalField(db_column='CNAmt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    taxpermitno = models.CharField(db_column='TaxPermitNo', max_length=20, blank=True, null=True)  # Field name made lowercase.
    taxableamt = models.DecimalField(db_column='TaxableAmt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    taxadjustment = models.DecimalField(db_column='TaxAdjustment', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    localsubtotalextax = models.DecimalField(db_column='LocalSubTotalExTax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    extradiscountamt = models.DecimalField(db_column='ExtraDiscountAmt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    taxrate = models.DecimalField(db_column='TaxRate', max_digits=18, decimal_places=6, blank=True, null=True)  # Field name made lowercase.
    localtaxadjustment = models.DecimalField(db_column='LocalTaxAdjustment', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    localtaxableamt = models.DecimalField(db_column='LocalTaxableAmt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    taxcurrencytax = models.DecimalField(db_column='TaxCurrencyTax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    taxcurrencytaxableamt = models.DecimalField(db_column='TaxCurrencyTaxableAmt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    salesexamtionno = models.CharField(db_column='SalesExamtionNo', max_length=60, blank=True, null=True)  # Field name made lowercase.
    tariffcode = models.CharField(db_column='TariffCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    desc2 = models.CharField(db_column='Desc2', max_length=100, blank=True, null=True)  # Field name made lowercase.
    itemcode = models.ForeignKey('Item', models.DO_NOTHING, db_column='ItemCode', to_field='ItemCode')  # Field name made lowercase.
    location = models.ForeignKey('Location', models.DO_NOTHING, db_column='Location', to_field='Location')  # Field name made lowercase.
    headerautokey = models.CharField(db_column='HeaderAutoKey', max_length=45, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'grdtl'


class Item(models.Model):
    autokey = models.CharField(db_column='Autokey', primary_key=True, max_length=32)  # Field name made lowercase.
    itemcode = models.CharField(db_column='ItemCode', unique=True, max_length=30)  # Field name made lowercase.
    dockkey = models.IntegerField(db_column='DockKey')  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=100, blank=True, null=True)  # Field name made lowercase.
    desc2 = models.CharField(db_column='Desc2', max_length=100, blank=True, null=True)  # Field name made lowercase.
    furtherdescription = models.CharField(db_column='FurtherDescription', max_length=255, blank=True, null=True)  # Field name made lowercase.
    assemblycost = models.DecimalField(db_column='AssemblyCost', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    leadtime = models.CharField(db_column='LeadTime', max_length=40, blank=True, null=True)  # Field name made lowercase.
    stockcontrol = models.CharField(db_column='StockControl', max_length=5)  # Field name made lowercase.
    hasserialno = models.CharField(db_column='HasSerialNo', max_length=5)  # Field name made lowercase.
    hasbatchno = models.CharField(db_column='HasBatchNo', max_length=5)  # Field name made lowercase.
    dutyrate = models.DecimalField(db_column='DutyRate', max_digits=18, decimal_places=6)  # Field name made lowercase.
    note = models.CharField(db_column='Note', max_length=255, blank=True, null=True)  # Field name made lowercase.
    image = models.TextField(db_column='Image', blank=True, null=True)  # Field name made lowercase.
    costingmethod = models.SmallIntegerField(db_column='CostingMethod')  # Field name made lowercase.
    salesuom = models.CharField(db_column='SalesUOM', max_length=8)  # Field name made lowercase.
    purchaseuom = models.CharField(db_column='PurchaseUOM', max_length=8)  # Field name made lowercase.
    reportuom = models.CharField(db_column='ReportUOM', max_length=8)  # Field name made lowercase.
    lastmodified = models.DateTimeField(db_column='LastModified')  # Field name made lowercase.
    lastmodifieduserid = models.CharField(db_column='LastModifiedUserID', max_length=10)  # Field name made lowercase.
    createdtimestamp = models.DateTimeField(db_column='CreatedTimeStamp')  # Field name made lowercase.
    createduserid = models.CharField(db_column='CreatedUserID', max_length=10)  # Field name made lowercase.
    isactive = models.CharField(db_column='IsActive', max_length=5)  # Field name made lowercase.
    lastupdate = models.IntegerField(db_column='LastUpdate')  # Field name made lowercase.
    snformatname = models.CharField(db_column='SNFormatName', max_length=5, blank=True, null=True)  # Field name made lowercase.
    iscalcbonuspoint = models.CharField(db_column='IsCalcBonusPoint', max_length=5, blank=True, null=True)  # Field name made lowercase.
    markupratio = models.DecimalField(db_column='MarkupRatio', max_digits=18, decimal_places=6, blank=True, null=True)  # Field name made lowercase.
    haspromoter = models.CharField(db_column='HasPromoter', max_length=5)  # Field name made lowercase.
    globalcode = models.CharField(db_column='GlobalCode', max_length=30, blank=True, null=True)  # Field name made lowercase.
    leadtimeday = models.IntegerField(db_column='LeadTimeDay', blank=True, null=True)  # Field name made lowercase.
    externallink = models.CharField(db_column='ExternalLink', max_length=255, blank=True, null=True)  # Field name made lowercase.
    discontinued = models.CharField(db_column='Discontinued', max_length=5)  # Field name made lowercase.
    autouomconversion = models.CharField(db_column='AutoUOMConversion', max_length=5, blank=True, null=True)  # Field name made lowercase.
    baseuom = models.CharField(db_column='BaseUOM', max_length=8)  # Field name made lowercase.
    backordercontrol = models.CharField(db_column='BackOrderCOntrol', max_length=5)  # Field name made lowercase.
    purchasetaxtype = models.CharField(db_column='PurchaseTaxType', max_length=14, blank=True, null=True)  # Field name made lowercase.
    tariffcode = models.CharField(db_column='TariffCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    guid = models.CharField(db_column='Guid', max_length=32)  # Field name made lowercase.
    issalesitem = models.CharField(db_column='IsSalesItem', max_length=5, blank=True, null=True)  # Field name made lowercase.
    ispurchaseitem = models.CharField(db_column='IsPurchaseItem', max_length=5, blank=True, null=True)  # Field name made lowercase.
    ispositem = models.CharField(db_column='IspOSItem', max_length=5, blank=True, null=True)  # Field name made lowercase.
    israwmaterialitem = models.CharField(db_column='IsRawMaterialItem', max_length=5, blank=True, null=True)  # Field name made lowercase.
    isfinishgoodsitem = models.CharField(db_column='IsFinishGoodsItem', max_length=5, blank=True, null=True)  # Field name made lowercase.
    imagefilename = models.CharField(db_column='ImageFileName', max_length=120, blank=True, null=True)  # Field name made lowercase.
    companyautokey = models.ForeignKey(Company, models.DO_NOTHING, db_column='CompanyAutoKey')  # Field name made lowercase.
    itembrand = models.CharField(db_column='ItemBrand', max_length=30, blank=True, null=True)  # Field name made lowercase.
    itemcategory = models.CharField(db_column='ItemCategory', max_length=30, blank=True, null=True)  # Field name made lowercase.
    itemclass = models.CharField(db_column='ItemClass', max_length=30, blank=True, null=True)  # Field name made lowercase.
    itemgroup = models.CharField(db_column='ItemGroup', max_length=30, blank=True, null=True)  # Field name made lowercase.
    itemtype = models.CharField(db_column='ItemType', max_length=30, blank=True, null=True)  # Field name made lowercase.
    mainsupplier = models.CharField(db_column='MainSupplier', max_length=30)  # Field name made lowercase.
    taxtype = models.CharField(db_column='TaxType', max_length=30, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'item'


class Itembatch(models.Model):
    autokey = models.CharField(db_column='Autokey', primary_key=True, max_length=32)  # Field name made lowercase.
    itemcode = models.ForeignKey(Item, models.DO_NOTHING, db_column='ItemCode')  # Field name made lowercase.
    batchno = models.CharField(db_column='BatchNo', max_length=20)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=40, blank=True, null=True)  # Field name made lowercase.
    manufactureddate = models.DateTimeField(db_column='ManufacturedDate', blank=True, null=True)  # Field name made lowercase.
    expirydate = models.DateTimeField(db_column='ExpiryDate', blank=True, null=True)  # Field name made lowercase.
    lastsaledate = models.DateTimeField(db_column='LastSaleDate', blank=True, null=True)  # Field name made lowercase.
    guid = models.CharField(db_column='Guid', unique=True, max_length=32)  # Field name made lowercase.
    companyautokey = models.ForeignKey(Company, models.DO_NOTHING, db_column='CompanyAutoKey')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'itembatch'


class Itembom(models.Model):
    autokey = models.CharField(db_column='AutoKey', primary_key=True, max_length=32)  # Field name made lowercase.
    itemcode = models.ForeignKey(Item, models.DO_NOTHING, db_column='ItemCode')  # Field name made lowercase.
    subitemcode = models.CharField(db_column='SubItemCode', max_length=30)  # Field name made lowercase.
    qty = models.DecimalField(db_column='Qty', max_digits=25, decimal_places=8)  # Field name made lowercase.
    overheadcost = models.DecimalField(db_column='OverHeadCost', max_digits=25, decimal_places=8)  # Field name made lowercase.
    seq = models.IntegerField(db_column='Seq')  # Field name made lowercase.
    costfraction = models.DecimalField(db_column='CostFraction', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    companyautokey = models.ForeignKey(Company, models.DO_NOTHING, db_column='CompanyAutoKey')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'itembom'


class Itembrand(models.Model):
    autokey = models.CharField(db_column='Autokey', primary_key=True, max_length=32)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=40, blank=True, null=True)  # Field name made lowercase.
    desc2 = models.CharField(db_column='Desc2', max_length=40, blank=True, null=True)  # Field name made lowercase.
    note = models.CharField(db_column='Note', max_length=40, blank=True, null=True)  # Field name made lowercase.
    lastupdate = models.IntegerField(db_column='LastUpdate')  # Field name made lowercase.
    shortcode = models.CharField(db_column='ShortCode', max_length=8, blank=True, null=True)  # Field name made lowercase.
    markupratio = models.DecimalField(db_column='MarkupRatio', max_digits=18, decimal_places=6, blank=True, null=True)  # Field name made lowercase.
    guid = models.CharField(db_column='Guid', unique=True, max_length=32)  # Field name made lowercase.
    companyautokey = models.ForeignKey(Company, models.DO_NOTHING, db_column='CompanyAutoKey')  # Field name made lowercase.
    itembrand = models.CharField(db_column='ItemBrand', max_length=20)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'itembrand'


class Itemcategory(models.Model):
    autokey = models.CharField(db_column='Autokey', primary_key=True, max_length=32)  # Field name made lowercase.
    itemcategory = models.CharField(db_column='ItemCategory', max_length=20)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=40, blank=True, null=True)  # Field name made lowercase.
    desc2 = models.CharField(db_column='Desc2', max_length=40, blank=True, null=True)  # Field name made lowercase.
    note = models.CharField(db_column='Note', max_length=255, blank=True, null=True)  # Field name made lowercase.
    lastupdate = models.IntegerField(db_column='LastUpdate')  # Field name made lowercase.
    shortcode = models.CharField(db_column='ShortCode', max_length=8, blank=True, null=True)  # Field name made lowercase.
    markupratio = models.DecimalField(db_column='MarkupRatio', max_digits=18, decimal_places=6, blank=True, null=True)  # Field name made lowercase.
    guid = models.CharField(db_column='Guid', unique=True, max_length=32)  # Field name made lowercase.
    companyautokey = models.ForeignKey(Company, models.DO_NOTHING, db_column='CompanyAutoKey')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'itemcategory'


class Itemclass(models.Model):
    itemclass = models.CharField(db_column='ItemClass', unique=True, max_length=20)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=40, blank=True, null=True)  # Field name made lowercase.
    desc2 = models.CharField(db_column='Desc2', max_length=40, blank=True, null=True)  # Field name made lowercase.
    note = models.CharField(db_column='Note', max_length=255, blank=True, null=True)  # Field name made lowercase.
    lastupdate = models.IntegerField(db_column='LastUpdate')  # Field name made lowercase.
    shortcode = models.CharField(db_column='ShortCode', max_length=8, blank=True, null=True)  # Field name made lowercase.
    markupratio = models.DecimalField(db_column='MarkupRatio', max_digits=18, decimal_places=6, blank=True, null=True)  # Field name made lowercase.
    guid = models.CharField(db_column='Guid', unique=True, max_length=32)  # Field name made lowercase.
    companyautokey = models.ForeignKey(Company, models.DO_NOTHING, db_column='CompanyAutoKey')  # Field name made lowercase.
    itemclassguid = models.CharField(db_column='ItemClassGuid', primary_key=True, max_length=32)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'itemclass'


class Itemgroup(models.Model):
    autokey = models.CharField(db_column='AutoKey', primary_key=True, max_length=32)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=40, blank=True, null=True)  # Field name made lowercase.
    desc2 = models.CharField(db_column='Desc2', max_length=40, blank=True, null=True)  # Field name made lowercase.
    note = models.CharField(db_column='Note', max_length=255, blank=True, null=True)  # Field name made lowercase.
    salescode = models.CharField(db_column='SalesCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    cashsalescode = models.CharField(db_column='CashSalesCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    salesreturncode = models.CharField(db_column='SalesReturnCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    salesdiscountcode = models.CharField(db_column='SalesDiscountCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    purchasecode = models.CharField(db_column='PurchaseCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    purchasereturncode = models.CharField(db_column='PurchaseReturnCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    lastupdate = models.IntegerField(db_column='LastUpdate')  # Field name made lowercase.
    shortcode = models.CharField(db_column='ShortCode', max_length=8, blank=True, null=True)  # Field name made lowercase.
    markupration = models.DecimalField(db_column='MarkupRation', max_digits=18, decimal_places=6, blank=True, null=True)  # Field name made lowercase.
    balancestockcode = models.CharField(db_column='BalanceStockCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    guid = models.CharField(db_column='Guid', unique=True, max_length=32)  # Field name made lowercase.
    roundingmethod = models.CharField(db_column='RoundingMethod', max_length=10, blank=True, null=True)  # Field name made lowercase.
    roundingamount = models.CharField(db_column='RoundingAmount', max_length=10, blank=True, null=True)  # Field name made lowercase.
    cashpurchasecode = models.CharField(db_column='CashPurchaseCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    companyautokey = models.ForeignKey(Company, models.DO_NOTHING, db_column='CompanyAutoKey')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'itemgroup'


class Itemprice(models.Model):
    autokey = models.CharField(db_column='Autokey', primary_key=True, max_length=32)  # Field name made lowercase.
    uom = models.CharField(db_column='UOM', max_length=8)  # Field name made lowercase.
    pricecategory = models.CharField(db_column='PriceCategory', max_length=12, blank=True, null=True)  # Field name made lowercase.
    accno = models.CharField(db_column='AccNo', max_length=12, blank=True, null=True)  # Field name made lowercase.
    suppcustitemcode = models.CharField(db_column='SuppCustItemCode', max_length=30, blank=True, null=True)  # Field name made lowercase.
    ref = models.CharField(db_column='Ref', max_length=80, blank=True, null=True)  # Field name made lowercase.
    usefixedprice = models.CharField(db_column='UseFixedPrice', max_length=1)  # Field name made lowercase.
    fixedprice = models.DecimalField(db_column='FixedPrice', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    fixeddetaildiscount = models.CharField(db_column='FixedDetailDiscount', max_length=20, blank=True, null=True)  # Field name made lowercase.
    qty1 = models.DecimalField(db_column='Qty1', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    price1 = models.DecimalField(db_column='Price1', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    detaildiscount1 = models.CharField(db_column='DetailDiscount1', max_length=20, blank=True, null=True)  # Field name made lowercase.
    qty2 = models.DecimalField(db_column='Qty2', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    price2 = models.DecimalField(db_column='Price2', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    detaildiscount2 = models.CharField(db_column='DetailDiscount2', max_length=20, blank=True, null=True)  # Field name made lowercase.
    qty3 = models.DecimalField(db_column='Qty3', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    price3 = models.DecimalField(db_column='Price3', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    detaildiscount3 = models.CharField(db_column='DetailDiscount3', max_length=20, blank=True, null=True)  # Field name made lowercase.
    qty4 = models.DecimalField(db_column='Qty4', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    price4 = models.DecimalField(db_column='Price4', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    detaildiscount4 = models.CharField(db_column='DetailDiscount4', max_length=20, blank=True, null=True)  # Field name made lowercase.
    foclevel = models.DecimalField(db_column='FOCLevel', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    focqty = models.DecimalField(db_column='FOCQty', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    bonuspointqty = models.DecimalField(db_column='BonusPointQty', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    bonuspoint = models.DecimalField(db_column='BonusPoint', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    lastupdate = models.IntegerField(db_column='LastUpdate')  # Field name made lowercase.
    guid = models.CharField(db_column='Guid', unique=True, max_length=32)  # Field name made lowercase.
    companyautokey = models.ForeignKey(Company, models.DO_NOTHING, db_column='CompanyAutoKey')  # Field name made lowercase.
    itemcode = models.ForeignKey(Item, models.DO_NOTHING, db_column='ItemCode', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'itemprice'


class Itemtype(models.Model):
    autokey = models.CharField(db_column='Autokey', primary_key=True, max_length=32)  # Field name made lowercase.
    itemtype = models.CharField(db_column='ItemType', max_length=12)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=40, blank=True, null=True)  # Field name made lowercase.
    desc2 = models.CharField(db_column='Desc2', max_length=40, blank=True, null=True)  # Field name made lowercase.
    note = models.CharField(db_column='Note', max_length=255, blank=True, null=True)  # Field name made lowercase.
    lastupdate = models.IntegerField(db_column='LastUpdate')  # Field name made lowercase.
    shortcode = models.CharField(db_column='ShortCode', max_length=8, blank=True, null=True)  # Field name made lowercase.
    markupratio = models.DecimalField(db_column='MarkupRatio', max_digits=18, decimal_places=6, blank=True, null=True)  # Field name made lowercase.
    guid = models.CharField(db_column='Guid', unique=True, max_length=32)  # Field name made lowercase.
    companyautokey = models.ForeignKey(Company, models.DO_NOTHING, db_column='CompanyAutoKey')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'itemtype'


class Itemuom(models.Model):
    autokey = models.CharField(db_column='Autokey', primary_key=True, max_length=32)  # Field name made lowercase.
    itemcode = models.ForeignKey(Item, models.DO_NOTHING, db_column='ItemCode', to_field='ItemCode')  # Field name made lowercase.
    uom = models.CharField(db_column='UOM', max_length=8)  # Field name made lowercase.
    rate = models.DecimalField(db_column='Rate', max_digits=25, decimal_places=8)  # Field name made lowercase.
    shelf = models.CharField(db_column='Shelf', max_length=20, blank=True, null=True)  # Field name made lowercase.
    price = models.DecimalField(db_column='Price', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    cost = models.DecimalField(db_column='Cost', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    realcost = models.DecimalField(db_column='RealCost', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    mostrecentlycost = models.DecimalField(db_column='MostRecentlyCost', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    minsaleprice = models.DecimalField(db_column='MinSalePrice', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    maxsaleprice = models.DecimalField(db_column='MaxSalePrice', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    minpurchaseprice = models.DecimalField(db_column='MinPurchasePrice', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    maxpurchaseprice = models.DecimalField(db_column='MaxPurchasePrice', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    minqty = models.DecimalField(db_column='MinQty', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    maxqty = models.DecimalField(db_column='MaxQty', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    normallevel = models.DecimalField(db_column='NormalLevel', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    reolevel = models.DecimalField(db_column='ReOLevel', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    reoqty = models.DecimalField(db_column='ReOQty', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    foclevel = models.DecimalField(db_column='FOCLevel', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    focqty = models.DecimalField(db_column='FOCQty', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    bonuspointqty = models.DecimalField(db_column='BonusPointQty', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    bonuspoint = models.DecimalField(db_column='Bonuspoint', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    weight = models.DecimalField(db_column='Weight', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    weightuom = models.CharField(db_column='WeightUOM', max_length=8, blank=True, null=True)  # Field name made lowercase.
    volume = models.DecimalField(db_column='Volume', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    volumeuom = models.CharField(db_column='VolumeUOM', max_length=8, blank=True, null=True)  # Field name made lowercase.
    barcode = models.CharField(db_column='Barcode', max_length=30, blank=True, null=True)  # Field name made lowercase.
    lastupdate = models.IntegerField(db_column='LastUpdate')  # Field name made lowercase.
    redeembonuespoint = models.DecimalField(db_column='RedeemBonuesPoint', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    csgnqty = models.DecimalField(db_column='CSGNQty', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    price2 = models.DecimalField(db_column='Price2', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    guid = models.CharField(db_column='Guid', max_length=32)  # Field name made lowercase.
    price3 = models.DecimalField(db_column='Price3', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    price4 = models.DecimalField(db_column='Price4', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    price5 = models.DecimalField(db_column='Price5', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    price6 = models.DecimalField(db_column='Price6', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    markupratio = models.DecimalField(db_column='MarkupRatio', max_digits=18, decimal_places=6, blank=True, null=True)  # Field name made lowercase.
    markdownratio2 = models.DecimalField(db_column='MarkdownRatio2', max_digits=18, decimal_places=6, blank=True, null=True)  # Field name made lowercase.
    markdownratio3 = models.DecimalField(db_column='MarkdownRatio3', max_digits=18, decimal_places=6, blank=True, null=True)  # Field name made lowercase.
    markdownratio4 = models.DecimalField(db_column='MarkdownRatio4', max_digits=18, decimal_places=6, blank=True, null=True)  # Field name made lowercase.
    markdownratio5 = models.DecimalField(db_column='MarkdownRatio5', max_digits=18, decimal_places=6, blank=True, null=True)  # Field name made lowercase.
    markdownratio6 = models.DecimalField(db_column='MarkdownRatio6', max_digits=18, decimal_places=6, blank=True, null=True)  # Field name made lowercase.
    markdownratiominprice = models.DecimalField(db_column='MarkdownRatioMinPrice', max_digits=18, decimal_places=6, blank=True, null=True)  # Field name made lowercase.
    markdownratiomaxprice = models.DecimalField(db_column='MarkdownRatioMaxPrice', max_digits=18, decimal_places=6, blank=True, null=True)  # Field name made lowercase.
    companyautokey = models.ForeignKey(Company, models.DO_NOTHING, db_column='CompanyAutoKey')  # Field name made lowercase.
    udfcalmethod = models.CharField(db_column='UdfCalMethod', max_length=8, blank=True, null=True)  # Field name made lowercase.
    udfcalrate = models.DecimalField(db_column='UdfCalRate', max_digits=2, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    # udfpallet = models.SmallIntegerField(db_column='UdfPallet', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'itemuom'


class Iv(models.Model):
    autokey = models.CharField(db_column='Autokey', primary_key=True, max_length=32)  # Field name made lowercase.
    docno = models.CharField(db_column='DocNo', max_length=20)  # Field name made lowercase.
    docdate = models.DateTimeField(db_column='DocDate')  # Field name made lowercase.
    debtorcode = models.ForeignKey(Debtor, models.DO_NOTHING, db_column='DebtorCode', to_field='AccNo')  # Field name made lowercase.
    ref = models.CharField(db_column='Ref', max_length=40, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=80, blank=True, null=True)  # Field name made lowercase.
    salesagent = models.ForeignKey('Salesagent', models.DO_NOTHING, db_column='SalesAgent', to_field='SalesAgent')  # Field name made lowercase.
    invaddr1 = models.CharField(db_column='InvAddr1', max_length=40, blank=True, null=True)  # Field name made lowercase.
    invaddr2 = models.CharField(db_column='InvAddr2', max_length=40, blank=True, null=True)  # Field name made lowercase.
    invaddr3 = models.CharField(db_column='InvAddr3', max_length=40, blank=True, null=True)  # Field name made lowercase.
    invaddr4 = models.CharField(db_column='InvAddr4', max_length=40, blank=True, null=True)  # Field name made lowercase.
    phone1 = models.CharField(db_column='Phone1', max_length=25, blank=True, null=True)  # Field name made lowercase.
    fax1 = models.CharField(db_column='Fax1', max_length=25, blank=True, null=True)  # Field name made lowercase.
    attention = models.CharField(db_column='Attention', max_length=40, blank=True, null=True)  # Field name made lowercase.
    branchcode = models.CharField(db_column='BranchCode', max_length=20, blank=True, null=True)  # Field name made lowercase.
    deliveraddr1 = models.CharField(db_column='DeliverAddr1', max_length=40, blank=True, null=True)  # Field name made lowercase.
    deliveraddr2 = models.CharField(db_column='DeliverAddr2', max_length=40, blank=True, null=True)  # Field name made lowercase.
    deliveraddr3 = models.CharField(db_column='DeliverAddr3', max_length=40, blank=True, null=True)  # Field name made lowercase.
    deliveraddr4 = models.CharField(db_column='DeliverAddr4', max_length=40, blank=True, null=True)  # Field name made lowercase.
    deliverphone1 = models.CharField(db_column='DeliverPhone1', max_length=25, blank=True, null=True)  # Field name made lowercase.
    deliverfax1 = models.CharField(db_column='DeliverFax1', max_length=25, blank=True, null=True)  # Field name made lowercase.
    delivercontact = models.CharField(db_column='DeliverContact', max_length=40, blank=True, null=True)  # Field name made lowercase.
    salesexemptionno = models.CharField(db_column='SalesExemptionNo', max_length=60, blank=True, null=True)  # Field name made lowercase.
    salesexemptionexpirydate = models.DateTimeField(db_column='SalesExemptionExpiryDate', blank=True, null=True)  # Field name made lowercase.
    total = models.DecimalField(db_column='Total', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    footer1param = models.DecimalField(db_column='Footer1Param', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer1amt = models.DecimalField(db_column='Footer1Amt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer1localamt = models.DecimalField(db_column='Footer1LocalAmt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer1taxtype = models.CharField(db_column='Footer1TaxType', max_length=14, blank=True, null=True)  # Field name made lowercase.
    footer2param = models.DecimalField(db_column='Footer2Param', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer2amt = models.DecimalField(db_column='Footer2Amt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer2localamt = models.DecimalField(db_column='Footer2LocalAmt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer2taxtype = models.CharField(db_column='Footer2TaxType', max_length=14, blank=True, null=True)  # Field name made lowercase.
    footer3param = models.DecimalField(db_column='Footer3Param', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer3amt = models.DecimalField(db_column='Footer3Amt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer3localamt = models.DecimalField(db_column='Footer3LocalAmt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer3taxtype = models.CharField(db_column='Footer3TaxType', max_length=14, blank=True, null=True)  # Field name made lowercase.
    crrencycode = models.CharField(db_column='CrrencyCode', max_length=5)  # Field name made lowercase.
    currencyrate = models.DecimalField(db_column='CurrencyRate', max_digits=19, decimal_places=4)  # Field name made lowercase.
    nettotal = models.DecimalField(db_column='NetTotal', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    localnettotal = models.DecimalField(db_column='LocalNetTotal', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    analysisnettotal = models.DecimalField(db_column='AnalysisNetTotal', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    localanalysisnettotal = models.DecimalField(db_column='LocalAnalysisNetTotal', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    localtotalcost = models.DecimalField(db_column='LocalTotalCost', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    tax = models.DecimalField(db_column='Tax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    localtax = models.DecimalField(db_column='LocalTax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    totalbonuspoint = models.DecimalField(db_column='TotalBonusPoint', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    posttostock = models.CharField(db_column='PostToStock', max_length=1)  # Field name made lowercase.
    posttogl = models.CharField(db_column='PostToGL', max_length=1)  # Field name made lowercase.
    referdepositdockey = models.BigIntegerField(db_column='ReferDepositDocKey', blank=True, null=True)  # Field name made lowercase.
    transferable = models.CharField(db_column='Transferable', max_length=1)  # Field name made lowercase.
    todoctype = models.CharField(db_column='ToDocType', max_length=2, blank=True, null=True)  # Field name made lowercase.
    todockey = models.BigIntegerField(db_column='ToDocKey', blank=True, null=True)  # Field name made lowercase.
    note = models.CharField(db_column='Note', max_length=255, blank=True, null=True)  # Field name made lowercase.
    remark1 = models.CharField(db_column='Remark1', max_length=40, blank=True, null=True)  # Field name made lowercase.
    remark2 = models.CharField(db_column='Remark2', max_length=40, blank=True, null=True)  # Field name made lowercase.
    remark3 = models.CharField(db_column='Remark3', max_length=40, blank=True, null=True)  # Field name made lowercase.
    remark4 = models.CharField(db_column='Remark4', max_length=40, blank=True, null=True)  # Field name made lowercase.
    printcount = models.SmallIntegerField(db_column='PrintCOunt')  # Field name made lowercase.
    cancelled = models.CharField(db_column='Cancelled', max_length=1)  # Field name made lowercase.
    lastmodified = models.DateTimeField(db_column='LastModified')  # Field name made lowercase.
    lastmodifieduserid = models.CharField(db_column='LastModifiedUserID', max_length=10)  # Field name made lowercase.
    createdtimestamp = models.DateTimeField(db_column='CreatedTimeStamp')  # Field name made lowercase.
    createduserid = models.CharField(db_column='CreatedUserID', max_length=10)  # Field name made lowercase.
    externallink = models.CharField(db_column='ExternalLink', max_length=255, blank=True, null=True)  # Field name made lowercase.
    refdocno = models.CharField(db_column='RefDocNo', max_length=20, blank=True, null=True)  # Field name made lowercase.
    cansync = models.CharField(db_column='CanSync', max_length=1)  # Field name made lowercase.
    lastupdate = models.IntegerField(db_column='LastUpdate')  # Field name made lowercase.
    memberno = models.CharField(db_column='MemberNo', max_length=20, blank=True, null=True)  # Field name made lowercase.
    todtlkey = models.BigIntegerField(db_column='ToDtlKey', blank=True, null=True)  # Field name made lowercase.
    fulltransferoption = models.CharField(db_column='FullTransferOption', max_length=1, blank=True, null=True)  # Field name made lowercase.
    shipvia = models.CharField(db_column='ShipVia', max_length=20, blank=True, null=True)  # Field name made lowercase.
    shipinfo = models.CharField(db_column='ShipInfo', max_length=40, blank=True, null=True)  # Field name made lowercase.
    reallocatepurchasebyproject = models.CharField(db_column='ReallocatePurchaseByProject', max_length=1)  # Field name made lowercase.
    reallocatepurchasebyprojectjedockey = models.BigIntegerField(db_column='ReallocatePurchaseByProjectJEDocKey', blank=True, null=True)  # Field name made lowercase.
    refno2 = models.CharField(db_column='RefNo2', max_length=20, blank=True, null=True)  # Field name made lowercase.
    saleslocation = models.CharField(db_column='SalesLocation', max_length=8, blank=True, null=True)  # Field name made lowercase.
    footer1tax = models.DecimalField(db_column='Footer1Tax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer1localtax = models.DecimalField(db_column='Footer1LocalTax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer2tax = models.DecimalField(db_column='Footer2Tax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer2localtax = models.DecimalField(db_column='Footer2LocalTax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer3tax = models.DecimalField(db_column='Footer3Tax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer3localtax = models.DecimalField(db_column='Footer3LocalTax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    extax = models.DecimalField(db_column='ExTax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    localextax = models.DecimalField(db_column='LocalExTax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    yourpono = models.CharField(db_column='YourPONo', max_length=25, blank=True, null=True)  # Field name made lowercase.
    yourpodate = models.DateTimeField(db_column='YourPODate', blank=True, null=True)  # Field name made lowercase.
    guid = models.CharField(db_column='Guid', unique=True, max_length=32)  # Field name made lowercase.
    reallocatepurchasebyprojectno = models.CharField(db_column='ReallocatePurchaseByProjectNo', max_length=10, blank=True, null=True)  # Field name made lowercase.
    totaxcurrencyrate = models.DecimalField(db_column='ToTaxCurrencyRate', max_digits=19, decimal_places=2)  # Field name made lowercase.
    roundadj = models.DecimalField(db_column='RoundAdj', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    finaltotal = models.DecimalField(db_column='FinalTotal', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    calcdiscountonunitprice = models.CharField(db_column='CalcDiscountOnUnitPrice', max_length=1, blank=True, null=True)  # Field name made lowercase.
    taxdocno = models.CharField(db_column='TaxDocNo', max_length=20, blank=True, null=True)  # Field name made lowercase.
    totalextax = models.DecimalField(db_column='TotalExTax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    taxableamt = models.DecimalField(db_column='TaxableAmt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    inclusivetax = models.CharField(db_column='InclusiveTax', max_length=1)  # Field name made lowercase.
    footer1taxrate = models.DecimalField(db_column='Footer1TaxRate', max_digits=18, decimal_places=6, blank=True, null=True)  # Field name made lowercase.
    footer2taxrate = models.DecimalField(db_column='Footer2TaxRate', max_digits=18, decimal_places=6, blank=True, null=True)  # Field name made lowercase.
    footer3taxrate = models.DecimalField(db_column='Footer3TaxRate', max_digits=18, decimal_places=6, blank=True, null=True)  # Field name made lowercase.
    taxdate = models.DateTimeField(db_column='TaxDate', blank=True, null=True)  # Field name made lowercase.
    isroundadj = models.CharField(db_column='IsRoundAdj', max_length=1)  # Field name made lowercase.
    roundingmethod = models.IntegerField(db_column='RoundingMethod')  # Field name made lowercase.
    localtaxableamt = models.DecimalField(db_column='LocalTaxableAmt', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    taxcurrencytax = models.DecimalField(db_column='TaxCurrencyTax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    taxcurrencytaxableamt = models.DecimalField(db_column='TaxCurrencyTaxableAmt', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    multiprice = models.CharField(db_column='MultiPrice', max_length=8, blank=True, null=True)  # Field name made lowercase.
    taxbranchid = models.CharField(db_column='TaxBranchID', max_length=8, blank=True, null=True)  # Field name made lowercase.
    branchautokey = models.CharField(db_column='BranchAutoKey', max_length=255)  # Field name made lowercase.
    displayterm = models.ForeignKey('Terms', models.DO_NOTHING, db_column='DisplayTerm')  # Field name made lowercase.
    debtorname = models.CharField(db_column='DebtorName', max_length=80)  # Field name made lowercase.
    lorrydriver = models.ForeignKey('Lorrydriver', models.DO_NOTHING, db_column='LorryDriver', to_field='LorryDriver')  # Field name made lowercase.
    udfbook = models.PositiveSmallIntegerField(db_column='UdfBook', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'iv'


class Ivdtl(models.Model):
    autokey = models.CharField(db_column='Autokey', primary_key=True, max_length=32)  # Field name made lowercase.
    focdtlkey = models.BigIntegerField(db_column='FOCDtlKey', blank=True, null=True)  # Field name made lowercase.
    seq = models.IntegerField(db_column='Seq')  # Field name made lowercase.
    indent = models.SmallIntegerField(db_column='Indent', blank=True, null=True)  # Field name made lowercase.
    fontstyle = models.CharField(db_column='FontStyle', max_length=8, blank=True, null=True)  # Field name made lowercase.
    mainitem = models.CharField(db_column='Mainitem', max_length=1)  # Field name made lowercase.
    numbering = models.CharField(db_column='Numbering', max_length=6, blank=True, null=True)  # Field name made lowercase.
    batchno = models.CharField(db_column='BatchNo', max_length=20, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=100, blank=True, null=True)  # Field name made lowercase.
    furtherdescription = models.CharField(db_column='FurtherDescription', max_length=255, blank=True, null=True)  # Field name made lowercase.
    yourpono = models.CharField(db_column='YourPONo', max_length=25, blank=True, null=True)  # Field name made lowercase.
    yourpodate = models.DateTimeField(db_column='YourPODate', blank=True, null=True)  # Field name made lowercase.
    posttostockdate = models.DateTimeField(db_column='PostToStockDate', blank=True, null=True)  # Field name made lowercase.
    projno = models.CharField(db_column='ProjNo', max_length=10, blank=True, null=True)  # Field name made lowercase.
    deptno = models.CharField(db_column='DeptNo', max_length=10, blank=True, null=True)  # Field name made lowercase.
    uom = models.CharField(db_column='UOM', max_length=8, blank=True, null=True)  # Field name made lowercase.
    useruom = models.CharField(db_column='UserUOM', max_length=8, blank=True, null=True)  # Field name made lowercase.
    qty = models.DecimalField(db_column='Qty', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    rate = models.DecimalField(db_column='Rate', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    smallestqty = models.DecimalField(db_column='SmallestQty', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    transferedqty = models.DecimalField(db_column='TransferedQty', max_digits=25, decimal_places=8)  # Field name made lowercase.
    focqty = models.DecimalField(db_column='FOCQty', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    foctransferedqty = models.DecimalField(db_column='FOCTransferedQty', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    smallestunitprice = models.DecimalField(db_column='SmallestUnitPrice', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    unitprice = models.DecimalField(db_column='UnitPrice', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    discount = models.CharField(db_column='Discount', max_length=20, blank=True, null=True)  # Field name made lowercase.
    discountamt = models.DecimalField(db_column='DiscountAmt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    taxtype = models.CharField(db_column='TaxType', max_length=14, blank=True, null=True)  # Field name made lowercase.
    tax = models.DecimalField(db_column='Tax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    subtotal = models.DecimalField(db_column='SubTotal', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    localsubtotal = models.DecimalField(db_column='LocalSubTotal', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    localtotalcost = models.DecimalField(db_column='LocalTotalCost', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    localfoctotalcost = models.DecimalField(db_column='LocalFOCTotalCost', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    bonuspoint = models.DecimalField(db_column='BonusPoint', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    transferable = models.CharField(db_column='Transferable', max_length=1)  # Field name made lowercase.
    printout = models.CharField(db_column='PrintOut', max_length=1)  # Field name made lowercase.
    dtltype = models.CharField(db_column='DTLType', max_length=1, blank=True, null=True)  # Field name made lowercase.
    calcbypercent = models.DecimalField(db_column='CalcByPercent', max_digits=18, decimal_places=6, blank=True, null=True)  # Field name made lowercase.
    addtosubtotal = models.CharField(db_column='AddToSubTotal', max_length=1)  # Field name made lowercase.
    fromdoctype = models.CharField(db_column='FromDocType', max_length=2, blank=True, null=True)  # Field name made lowercase.
    fromdocno = models.CharField(db_column='FromDocNo', max_length=255, blank=True, null=True)  # Field name made lowercase.
    fromdocdtlkey = models.BigIntegerField(db_column='FromDocDtlKey', blank=True, null=True)  # Field name made lowercase.
    valuexfersodockey = models.BigIntegerField(db_column='ValueXferSODocKey', blank=True, null=True)  # Field name made lowercase.
    accno = models.CharField(db_column='AccNo', max_length=12, blank=True, null=True)  # Field name made lowercase.
    fulltransferoption = models.CharField(db_column='FullTransferOption', max_length=1, blank=True, null=True)  # Field name made lowercase.
    fulltransferfromdoclist = models.CharField(db_column='FullTransferFromDocList', max_length=255, blank=True, null=True)  # Field name made lowercase.
    ourdono = models.CharField(db_column='OurDONo', max_length=20, blank=True, null=True)  # Field name made lowercase.
    ourdodate = models.DateTimeField(db_column='OurDODate', blank=True, null=True)  # Field name made lowercase.
    serialnolist = models.CharField(db_column='SerialNoList', max_length=255, blank=True, null=True)  # Field name made lowercase.
    estimateddeliverydate = models.CharField(db_column='EstimatedDeliveryDate', max_length=20, blank=True, null=True)  # Field name made lowercase.
    packagedockey = models.BigIntegerField(db_column='PackageDocKey', blank=True, null=True)  # Field name made lowercase.
    parentdtlkey = models.BigIntegerField(db_column='ParentDtlKey', blank=True, null=True)  # Field name made lowercase.
    subqty = models.DecimalField(db_column='SubQty', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    iscalcbonuspoint = models.CharField(db_column='IsCalcBonusPoint', max_length=1, blank=True, null=True)  # Field name made lowercase.
    subtotalextax = models.DecimalField(db_column='SubTotalExTax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    localtax = models.DecimalField(db_column='LocalTax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    guid = models.CharField(db_column='Guid', unique=True, max_length=32)  # Field name made lowercase.
    ruleno = models.BigIntegerField(db_column='RuleNo', blank=True, null=True)  # Field name made lowercase.
    deliverydate = models.DateTimeField(db_column='DeliveryDate', blank=True, null=True)  # Field name made lowercase.
    taxableamt = models.DecimalField(db_column='TaxableAmt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    taxadjustment = models.DecimalField(db_column='TaxAdjustment', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    taxexportcountry = models.CharField(db_column='TaxExportCountry', max_length=50, blank=True, null=True)  # Field name made lowercase.
    localsubtotalextax = models.DecimalField(db_column='LocalSubTotalExTax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    extradiscountamt = models.DecimalField(db_column='ExtraDiscountAmt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    taxrate = models.DecimalField(db_column='TaxRate', max_digits=18, decimal_places=6, blank=True, null=True)  # Field name made lowercase.
    localtaxadjustment = models.DecimalField(db_column='LocalTaxAdjustment', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    localtaxableamt = models.DecimalField(db_column='LocalTaxableAmt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    taxcurrencytax = models.DecimalField(db_column='TaxCurrencyTax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    taxcurrencytaxableamt = models.DecimalField(db_column='TaxCurrencyTaxableAmt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    taxpermitno = models.CharField(db_column='TaxPermitNo', max_length=20, blank=True, null=True)  # Field name made lowercase.
    salesexamtionno = models.CharField(db_column='SalesExamtionNo', max_length=60, blank=True, null=True)  # Field name made lowercase.
    desc2 = models.CharField(db_column='Desc2', max_length=100, blank=True, null=True)  # Field name made lowercase.
    headerautokey = models.ForeignKey(Iv, models.DO_NOTHING, db_column='HeaderAutoKey')  # Field name made lowercase.
    itemcode = models.ForeignKey(Item, models.DO_NOTHING, db_column='ItemCode', to_field='ItemCode', blank=True, null=True)  # Field name made lowercase.
    location = models.ForeignKey('Location', models.DO_NOTHING, db_column='Location')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ivdtl'


class IvdtlCopy(models.Model):
    autokey = models.CharField(db_column='Autokey', primary_key=True, max_length=32)  # Field name made lowercase.
    focdtlkey = models.BigIntegerField(db_column='FOCDtlKey', blank=True, null=True)  # Field name made lowercase.
    seq = models.IntegerField(db_column='Seq')  # Field name made lowercase.
    indent = models.SmallIntegerField(db_column='Indent', blank=True, null=True)  # Field name made lowercase.
    fontstyle = models.CharField(db_column='FontStyle', max_length=8, blank=True, null=True)  # Field name made lowercase.
    mainitem = models.CharField(db_column='Mainitem', max_length=1)  # Field name made lowercase.
    numbering = models.CharField(db_column='Numbering', max_length=6, blank=True, null=True)  # Field name made lowercase.
    batchno = models.CharField(db_column='BatchNo', max_length=20, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=100, blank=True, null=True)  # Field name made lowercase.
    furtherdescription = models.CharField(db_column='FurtherDescription', max_length=255, blank=True, null=True)  # Field name made lowercase.
    yourpono = models.CharField(db_column='YourPONo', max_length=25, blank=True, null=True)  # Field name made lowercase.
    yourpodate = models.DateTimeField(db_column='YourPODate', blank=True, null=True)  # Field name made lowercase.
    posttostockdate = models.DateTimeField(db_column='PostToStockDate', blank=True, null=True)  # Field name made lowercase.
    projno = models.CharField(db_column='ProjNo', max_length=10, blank=True, null=True)  # Field name made lowercase.
    deptno = models.CharField(db_column='DeptNo', max_length=10, blank=True, null=True)  # Field name made lowercase.
    uom = models.CharField(db_column='UOM', max_length=8, blank=True, null=True)  # Field name made lowercase.
    useruom = models.CharField(db_column='UserUOM', max_length=8, blank=True, null=True)  # Field name made lowercase.
    qty = models.DecimalField(db_column='Qty', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    rate = models.DecimalField(db_column='Rate', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    smallestqty = models.DecimalField(db_column='SmallestQty', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    transferedqty = models.DecimalField(db_column='TransferedQty', max_digits=25, decimal_places=8)  # Field name made lowercase.
    focqty = models.DecimalField(db_column='FOCQty', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    foctransferedqty = models.DecimalField(db_column='FOCTransferedQty', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    smallestunitprice = models.DecimalField(db_column='SmallestUnitPrice', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    unitprice = models.DecimalField(db_column='UnitPrice', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    discount = models.CharField(db_column='Discount', max_length=20, blank=True, null=True)  # Field name made lowercase.
    discountamt = models.DecimalField(db_column='DiscountAmt', max_digits=19, decimal_places=9, blank=True, null=True)  # Field name made lowercase.
    taxtype = models.CharField(db_column='TaxType', max_length=14, blank=True, null=True)  # Field name made lowercase.
    tax = models.DecimalField(db_column='Tax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    subtotal = models.DecimalField(db_column='SubTotal', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    localsubtotal = models.DecimalField(db_column='LocalSubTotal', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    localtotalcost = models.DecimalField(db_column='LocalTotalCost', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    localfoctotalcost = models.DecimalField(db_column='LocalFOCTotalCost', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    bonuspoint = models.DecimalField(db_column='BonusPoint', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    transferable = models.CharField(db_column='Transferable', max_length=1)  # Field name made lowercase.
    printout = models.CharField(db_column='PrintOut', max_length=1)  # Field name made lowercase.
    dtltype = models.CharField(db_column='DTLType', max_length=1, blank=True, null=True)  # Field name made lowercase.
    calcbypercent = models.DecimalField(db_column='CalcByPercent', max_digits=18, decimal_places=6, blank=True, null=True)  # Field name made lowercase.
    addtosubtotal = models.CharField(db_column='AddToSubTotal', max_length=1)  # Field name made lowercase.
    fromdoctype = models.CharField(db_column='FromDocType', max_length=2, blank=True, null=True)  # Field name made lowercase.
    fromdocno = models.CharField(db_column='FromDocNo', max_length=255, blank=True, null=True)  # Field name made lowercase.
    fromdocdtlkey = models.BigIntegerField(db_column='FromDocDtlKey', blank=True, null=True)  # Field name made lowercase.
    valuexfersodockey = models.BigIntegerField(db_column='ValueXferSODocKey', blank=True, null=True)  # Field name made lowercase.
    accno = models.CharField(db_column='AccNo', max_length=12, blank=True, null=True)  # Field name made lowercase.
    fulltransferoption = models.CharField(db_column='FullTransferOption', max_length=1, blank=True, null=True)  # Field name made lowercase.
    fulltransferfromdoclist = models.CharField(db_column='FullTransferFromDocList', max_length=255, blank=True, null=True)  # Field name made lowercase.
    ourdono = models.CharField(db_column='OurDONo', max_length=20, blank=True, null=True)  # Field name made lowercase.
    ourdodate = models.DateTimeField(db_column='OurDODate', blank=True, null=True)  # Field name made lowercase.
    serialnolist = models.CharField(db_column='SerialNoList', max_length=255, blank=True, null=True)  # Field name made lowercase.
    estimateddeliverydate = models.CharField(db_column='EstimatedDeliveryDate', max_length=20, blank=True, null=True)  # Field name made lowercase.
    packagedockey = models.BigIntegerField(db_column='PackageDocKey', blank=True, null=True)  # Field name made lowercase.
    parentdtlkey = models.BigIntegerField(db_column='ParentDtlKey', blank=True, null=True)  # Field name made lowercase.
    subqty = models.DecimalField(db_column='SubQty', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    iscalcbonuspoint = models.CharField(db_column='IsCalcBonusPoint', max_length=1, blank=True, null=True)  # Field name made lowercase.
    subtotalextax = models.DecimalField(db_column='SubTotalExTax', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    localtax = models.DecimalField(db_column='LocalTax', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    guid = models.CharField(db_column='Guid', unique=True, max_length=32)  # Field name made lowercase.
    ruleno = models.BigIntegerField(db_column='RuleNo', blank=True, null=True)  # Field name made lowercase.
    deliverydate = models.DateTimeField(db_column='DeliveryDate', blank=True, null=True)  # Field name made lowercase.
    taxableamt = models.DecimalField(db_column='TaxableAmt', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    taxadjustment = models.DecimalField(db_column='TaxAdjustment', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    taxexportcountry = models.CharField(db_column='TaxExportCountry', max_length=50, blank=True, null=True)  # Field name made lowercase.
    localsubtotalextax = models.DecimalField(db_column='LocalSubTotalExTax', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    extradiscountamt = models.DecimalField(db_column='ExtraDiscountAmt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    taxrate = models.DecimalField(db_column='TaxRate', max_digits=18, decimal_places=6, blank=True, null=True)  # Field name made lowercase.
    localtaxadjustment = models.DecimalField(db_column='LocalTaxAdjustment', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    localtaxableamt = models.DecimalField(db_column='LocalTaxableAmt', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    taxcurrencytax = models.DecimalField(db_column='TaxCurrencyTax', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    taxcurrencytaxableamt = models.DecimalField(db_column='TaxCurrencyTaxableAmt', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    taxpermitno = models.CharField(db_column='TaxPermitNo', max_length=20, blank=True, null=True)  # Field name made lowercase.
    salesexamtionno = models.CharField(db_column='SalesExamtionNo', max_length=60, blank=True, null=True)  # Field name made lowercase.
    desc2 = models.CharField(db_column='Desc2', max_length=100, blank=True, null=True)  # Field name made lowercase.
    itemcode = models.CharField(db_column='ItemCode', max_length=30)  # Field name made lowercase.
    location = models.CharField(db_column='Location', max_length=60)  # Field name made lowercase.
    headerautokey = models.CharField(db_column='HeaderAutoKey', max_length=45, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ivdtl_copy'


class Location(models.Model):
    autokey = models.CharField(db_column='Autokey', primary_key=True, max_length=32)  # Field name made lowercase.
    location = models.CharField(db_column='Location', unique=True, max_length=30)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=80, blank=True, null=True)  # Field name made lowercase.
    desc2 = models.CharField(db_column='Desc2', max_length=80, blank=True, null=True)  # Field name made lowercase.
    address1 = models.CharField(db_column='Address1', max_length=40, blank=True, null=True)  # Field name made lowercase.
    address2 = models.CharField(db_column='Address2', max_length=40, blank=True, null=True)  # Field name made lowercase.
    address3 = models.CharField(db_column='Address3', max_length=40, blank=True, null=True)  # Field name made lowercase.
    address4 = models.CharField(db_column='Address4', max_length=40, blank=True, null=True)  # Field name made lowercase.
    postcode = models.CharField(db_column='PostCode', max_length=10, blank=True, null=True)  # Field name made lowercase.
    phone1 = models.CharField(db_column='Phone1', max_length=25, blank=True, null=True)  # Field name made lowercase.
    phone2 = models.CharField(db_column='Phone2', max_length=25, blank=True, null=True)  # Field name made lowercase.
    fax1 = models.CharField(db_column='Fax1', max_length=25, blank=True, null=True)  # Field name made lowercase.
    fax2 = models.CharField(db_column='Fax2', max_length=25, blank=True, null=True)  # Field name made lowercase.
    contact = models.CharField(db_column='Contact', max_length=40, blank=True, null=True)  # Field name made lowercase.
    note = models.CharField(db_column='Note', max_length=255, blank=True, null=True)  # Field name made lowercase.
    isactive = models.CharField(db_column='IsActive', max_length=5)  # Field name made lowercase.
    lastupdate = models.IntegerField(db_column='LastUpdate')  # Field name made lowercase.
    areacode = models.CharField(db_column='AreaCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    cashpayment = models.CharField(db_column='CashPayment', max_length=20, blank=True, null=True)  # Field name made lowercase.
    debitcardpayment = models.CharField(db_column='DebitCardPayment', max_length=20, blank=True, null=True)  # Field name made lowercase.
    voucherpaymentmethod = models.CharField(db_column='VoucherPaymentMethod', max_length=20, blank=True, null=True)  # Field name made lowercase.
    chequepaymentmethod = models.CharField(db_column='ChequePaymentMethod', max_length=20, blank=True, null=True)  # Field name made lowercase.
    pointpaymentmethod = models.CharField(db_column='PointPaymentMethod', max_length=20, blank=True, null=True)  # Field name made lowercase.
    roundingaccno = models.CharField(db_column='RoundingAccNo', max_length=12, blank=True, null=True)  # Field name made lowercase.
    depositaccno = models.CharField(db_column='DepositAccNo', max_length=12, blank=True, null=True)  # Field name made lowercase.
    forfeitedaccno = models.CharField(db_column='ForfeitedAccNo', max_length=12, blank=True, null=True)  # Field name made lowercase.
    creditcardchargesaccno = models.CharField(db_column='CreditCardChargesAccNo', max_length=12, blank=True, null=True)  # Field name made lowercase.
    pointpaymentaccno = models.CharField(db_column='PointPaymentAccNo', max_length=12, blank=True, null=True)  # Field name made lowercase.
    servicechargeaccno = models.CharField(db_column='ServiceChargeAccNo', max_length=12, blank=True, null=True)  # Field name made lowercase.
    voucherforfeitedaccno = models.CharField(db_column='VoucherForfeitedAccNo', max_length=12, blank=True, null=True)  # Field name made lowercase.
    guid = models.CharField(db_column='Guid', unique=True, max_length=32, blank=True, null=True)  # Field name made lowercase.
    tipaccno = models.CharField(db_column='TipAccNo', max_length=12, blank=True, null=True)  # Field name made lowercase.
    branchautokey = models.ForeignKey(Branch, models.DO_NOTHING, db_column='BranchAutoKey')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'location'


class Lorry(models.Model):
    lorryguid = models.CharField(db_column='LorryGuid', primary_key=True, max_length=32)  # Field name made lowercase.
    lorrynumber = models.ForeignKey('Lorryplate', models.DO_NOTHING, db_column='LorryNumber', to_field='LorryNumber')  # Field name made lowercase.
    docdate = models.DateTimeField(db_column='DocDate')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'lorry'


class Lorrydriver(models.Model):
    autokey = models.CharField(db_column='Autokey', primary_key=True, max_length=32)  # Field name made lowercase.
    lorrydriver = models.CharField(db_column='LorryDriver', unique=True, max_length=40)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'lorrydriver'


class Lorryplate(models.Model):
    lorryplateguid = models.CharField(db_column='LorryPlateGuid', primary_key=True, max_length=32)  # Field name made lowercase.
    lorrynumber = models.CharField(db_column='LorryNumber', unique=True, max_length=30)  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='CreatedAt')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'lorryplate'


class Pi(models.Model):
    autokey = models.CharField(db_column='AutoKey', primary_key=True, max_length=32)  # Field name made lowercase.
    docno = models.CharField(db_column='DocNo', max_length=20)  # Field name made lowercase.
    docdate = models.DateTimeField(db_column='DocDate')  # Field name made lowercase.
    creditorcode = models.ForeignKey(Creditor, models.DO_NOTHING, db_column='CreditorCode', to_field='AccNo')  # Field name made lowercase.
    creditorname = models.ForeignKey(Creditor, models.DO_NOTHING, db_column='CreditorName', to_field='CompanyName', related_name='pi_creditorname_set')  # Field name made lowercase.
    ref = models.CharField(db_column='Ref', max_length=40, blank=True, null=True)  # Field name made lowercase.
    supplierdono = models.CharField(db_column='SupplierDONo', max_length=20, blank=True, null=True)  # Field name made lowercase.
    supplierinvoiceno = models.CharField(db_column='SupplierInvoiceNo', max_length=20, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=80, blank=True, null=True)  # Field name made lowercase.
    displayterm = models.ForeignKey('Terms', models.DO_NOTHING, db_column='DisplayTerm', to_field='DisplayTerm')  # Field name made lowercase.
    purchaseagent = models.CharField(db_column='PurchaseAgent', max_length=12, blank=True, null=True)  # Field name made lowercase.
    invaddr1 = models.CharField(db_column='InvAddr1', max_length=40, blank=True, null=True)  # Field name made lowercase.
    invaddr2 = models.CharField(db_column='InvAddr2', max_length=40, blank=True, null=True)  # Field name made lowercase.
    invaddr3 = models.CharField(db_column='InvAddr3', max_length=40, blank=True, null=True)  # Field name made lowercase.
    invaddr4 = models.CharField(db_column='InvAddr4', max_length=40, blank=True, null=True)  # Field name made lowercase.
    phone1 = models.CharField(db_column='Phone1', max_length=25, blank=True, null=True)  # Field name made lowercase.
    fax1 = models.CharField(db_column='Fax1', max_length=25, blank=True, null=True)  # Field name made lowercase.
    attention = models.CharField(db_column='Attention', max_length=40, blank=True, null=True)  # Field name made lowercase.
    branchcode = models.CharField(db_column='BranchCode', max_length=20, blank=True, null=True)  # Field name made lowercase.
    total = models.DecimalField(db_column='Total', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer1param = models.DecimalField(db_column='Footer1Param', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer1amt = models.DecimalField(db_column='Footer1Amt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer1localamt = models.DecimalField(db_column='Footer1LocalAmt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer1taxtype = models.CharField(db_column='Footer1TaxType', max_length=14, blank=True, null=True)  # Field name made lowercase.
    footer2param = models.DecimalField(db_column='Footer2Param', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer2amt = models.DecimalField(db_column='Footer2Amt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer2localamt = models.DecimalField(db_column='Footer2LocalAmt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer2taxtype = models.CharField(db_column='Footer2TaxType', max_length=14, blank=True, null=True)  # Field name made lowercase.
    footer3param = models.DecimalField(db_column='Footer3Param', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer3amt = models.DecimalField(db_column='Footer3Amt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer3localamt = models.DecimalField(db_column='Footer3LocalAmt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer3taxtype = models.CharField(db_column='Footer3TaxType', max_length=14, blank=True, null=True)  # Field name made lowercase.
    crrencycode = models.CharField(db_column='CrrencyCode', max_length=5)  # Field name made lowercase.
    currencyrate = models.DecimalField(db_column='CurrencyRate', max_digits=19, decimal_places=2)  # Field name made lowercase.
    nettotal = models.DecimalField(db_column='NetTotal', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    localnettotal = models.DecimalField(db_column='LocalNetTotal', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    tax = models.DecimalField(db_column='Tax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    localtax = models.DecimalField(db_column='LocalTax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    foreigncharges = models.DecimalField(db_column='ForeignCharges', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    localcharges = models.DecimalField(db_column='LocalCharges', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    landedcostmethod = models.CharField(db_column='LandedCostMethod', max_length=1, blank=True, null=True)  # Field name made lowercase.
    posttostock = models.CharField(db_column='PostToStock', max_length=1)  # Field name made lowercase.
    posttogl = models.CharField(db_column='PostToGL', max_length=1)  # Field name made lowercase.
    referdockey = models.BigIntegerField(db_column='ReferDocKey', blank=True, null=True)  # Field name made lowercase.
    referpaymentdockey = models.BigIntegerField(db_column='ReferPaymentDocKey', blank=True, null=True)  # Field name made lowercase.
    transferable = models.CharField(db_column='Transferable', max_length=1)  # Field name made lowercase.
    todoctype = models.CharField(db_column='ToDocType', max_length=2, blank=True, null=True)  # Field name made lowercase.
    todockey = models.BigIntegerField(db_column='ToDocKey', blank=True, null=True)  # Field name made lowercase.
    note = models.CharField(db_column='Note', max_length=255, blank=True, null=True)  # Field name made lowercase.
    remark1 = models.CharField(db_column='Remark1', max_length=40, blank=True, null=True)  # Field name made lowercase.
    remark2 = models.CharField(db_column='Remark2', max_length=40, blank=True, null=True)  # Field name made lowercase.
    remark3 = models.CharField(db_column='Remark3', max_length=40, blank=True, null=True)  # Field name made lowercase.
    remark4 = models.CharField(db_column='Remark4', max_length=40, blank=True, null=True)  # Field name made lowercase.
    printcount = models.SmallIntegerField(db_column='PrintCount')  # Field name made lowercase.
    cancelled = models.CharField(db_column='Cancelled', max_length=1)  # Field name made lowercase.
    lastmodified = models.DateTimeField(db_column='LastModified')  # Field name made lowercase.
    lastmodifieduserid = models.CharField(db_column='LastModifiedUserID', max_length=10)  # Field name made lowercase.
    createdtimestamp = models.DateTimeField(db_column='CreatedTimeStamp')  # Field name made lowercase.
    createduserid = models.CharField(db_column='CreatedUserID', max_length=10)  # Field name made lowercase.
    externallink = models.CharField(db_column='ExternalLink', max_length=255, blank=True, null=True)  # Field name made lowercase.
    refdocno = models.CharField(db_column='RefDocNo', max_length=20, blank=True, null=True)  # Field name made lowercase.
    cansync = models.CharField(db_column='CanSync', max_length=1)  # Field name made lowercase.
    lastupdate = models.IntegerField(db_column='LastUpdate')  # Field name made lowercase.
    todtlkey = models.BigIntegerField(db_column='ToDtlKey', blank=True, null=True)  # Field name made lowercase.
    fulltransferoption = models.CharField(db_column='FullTransferOption', max_length=1, blank=True, null=True)  # Field name made lowercase.
    shipvia = models.CharField(db_column='ShipVia', max_length=20, blank=True, null=True)  # Field name made lowercase.
    shipinfo = models.CharField(db_column='ShipInfo', max_length=40, blank=True, null=True)  # Field name made lowercase.
    refno2 = models.CharField(db_column='RefNo2', max_length=20, blank=True, null=True)  # Field name made lowercase.
    purchaselocation = models.CharField(db_column='PurchaseLocation', max_length=8, blank=True, null=True)  # Field name made lowercase.
    footer1tax = models.DecimalField(db_column='Footer1Tax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer1localtax = models.DecimalField(db_column='Footer1LocalTax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer2tax = models.DecimalField(db_column='Footer2Tax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer2localtax = models.DecimalField(db_column='Footer2LocalTax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer3tax = models.DecimalField(db_column='Footer3Tax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer3localtax = models.DecimalField(db_column='Footer3LocalTax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    extax = models.DecimalField(db_column='ExTax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    localextax = models.DecimalField(db_column='LocalExTax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    analysisnettotal = models.DecimalField(db_column='AnalysisNetTotal', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    localanalysisnettotal = models.DecimalField(db_column='LocalAnalysisNetTotal', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    guid = models.CharField(db_column='Guid', unique=True, max_length=32)  # Field name made lowercase.
    totaxcurrencyrate = models.DecimalField(db_column='ToTaxCurrencyRate', max_digits=19, decimal_places=2)  # Field name made lowercase.
    calcdiscountonunitprice = models.CharField(db_column='CalcDiscountOnUnitPrice', max_length=1, blank=True, null=True)  # Field name made lowercase.
    taxdocno = models.CharField(db_column='TaxDocNo', max_length=20, blank=True, null=True)  # Field name made lowercase.
    totalextax = models.DecimalField(db_column='TotalExTax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    taxableamt = models.DecimalField(db_column='TaxableAmt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    inclusivetax = models.CharField(db_column='InclusiveTax', max_length=1)  # Field name made lowercase.
    footer1taxrate = models.DecimalField(db_column='Footer1TaxRate', max_digits=18, decimal_places=6, blank=True, null=True)  # Field name made lowercase.
    footer2taxrate = models.DecimalField(db_column='Footer2TaxRate', max_digits=18, decimal_places=6, blank=True, null=True)  # Field name made lowercase.
    footer3taxrate = models.DecimalField(db_column='Footer3TaxRate', max_digits=18, decimal_places=6, blank=True, null=True)  # Field name made lowercase.
    taxdate = models.DateTimeField(db_column='TaxDate', blank=True, null=True)  # Field name made lowercase.
    isroundadj = models.CharField(db_column='IsRoundAdj', max_length=1)  # Field name made lowercase.
    roundadj = models.DecimalField(db_column='RoundAdj', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    finaltotal = models.DecimalField(db_column='FinalTotal', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    selfbilledapprovalno = models.CharField(db_column='SelfBilledApprovalNo', max_length=30, blank=True, null=True)  # Field name made lowercase.
    roundingmethod = models.IntegerField(db_column='RoundingMethod')  # Field name made lowercase.
    localtaxableamt = models.DecimalField(db_column='LocalTaxableAmt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    taxcurrencytax = models.DecimalField(db_column='TaxCurrencyTax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    taxcurrencytaxableamt = models.DecimalField(db_column='TaxCurrencyTaxableAmt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    docdate2 = models.DateTimeField(db_column='DocDate2', blank=True, null=True)  # Field name made lowercase.
    taxbranchid = models.CharField(db_column='TaxBranchID', max_length=8, blank=True, null=True)  # Field name made lowercase.
    branchautokey = models.ForeignKey(Branch, models.DO_NOTHING, db_column='BranchAutoKey')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'pi'


class Pidtl(models.Model):
    autokey = models.CharField(db_column='AutoKey', primary_key=True, max_length=32)  # Field name made lowercase.
    focdtlkey = models.BigIntegerField(db_column='FOCDtlKey', blank=True, null=True)  # Field name made lowercase.
    seq = models.IntegerField(db_column='Seq')  # Field name made lowercase.
    indent = models.SmallIntegerField(db_column='Indent', blank=True, null=True)  # Field name made lowercase.
    fontstyle = models.CharField(db_column='FontStyle', max_length=8, blank=True, null=True)  # Field name made lowercase.
    mainitem = models.CharField(db_column='Mainitem', max_length=5)  # Field name made lowercase.
    numbering = models.CharField(db_column='Numbering', max_length=6, blank=True, null=True)  # Field name made lowercase.
    batchno = models.CharField(db_column='BatchNo', max_length=20, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=100, blank=True, null=True)  # Field name made lowercase.
    furtherdescription = models.CharField(db_column='FurtherDescription', max_length=255, blank=True, null=True)  # Field name made lowercase.
    projno = models.CharField(db_column='ProjNo', max_length=10, blank=True, null=True)  # Field name made lowercase.
    deptno = models.CharField(db_column='DeptNo', max_length=10, blank=True, null=True)  # Field name made lowercase.
    ourpono = models.CharField(db_column='OurPONo', max_length=20, blank=True, null=True)  # Field name made lowercase.
    ourpodate = models.DateTimeField(db_column='OurPODate', blank=True, null=True)  # Field name made lowercase.
    posttostockdate = models.DateTimeField(db_column='PostToStockDate', blank=True, null=True)  # Field name made lowercase.
    uom = models.CharField(db_column='UOM', max_length=8, blank=True, null=True)  # Field name made lowercase.
    useruom = models.CharField(db_column='UserUOM', max_length=8, blank=True, null=True)  # Field name made lowercase.
    qty = models.DecimalField(db_column='Qty', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    rate = models.DecimalField(db_column='Rate', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    smallestqty = models.DecimalField(db_column='SmallestQty', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    transferedqty = models.DecimalField(db_column='TransferedQty', max_digits=25, decimal_places=8)  # Field name made lowercase.
    focqty = models.DecimalField(db_column='FOCQty', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    foctransferedqty = models.DecimalField(db_column='FOCTransferedQty', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    smallestunitprice = models.DecimalField(db_column='SmallestUnitPrice', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    unitprice = models.DecimalField(db_column='UnitPrice', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    discount = models.CharField(db_column='Discount', max_length=20, blank=True, null=True)  # Field name made lowercase.
    discountamt = models.DecimalField(db_column='DiscountAmt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    taxtype = models.CharField(db_column='TaxType', max_length=14, blank=True, null=True)  # Field name made lowercase.
    tax = models.DecimalField(db_column='Tax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    subtotal = models.DecimalField(db_column='SubTotal', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    localsubtotal = models.DecimalField(db_column='LocalSubTotal', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    transferable = models.CharField(db_column='Transferable', max_length=1)  # Field name made lowercase.
    printout = models.CharField(db_column='PrintOut', max_length=1)  # Field name made lowercase.
    dtltype = models.CharField(db_column='DTLType', max_length=1, blank=True, null=True)  # Field name made lowercase.
    calcbypercent = models.DecimalField(db_column='CalcByPercent', max_digits=18, decimal_places=6, blank=True, null=True)  # Field name made lowercase.
    addtosubtotal = models.CharField(db_column='AddToSubTotal', max_length=1)  # Field name made lowercase.
    fromdoctype = models.CharField(db_column='FromDocType', max_length=2, blank=True, null=True)  # Field name made lowercase.
    fromdocno = models.CharField(db_column='FromDocNo', max_length=255, blank=True, null=True)  # Field name made lowercase.
    fromdocdtlkey = models.BigIntegerField(db_column='FromDocDtlKey', blank=True, null=True)  # Field name made lowercase.
    fulltransferoption = models.CharField(db_column='FullTransferOption', max_length=1, blank=True, null=True)  # Field name made lowercase.
    foreigncharges = models.DecimalField(db_column='ForeignCharges', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    localcharges = models.DecimalField(db_column='LocalCharges', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    duty = models.DecimalField(db_column='Duty', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    accno = models.CharField(db_column='AccNo', max_length=12, blank=True, null=True)  # Field name made lowercase.
    fulltransferfromdoclist = models.CharField(db_column='FullTransferFromDocList', max_length=255, blank=True, null=True)  # Field name made lowercase.
    serialnolist = models.CharField(db_column='SerialNoList', max_length=255, blank=True, null=True)  # Field name made lowercase.
    estimateddeliverydate = models.CharField(db_column='EstimatedDeliveryDate', max_length=20, blank=True, null=True)  # Field name made lowercase.
    packagedockey = models.BigIntegerField(db_column='PackageDocKey', blank=True, null=True)  # Field name made lowercase.
    parentdtlkey = models.BigIntegerField(db_column='ParentDtlKey', blank=True, null=True)  # Field name made lowercase.
    subqty = models.DecimalField(db_column='SubQty', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    subtotalextax = models.DecimalField(db_column='SubTotalExTax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    localtax = models.DecimalField(db_column='LocalTax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    guid = models.CharField(db_column='Guid', unique=True, max_length=32)  # Field name made lowercase.
    deliverydate = models.DateTimeField(db_column='DeliveryDate', blank=True, null=True)  # Field name made lowercase.
    cnamt = models.DecimalField(db_column='CNAmt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    taxpermitno = models.CharField(db_column='TaxPermitNo', max_length=20, blank=True, null=True)  # Field name made lowercase.
    taxableamt = models.DecimalField(db_column='TaxableAmt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    taxadjustment = models.DecimalField(db_column='TaxAdjustment', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    localsubtotalextax = models.DecimalField(db_column='LocalSubTotalExTax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    extradiscountamt = models.DecimalField(db_column='ExtraDiscountAmt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    taxrate = models.DecimalField(db_column='TaxRate', max_digits=18, decimal_places=6, blank=True, null=True)  # Field name made lowercase.
    localtaxadjustment = models.DecimalField(db_column='LocalTaxAdjustment', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    localtaxableamt = models.DecimalField(db_column='LocalTaxableAmt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    taxcurrencytax = models.DecimalField(db_column='TaxCurrencyTax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    taxcurrencytaxableamt = models.DecimalField(db_column='TaxCurrencyTaxableAmt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    salesexamtionno = models.CharField(db_column='SalesExamtionNo', max_length=60, blank=True, null=True)  # Field name made lowercase.
    tariffcode = models.CharField(db_column='TariffCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    desc2 = models.CharField(db_column='Desc2', max_length=100, blank=True, null=True)  # Field name made lowercase.
    headerautokey = models.ForeignKey(Pi, models.DO_NOTHING, db_column='HeaderAutoKey')  # Field name made lowercase.
    itemcode = models.ForeignKey(Item, models.DO_NOTHING, db_column='ItemCode', to_field='ItemCode')  # Field name made lowercase.
    location = models.ForeignKey(Location, models.DO_NOTHING, db_column='Location', to_field='Location')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'pidtl'


class Po(models.Model):
    autokey = models.CharField(db_column='AutoKey', primary_key=True, max_length=32)  # Field name made lowercase.
    docno = models.CharField(db_column='DocNo', max_length=20)  # Field name made lowercase.
    docdate = models.DateTimeField(db_column='DocDate')  # Field name made lowercase.
    creditorcode = models.CharField(db_column='CreditorCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    creditorname = models.CharField(db_column='CreditorName', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ref = models.CharField(db_column='Ref', max_length=40, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=80, blank=True, null=True)  # Field name made lowercase.
    displayterm = models.ForeignKey('Terms', models.DO_NOTHING, db_column='DisplayTerm')  # Field name made lowercase.
    purchaseagent = models.CharField(db_column='PurchaseAgent', max_length=12, blank=True, null=True)  # Field name made lowercase.
    invaddr1 = models.CharField(db_column='InvAddr1', max_length=40, blank=True, null=True)  # Field name made lowercase.
    invaddr2 = models.CharField(db_column='InvAddr2', max_length=40, blank=True, null=True)  # Field name made lowercase.
    invaddr3 = models.CharField(db_column='InvAddr3', max_length=40, blank=True, null=True)  # Field name made lowercase.
    invaddr4 = models.CharField(db_column='InvAddr4', max_length=40, blank=True, null=True)  # Field name made lowercase.
    phone1 = models.CharField(db_column='Phone1', max_length=25, blank=True, null=True)  # Field name made lowercase.
    fax1 = models.CharField(db_column='Fax1', max_length=25, blank=True, null=True)  # Field name made lowercase.
    attention = models.CharField(db_column='Attention', max_length=40, blank=True, null=True)  # Field name made lowercase.
    branchcode = models.CharField(db_column='BranchCode', max_length=20, blank=True, null=True)  # Field name made lowercase.
    deliveraddr1 = models.CharField(db_column='DeliverAddr1', max_length=40, blank=True, null=True)  # Field name made lowercase.
    deliveraddr2 = models.CharField(db_column='DeliverAddr2', max_length=40, blank=True, null=True)  # Field name made lowercase.
    deliveraddr3 = models.CharField(db_column='DeliverAddr3', max_length=40, blank=True, null=True)  # Field name made lowercase.
    deliveraddr4 = models.CharField(db_column='DeliverAddr4', max_length=40, blank=True, null=True)  # Field name made lowercase.
    deliverphone1 = models.CharField(db_column='DeliverPhone1', max_length=25, blank=True, null=True)  # Field name made lowercase.
    deliverfax1 = models.CharField(db_column='DeliverFax1', max_length=25, blank=True, null=True)  # Field name made lowercase.
    delivercontact = models.CharField(db_column='DeliverContact', max_length=40, blank=True, null=True)  # Field name made lowercase.
    total = models.DecimalField(db_column='Total', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer1param = models.DecimalField(db_column='Footer1Param', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer1amt = models.DecimalField(db_column='Footer1Amt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer1localamt = models.DecimalField(db_column='Footer1LocalAmt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer1taxtype = models.CharField(db_column='Footer1TaxType', max_length=14, blank=True, null=True)  # Field name made lowercase.
    footer2param = models.DecimalField(db_column='Footer2Param', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer2amt = models.DecimalField(db_column='Footer2Amt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer2localamt = models.DecimalField(db_column='Footer2LocalAmt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer2taxtype = models.CharField(db_column='Footer2TaxType', max_length=14, blank=True, null=True)  # Field name made lowercase.
    footer3param = models.DecimalField(db_column='Footer3Param', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer3amt = models.DecimalField(db_column='Footer3Amt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer3localamt = models.DecimalField(db_column='Footer3LocalAmt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer3taxtype = models.CharField(db_column='Footer3TaxType', max_length=14, blank=True, null=True)  # Field name made lowercase.
    crrencycode = models.CharField(db_column='CrrencyCode', max_length=5)  # Field name made lowercase.
    currencyrate = models.DecimalField(db_column='CurrencyRate', max_digits=19, decimal_places=12)  # Field name made lowercase.
    nettotal = models.DecimalField(db_column='NetTotal', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    localnettotal = models.DecimalField(db_column='LocalNetTotal', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    tax = models.DecimalField(db_column='Tax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    localtax = models.DecimalField(db_column='LocalTax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    referdepositdockey = models.BigIntegerField(db_column='ReferDepositDocKey', blank=True, null=True)  # Field name made lowercase.
    transferable = models.CharField(db_column='Transferable', max_length=1)  # Field name made lowercase.
    todoctype = models.CharField(db_column='ToDocType', max_length=2, blank=True, null=True)  # Field name made lowercase.
    todockey = models.BigIntegerField(db_column='ToDocKey', blank=True, null=True)  # Field name made lowercase.
    note = models.CharField(db_column='Note', max_length=255, blank=True, null=True)  # Field name made lowercase.
    remark1 = models.CharField(db_column='Remark1', max_length=40, blank=True, null=True)  # Field name made lowercase.
    remark2 = models.CharField(db_column='Remark2', max_length=40, blank=True, null=True)  # Field name made lowercase.
    remark3 = models.CharField(db_column='Remark3', max_length=40, blank=True, null=True)  # Field name made lowercase.
    remark4 = models.CharField(db_column='Remark4', max_length=40, blank=True, null=True)  # Field name made lowercase.
    printcount = models.SmallIntegerField(db_column='PrintCOunt')  # Field name made lowercase.
    cancelled = models.CharField(db_column='Cancelled', max_length=1)  # Field name made lowercase.
    lastmodified = models.DateTimeField(db_column='LastModified')  # Field name made lowercase.
    lastmodifieduserid = models.CharField(db_column='LastModifiedUserID', max_length=10)  # Field name made lowercase.
    createdtimestamp = models.DateTimeField(db_column='CreatedTimeStamp')  # Field name made lowercase.
    createduserid = models.CharField(db_column='CreatedUserID', max_length=10)  # Field name made lowercase.
    externallink = models.CharField(db_column='ExternalLink', max_length=255, blank=True, null=True)  # Field name made lowercase.
    refdocno = models.CharField(db_column='RefDocNo', max_length=20, blank=True, null=True)  # Field name made lowercase.
    cantransferbyvalue = models.CharField(db_column='CanTransferByValue', max_length=1, blank=True, null=True)  # Field name made lowercase.
    transferedamt = models.DecimalField(db_column='TransferedAmt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    cansync = models.CharField(db_column='CanSync', max_length=1)  # Field name made lowercase.
    lastupdate = models.IntegerField(db_column='LastUpdate')  # Field name made lowercase.
    todtlkey = models.BigIntegerField(db_column='ToDtlKey', blank=True, null=True)  # Field name made lowercase.
    fulltransferoption = models.CharField(db_column='FullTransferOption', max_length=1, blank=True, null=True)  # Field name made lowercase.
    shipvia = models.CharField(db_column='ShipVia', max_length=20, blank=True, null=True)  # Field name made lowercase.
    shipinfo = models.CharField(db_column='ShipInfo', max_length=40, blank=True, null=True)  # Field name made lowercase.
    purchaselocation = models.CharField(db_column='PurchaseLocation', max_length=8, blank=True, null=True)  # Field name made lowercase.
    footer1tax = models.DecimalField(db_column='Footer1Tax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer1localtax = models.DecimalField(db_column='Footer1LocalTax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer2tax = models.DecimalField(db_column='Footer2Tax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer2localtax = models.DecimalField(db_column='Footer2LocalTax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer3tax = models.DecimalField(db_column='Footer3Tax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer3localtax = models.DecimalField(db_column='Footer3LocalTax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    extax = models.DecimalField(db_column='ExTax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    localextax = models.DecimalField(db_column='LocalExTax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    analysisnettotal = models.DecimalField(db_column='AnalysisNetTotal', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    localanalysisnettotal = models.DecimalField(db_column='LocalAnalysisNetTotal', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    guid = models.CharField(db_column='Guid', unique=True, max_length=32)  # Field name made lowercase.
    totaxcurrencyrate = models.DecimalField(db_column='ToTaxCurrencyRate', max_digits=19, decimal_places=12)  # Field name made lowercase.
    calcdiscountonunitprice = models.CharField(db_column='CalcDiscountOnUnitPrice', max_length=1, blank=True, null=True)  # Field name made lowercase.
    totalextax = models.DecimalField(db_column='TotalExTax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    taxableamt = models.DecimalField(db_column='TaxableAmt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    inclusivetax = models.CharField(db_column='InclusiveTax', max_length=1)  # Field name made lowercase.
    footer1taxrate = models.DecimalField(db_column='Footer1TaxRate', max_digits=18, decimal_places=6, blank=True, null=True)  # Field name made lowercase.
    footer2taxrate = models.DecimalField(db_column='Footer2TaxRate', max_digits=18, decimal_places=6, blank=True, null=True)  # Field name made lowercase.
    footer3taxrate = models.DecimalField(db_column='Footer3TaxRate', max_digits=18, decimal_places=6, blank=True, null=True)  # Field name made lowercase.
    roundingmethod = models.IntegerField(db_column='RoundingMethod')  # Field name made lowercase.
    localtaxableamt = models.DecimalField(db_column='LocalTaxableAmt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    taxcurrencytax = models.DecimalField(db_column='TaxCurrencyTax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    taxcurrencytaxableamt = models.DecimalField(db_column='TaxCurrencyTaxableAmt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    isroundadj = models.CharField(db_column='IsRoundAdj', max_length=1)  # Field name made lowercase.
    roundedadj = models.DecimalField(db_column='RoundedAdj', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    finaltotal = models.DecimalField(db_column='FinalTotal', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    taxbranchid = models.CharField(db_column='TaxBranchID', max_length=8, blank=True, null=True)  # Field name made lowercase.
    branchautokey = models.ForeignKey(Branch, models.DO_NOTHING, db_column='BranchAutoKey')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'po'


class Podtl(models.Model):
    autokey = models.CharField(db_column='AutoKey', primary_key=True, max_length=32)  # Field name made lowercase.
    seq = models.IntegerField(db_column='Seq')  # Field name made lowercase.
    indent = models.SmallIntegerField(db_column='Indent', blank=True, null=True)  # Field name made lowercase.
    fontstyle = models.CharField(db_column='FontStyle', max_length=8, blank=True, null=True)  # Field name made lowercase.
    mainitem = models.CharField(db_column='Mainitem', max_length=1)  # Field name made lowercase.
    numbering = models.CharField(db_column='Numbering', max_length=6, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=100, blank=True, null=True)  # Field name made lowercase.
    furtherdescription = models.CharField(db_column='FurtherDescription', max_length=255, blank=True, null=True)  # Field name made lowercase.
    projno = models.CharField(db_column='ProjNo', max_length=10, blank=True, null=True)  # Field name made lowercase.
    deptno = models.CharField(db_column='DeptNo', max_length=10, blank=True, null=True)  # Field name made lowercase.
    uom = models.CharField(db_column='UOM', max_length=8, blank=True, null=True)  # Field name made lowercase.
    useruom = models.CharField(db_column='UserUOM', max_length=8, blank=True, null=True)  # Field name made lowercase.
    qty = models.DecimalField(db_column='Qty', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    rate = models.DecimalField(db_column='Rate', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    smallestqty = models.DecimalField(db_column='SmallestQty', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    transferedqty = models.DecimalField(db_column='TransferedQty', max_digits=25, decimal_places=8)  # Field name made lowercase.
    focqty = models.DecimalField(db_column='FOCQty', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    foctransferedqty = models.DecimalField(db_column='FOCTransferedQty', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    smallestunitprice = models.DecimalField(db_column='SmallestUnitPrice', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    unitprice = models.DecimalField(db_column='UnitPrice', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    discount = models.CharField(db_column='Discount', max_length=20, blank=True, null=True)  # Field name made lowercase.
    discountamt = models.DecimalField(db_column='DiscountAmt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    taxtype = models.CharField(db_column='TaxType', max_length=14, blank=True, null=True)  # Field name made lowercase.
    tax = models.DecimalField(db_column='Tax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    subtotal = models.DecimalField(db_column='SubTotal', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    localsubtotal = models.DecimalField(db_column='LocalSubTotal', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    transferable = models.CharField(db_column='Transferable', max_length=1)  # Field name made lowercase.
    printout = models.CharField(db_column='PrintOut', max_length=1)  # Field name made lowercase.
    dtltype = models.CharField(db_column='DTLType', max_length=1, blank=True, null=True)  # Field name made lowercase.
    calcbypercent = models.DecimalField(db_column='CalcByPercent', max_digits=18, decimal_places=6, blank=True, null=True)  # Field name made lowercase.
    addtosubtotal = models.CharField(db_column='AddToSubTotal', max_length=1)  # Field name made lowercase.
    fromdoctype = models.CharField(db_column='FromDocType', max_length=2, blank=True, null=True)  # Field name made lowercase.
    fromdocno = models.CharField(db_column='FromDocNo', max_length=255, blank=True, null=True)  # Field name made lowercase.
    fromdocdtlkey = models.BigIntegerField(db_column='FromDocDtlKey', blank=True, null=True)  # Field name made lowercase.
    fulltransferoption = models.CharField(db_column='FullTransferOption', max_length=1, blank=True, null=True)  # Field name made lowercase.
    fulltransferfromdoclist = models.CharField(db_column='FullTransferFromDocList', max_length=255, blank=True, null=True)  # Field name made lowercase.
    fromsodtl = models.BigIntegerField(db_column='FromSODtl', blank=True, null=True)  # Field name made lowercase.
    estimateddeliverydate = models.CharField(db_column='EstimatedDeliveryDate', max_length=20, blank=True, null=True)  # Field name made lowercase.
    fromaodtlkey = models.BigIntegerField(db_column='FromAODtlKey', blank=True, null=True)  # Field name made lowercase.
    packagedockey = models.BigIntegerField(db_column='PackageDocKey', blank=True, null=True)  # Field name made lowercase.
    parentdtlkey = models.BigIntegerField(db_column='ParentDtlKey', blank=True, null=True)  # Field name made lowercase.
    subqty = models.DecimalField(db_column='SubQty', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    subtotalextax = models.DecimalField(db_column='SubTotalExTax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    localtax = models.DecimalField(db_column='LocalTax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    batchno = models.CharField(db_column='BatchNo', max_length=20, blank=True, null=True)  # Field name made lowercase.
    guid = models.CharField(db_column='Guid', unique=True, max_length=32)  # Field name made lowercase.
    fromsodoclist = models.CharField(db_column='FromSODocList', max_length=255, blank=True, null=True)  # Field name made lowercase.
    deliverydate = models.DateTimeField(db_column='DeliveryDate', blank=True, null=True)  # Field name made lowercase.
    taxableamt = models.DecimalField(db_column='TaxableAmt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    taxadjustment = models.DecimalField(db_column='TaxAdjustment', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    localsubtotalextax = models.DecimalField(db_column='LocalSubTotalExTax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    extradiscountamt = models.DecimalField(db_column='ExtraDiscountAmt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    taxrate = models.DecimalField(db_column='TaxRate', max_digits=18, decimal_places=6, blank=True, null=True)  # Field name made lowercase.
    localtaxadjustment = models.DecimalField(db_column='LocalTaxAdjustment', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    localtaxableamt = models.DecimalField(db_column='LocalTaxableAmt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    taxcurrencytax = models.DecimalField(db_column='TaxCurrencyTax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    taxcurrencytaxableamt = models.DecimalField(db_column='TaxCurrencyTaxableAmt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    salesexamtionno = models.CharField(db_column='SalesExamtionNo', max_length=60, blank=True, null=True)  # Field name made lowercase.
    desc2 = models.CharField(db_column='Desc2', max_length=100, blank=True, null=True)  # Field name made lowercase.
    itemcode = models.ForeignKey(Item, models.DO_NOTHING, db_column='ItemCode', blank=True, null=True)  # Field name made lowercase.
    location = models.ForeignKey(Location, models.DO_NOTHING, db_column='Location', blank=True, null=True)  # Field name made lowercase.
    poautokey = models.ForeignKey(Po, models.DO_NOTHING, db_column='POAutoKey')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'podtl'


class Pr(models.Model):
    autokey = models.CharField(db_column='AutoKey', primary_key=True, max_length=32)  # Field name made lowercase.
    docno = models.CharField(db_column='DocNo', max_length=20)  # Field name made lowercase.
    docdate = models.DateTimeField(db_column='DocDate')  # Field name made lowercase.
    creditorcode = models.ForeignKey(Creditor, models.DO_NOTHING, db_column='CreditorCode', to_field='AccNo')  # Field name made lowercase.
    creditorname = models.ForeignKey(Creditor, models.DO_NOTHING, db_column='CreditorName', to_field='CompanyName', related_name='pr_creditorname_set')  # Field name made lowercase.
    ref = models.CharField(db_column='Ref', max_length=40, blank=True, null=True)  # Field name made lowercase.
    suppliercnno = models.CharField(db_column='SupplierCNNo', max_length=20, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=80, blank=True, null=True)  # Field name made lowercase.
    purchaseagent = models.CharField(db_column='PurchaseAgent', max_length=12, blank=True, null=True)  # Field name made lowercase.
    invaddr1 = models.CharField(db_column='InvAddr1', max_length=40, blank=True, null=True)  # Field name made lowercase.
    invaddr2 = models.CharField(db_column='InvAddr2', max_length=40, blank=True, null=True)  # Field name made lowercase.
    invaddr3 = models.CharField(db_column='InvAddr3', max_length=40, blank=True, null=True)  # Field name made lowercase.
    invaddr4 = models.CharField(db_column='InvAddr4', max_length=40, blank=True, null=True)  # Field name made lowercase.
    phone1 = models.CharField(db_column='Phone1', max_length=25, blank=True, null=True)  # Field name made lowercase.
    fax1 = models.CharField(db_column='Fax1', max_length=25, blank=True, null=True)  # Field name made lowercase.
    attention = models.CharField(db_column='Attention', max_length=40, blank=True, null=True)  # Field name made lowercase.
    branchcode = models.CharField(db_column='BranchCode', max_length=20, blank=True, null=True)  # Field name made lowercase.
    total = models.DecimalField(db_column='Total', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer1param = models.DecimalField(db_column='Footer1Param', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer1amt = models.DecimalField(db_column='Footer1Amt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer1localamt = models.DecimalField(db_column='Footer1LocalAmt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer1taxtype = models.CharField(db_column='Footer1TaxType', max_length=14, blank=True, null=True)  # Field name made lowercase.
    footer2param = models.DecimalField(db_column='Footer2Param', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer2amt = models.DecimalField(db_column='Footer2Amt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer2localamt = models.DecimalField(db_column='Footer2LocalAmt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer2taxtype = models.CharField(db_column='Footer2TaxType', max_length=14, blank=True, null=True)  # Field name made lowercase.
    footer3param = models.DecimalField(db_column='Footer3Param', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer3amt = models.DecimalField(db_column='Footer3Amt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer3localamt = models.DecimalField(db_column='Footer3LocalAmt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer3taxtype = models.CharField(db_column='Footer3TaxType', max_length=14, blank=True, null=True)  # Field name made lowercase.
    crrencycode = models.CharField(db_column='CrrencyCode', max_length=5)  # Field name made lowercase.
    currencyrate = models.DecimalField(db_column='CurrencyRate', max_digits=19, decimal_places=2)  # Field name made lowercase.
    nettotal = models.DecimalField(db_column='NetTotal', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    localnettotal = models.DecimalField(db_column='LocalNetTotal', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    tax = models.DecimalField(db_column='Tax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    localtax = models.DecimalField(db_column='LocalTax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    posttostock = models.CharField(db_column='PostToStock', max_length=1)  # Field name made lowercase.
    posttogl = models.CharField(db_column='PostToGL', max_length=1)  # Field name made lowercase.
    referdockey = models.BigIntegerField(db_column='ReferDocKey', blank=True, null=True)  # Field name made lowercase.
    note = models.CharField(db_column='Note', max_length=255, blank=True, null=True)  # Field name made lowercase.
    remark1 = models.CharField(db_column='Remark1', max_length=40, blank=True, null=True)  # Field name made lowercase.
    remark2 = models.CharField(db_column='Remark2', max_length=40, blank=True, null=True)  # Field name made lowercase.
    remark3 = models.CharField(db_column='Remark3', max_length=40, blank=True, null=True)  # Field name made lowercase.
    remark4 = models.CharField(db_column='Remark4', max_length=40, blank=True, null=True)  # Field name made lowercase.
    printcount = models.SmallIntegerField(db_column='PrintCOunt')  # Field name made lowercase.
    cancelled = models.CharField(db_column='Cancelled', max_length=1)  # Field name made lowercase.
    lastmodified = models.DateTimeField(db_column='LastModified')  # Field name made lowercase.
    lastmodifieduserid = models.CharField(db_column='LastModifiedUserID', max_length=10)  # Field name made lowercase.
    createdtimestamp = models.DateTimeField(db_column='CreatedTimeStamp')  # Field name made lowercase.
    createduserid = models.CharField(db_column='CreatedUserID', max_length=10)  # Field name made lowercase.
    externallink = models.CharField(db_column='ExternalLink', max_length=255, blank=True, null=True)  # Field name made lowercase.
    refdocno = models.CharField(db_column='RefDocNo', max_length=20, blank=True, null=True)  # Field name made lowercase.
    cansync = models.CharField(db_column='CanSync', max_length=1)  # Field name made lowercase.
    lastupdate = models.IntegerField(db_column='LastUpdate')  # Field name made lowercase.
    refno2 = models.CharField(db_column='RefNo2', max_length=20, blank=True, null=True)  # Field name made lowercase.
    purchaselocation = models.CharField(db_column='PurchaseLocation', max_length=8, blank=True, null=True)  # Field name made lowercase.
    footer1tax = models.DecimalField(db_column='Footer1Tax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer1localtax = models.DecimalField(db_column='Footer1LocalTax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer2tax = models.DecimalField(db_column='Footer2Tax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer2localtax = models.DecimalField(db_column='Footer2LocalTax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer3tax = models.DecimalField(db_column='Footer3Tax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer3localtax = models.DecimalField(db_column='Footer3LocalTax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    extax = models.DecimalField(db_column='ExTax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    localextax = models.DecimalField(db_column='LocalExTax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    analysisnettotal = models.DecimalField(db_column='AnalysisNetTotal', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    localanalysisnettotal = models.DecimalField(db_column='LocalAnalysisNetTotal', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    guid = models.CharField(db_column='Guid', unique=True, max_length=32)  # Field name made lowercase.
    totaxcurrencyrate = models.DecimalField(db_column='ToTaxCurrencyRate', max_digits=19, decimal_places=12)  # Field name made lowercase.
    calcdiscountonunitprice = models.CharField(db_column='CalcDiscountOnUnitPrice', max_length=1, blank=True, null=True)  # Field name made lowercase.
    taxdocno = models.CharField(db_column='TaxDocNo', max_length=20, blank=True, null=True)  # Field name made lowercase.
    totalextax = models.DecimalField(db_column='TotalExTax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    taxableamt = models.DecimalField(db_column='TaxableAmt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    supplierinvoiceno = models.CharField(db_column='SupplierInvoiceNo', max_length=40, blank=True, null=True)  # Field name made lowercase.
    reason = models.CharField(db_column='Reason', max_length=80, blank=True, null=True)  # Field name made lowercase.
    inclusivetax = models.CharField(db_column='InclusiveTax', max_length=1)  # Field name made lowercase.
    footer1taxrate = models.DecimalField(db_column='Footer1TaxRate', max_digits=18, decimal_places=6, blank=True, null=True)  # Field name made lowercase.
    footer2taxrate = models.DecimalField(db_column='Footer2TaxRate', max_digits=18, decimal_places=6, blank=True, null=True)  # Field name made lowercase.
    footer3taxrate = models.DecimalField(db_column='Footer3TaxRate', max_digits=18, decimal_places=6, blank=True, null=True)  # Field name made lowercase.
    taxdate = models.DateTimeField(db_column='TaxDate', blank=True, null=True)  # Field name made lowercase.
    isroundadj = models.CharField(db_column='IsRoundAdj', max_length=1)  # Field name made lowercase.
    roundedadj = models.DecimalField(db_column='RoundedAdj', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    finaltotal = models.DecimalField(db_column='FinalTotal', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    roundingmethod = models.IntegerField(db_column='RoundingMethod')  # Field name made lowercase.
    localtaxableamt = models.DecimalField(db_column='LocalTaxableAmt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    taxcurrencytax = models.DecimalField(db_column='TaxCurrencyTax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    taxcurrencytaxableamt = models.DecimalField(db_column='TaxCurrencyTaxableAmt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    docdate2 = models.DateTimeField(db_column='DocDate2', blank=True, null=True)  # Field name made lowercase.
    taxbranchid = models.CharField(db_column='TaxBranchID', max_length=8, blank=True, null=True)  # Field name made lowercase.
    branchautokey = models.ForeignKey(Branch, models.DO_NOTHING, db_column='BranchAutoKey')  # Field name made lowercase.
    displayterm = models.ForeignKey('Terms', models.DO_NOTHING, db_column='DisplayTerm', to_field='DisplayTerm')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'pr'


class Prdtl(models.Model):
    autokey = models.CharField(db_column='AutoKey', primary_key=True, max_length=32)  # Field name made lowercase.
    focdtlkey = models.BigIntegerField(db_column='FOCDtlKey', blank=True, null=True)  # Field name made lowercase.
    seq = models.IntegerField(db_column='Seq')  # Field name made lowercase.
    indent = models.SmallIntegerField(db_column='Indent', blank=True, null=True)  # Field name made lowercase.
    fontstyle = models.CharField(db_column='FontStyle', max_length=8, blank=True, null=True)  # Field name made lowercase.
    mainitem = models.CharField(db_column='Mainitem', max_length=1)  # Field name made lowercase.
    numbering = models.CharField(db_column='Numbering', max_length=6, blank=True, null=True)  # Field name made lowercase.
    batchno = models.CharField(db_column='BatchNo', max_length=20, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=100, blank=True, null=True)  # Field name made lowercase.
    furtherdescription = models.CharField(db_column='FurtherDescription', max_length=255, blank=True, null=True)  # Field name made lowercase.
    projno = models.CharField(db_column='ProjNo', max_length=10, blank=True, null=True)  # Field name made lowercase.
    deptno = models.CharField(db_column='DeptNo', max_length=10, blank=True, null=True)  # Field name made lowercase.
    yourdono = models.CharField(db_column='YourDONo', max_length=20, blank=True, null=True)  # Field name made lowercase.
    yourdodate = models.DateTimeField(db_column='YourDODate', blank=True, null=True)  # Field name made lowercase.
    ourpono = models.CharField(db_column='OurPONo', max_length=20, blank=True, null=True)  # Field name made lowercase.
    ourpodate = models.DateTimeField(db_column='OurPODate', blank=True, null=True)  # Field name made lowercase.
    posttostockdate = models.DateTimeField(db_column='PostToStockDate', blank=True, null=True)  # Field name made lowercase.
    uom = models.CharField(db_column='UOM', max_length=8, blank=True, null=True)  # Field name made lowercase.
    useruom = models.CharField(db_column='UserUOM', max_length=8, blank=True, null=True)  # Field name made lowercase.
    qty = models.DecimalField(db_column='Qty', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    rate = models.DecimalField(db_column='Rate', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    smallestqty = models.DecimalField(db_column='SmallestQty', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    focqty = models.DecimalField(db_column='FOCQty', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    smallestunitprice = models.DecimalField(db_column='SmallestUnitPrice', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    unitprice = models.DecimalField(db_column='UnitPrice', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    discount = models.CharField(db_column='Discount', max_length=20, blank=True, null=True)  # Field name made lowercase.
    discountamt = models.DecimalField(db_column='DiscountAmt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    taxtype = models.CharField(db_column='TaxType', max_length=14, blank=True, null=True)  # Field name made lowercase.
    tax = models.DecimalField(db_column='Tax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    subtotal = models.DecimalField(db_column='SubTotal', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    localsubtotal = models.DecimalField(db_column='LocalSubTotal', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    printout = models.CharField(db_column='PrintOut', max_length=1)  # Field name made lowercase.
    dtltype = models.CharField(db_column='DTLType', max_length=1, blank=True, null=True)  # Field name made lowercase.
    calcbypercent = models.DecimalField(db_column='CalcByPercent', max_digits=18, decimal_places=6, blank=True, null=True)  # Field name made lowercase.
    addtosubtotal = models.CharField(db_column='AddToSubTotal', max_length=1)  # Field name made lowercase.
    fromdoctype = models.CharField(db_column='FromDocType', max_length=2, blank=True, null=True)  # Field name made lowercase.
    fromdocno = models.CharField(db_column='FromDocNo', max_length=255, blank=True, null=True)  # Field name made lowercase.
    fromdocdtlkey = models.BigIntegerField(db_column='FromDocDtlKey', blank=True, null=True)  # Field name made lowercase.
    fulltransferoption = models.CharField(db_column='FullTransferOption', max_length=1, blank=True, null=True)  # Field name made lowercase.
    accno = models.CharField(db_column='AccNo', max_length=12, blank=True, null=True)  # Field name made lowercase.
    fulltransferfromdoclist = models.CharField(db_column='FullTransferFromDocList', max_length=255, blank=True, null=True)  # Field name made lowercase.
    serialnolist = models.CharField(db_column='SerialNoList', max_length=255, blank=True, null=True)  # Field name made lowercase.
    packagedockey = models.BigIntegerField(db_column='PackageDocKey', blank=True, null=True)  # Field name made lowercase.
    parentdtlkey = models.BigIntegerField(db_column='ParentDtlKey', blank=True, null=True)  # Field name made lowercase.
    subqty = models.DecimalField(db_column='SubQty', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    subtotalextax = models.DecimalField(db_column='SubTotalExTax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    localtax = models.DecimalField(db_column='LocalTax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    guid = models.CharField(db_column='Guid', unique=True, max_length=32)  # Field name made lowercase.
    goodsreturn = models.CharField(db_column='GoodsReturn', max_length=1, blank=True, null=True)  # Field name made lowercase.
    taxpermitno = models.CharField(db_column='TaxPermitNo', max_length=20, blank=True, null=True)  # Field name made lowercase.
    taxableamt = models.DecimalField(db_column='TaxableAmt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    taxadjustment = models.DecimalField(db_column='TaxAdjustment', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    localsubtotalextax = models.DecimalField(db_column='LocalSubTotalExTax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    extradiscountamt = models.DecimalField(db_column='ExtraDiscountAmt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    taxrate = models.DecimalField(db_column='TaxRate', max_digits=18, decimal_places=6, blank=True, null=True)  # Field name made lowercase.
    localtaxadjustment = models.DecimalField(db_column='LocalTaxAdjustment', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    localtaxableamt = models.DecimalField(db_column='LocalTaxableAmt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    taxcurrencytax = models.DecimalField(db_column='TaxCurrencyTax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    taxcurrencytaxableamt = models.DecimalField(db_column='TaxCurrencyTaxableAmt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    salesexamtionno = models.CharField(db_column='SalesExamtionNo', max_length=60, blank=True, null=True)  # Field name made lowercase.
    supplypurchase = models.CharField(db_column='SupplyPurchase', max_length=1, blank=True, null=True)  # Field name made lowercase.
    tariffcode = models.CharField(db_column='TariffCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    desc2 = models.CharField(db_column='Desc2', max_length=100, blank=True, null=True)  # Field name made lowercase.
    itemcode = models.ForeignKey(Item, models.DO_NOTHING, db_column='ItemCode', to_field='ItemCode', blank=True, null=True)  # Field name made lowercase.
    location = models.ForeignKey(Location, models.DO_NOTHING, db_column='Location', to_field='Location', blank=True, null=True)  # Field name made lowercase.
    prautokey = models.ForeignKey(Pr, models.DO_NOTHING, db_column='PRAutoKey')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'prdtl'


class Salesagent(models.Model):
    autokey = models.CharField(db_column='Autokey', primary_key=True, max_length=32)  # Field name made lowercase.
    salesagent = models.CharField(db_column='SalesAgent', unique=True, max_length=40)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=40, blank=True, null=True)  # Field name made lowercase.
    desc2 = models.CharField(db_column='Desc2', max_length=80, blank=True, null=True)  # Field name made lowercase.
    isactive = models.CharField(db_column='IsActive', max_length=1)  # Field name made lowercase.
    lastupdate = models.IntegerField(db_column='LastUpdate')  # Field name made lowercase.
    signature = models.TextField(db_column='Signature', blank=True, null=True)  # Field name made lowercase.
    guid = models.CharField(db_column='Guid', unique=True, max_length=32)  # Field name made lowercase.
    emailaddress = models.CharField(db_column='EmailAddress', max_length=200, blank=True, null=True)  # Field name made lowercase.
    approveremailaddress = models.CharField(db_column='ApproverEmailAddress', max_length=200, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'salesagent'


class So(models.Model):
    autokey = models.CharField(db_column='Autokey', primary_key=True, max_length=32)  # Field name made lowercase.
    docno = models.CharField(db_column='DocNo', max_length=20)  # Field name made lowercase.
    docdate = models.DateTimeField(db_column='DocDate')  # Field name made lowercase.
    debtorcode = models.CharField(db_column='DebtorCode', max_length=12, blank=True, null=True)  # Field name made lowercase.
    creditorname = models.CharField(db_column='CreditorName', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ref = models.CharField(db_column='Ref', max_length=40, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=80, blank=True, null=True)  # Field name made lowercase.
    salesagent = models.CharField(db_column='SalesAgent', max_length=12, blank=True, null=True)  # Field name made lowercase.
    invaddr1 = models.CharField(db_column='InvAddr1', max_length=40, blank=True, null=True)  # Field name made lowercase.
    invaddr2 = models.CharField(db_column='InvAddr2', max_length=40, blank=True, null=True)  # Field name made lowercase.
    invaddr3 = models.CharField(db_column='InvAddr3', max_length=40, blank=True, null=True)  # Field name made lowercase.
    invaddr4 = models.CharField(db_column='InvAddr4', max_length=40, blank=True, null=True)  # Field name made lowercase.
    phone1 = models.CharField(db_column='Phone1', max_length=25, blank=True, null=True)  # Field name made lowercase.
    fax1 = models.CharField(db_column='Fax1', max_length=25, blank=True, null=True)  # Field name made lowercase.
    attention = models.CharField(db_column='Attention', max_length=40, blank=True, null=True)  # Field name made lowercase.
    branchcode = models.CharField(db_column='BranchCode', max_length=20, blank=True, null=True)  # Field name made lowercase.
    deliveraddr1 = models.CharField(db_column='DeliverAddr1', max_length=40, blank=True, null=True)  # Field name made lowercase.
    deliveraddr2 = models.CharField(db_column='DeliverAddr2', max_length=40, blank=True, null=True)  # Field name made lowercase.
    deliveraddr3 = models.CharField(db_column='DeliverAddr3', max_length=40, blank=True, null=True)  # Field name made lowercase.
    deliveraddr4 = models.CharField(db_column='DeliverAddr4', max_length=40, blank=True, null=True)  # Field name made lowercase.
    deliverphone1 = models.CharField(db_column='DeliverPhone1', max_length=25, blank=True, null=True)  # Field name made lowercase.
    deliverfax1 = models.CharField(db_column='DeliverFax1', max_length=25, blank=True, null=True)  # Field name made lowercase.
    delivercontact = models.CharField(db_column='DeliverContact', max_length=40, blank=True, null=True)  # Field name made lowercase.
    salesexemptionno = models.CharField(db_column='SalesExemptionNo', max_length=60, blank=True, null=True)  # Field name made lowercase.
    salesexemptionexpirydate = models.DateTimeField(db_column='SalesExemptionExpiryDate', blank=True, null=True)  # Field name made lowercase.
    total = models.DecimalField(db_column='Total', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer1param = models.DecimalField(db_column='Footer1Param', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer1amt = models.DecimalField(db_column='Footer1Amt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer1localamt = models.DecimalField(db_column='Footer1LocalAmt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer1taxtype = models.CharField(db_column='Footer1TaxType', max_length=14, blank=True, null=True)  # Field name made lowercase.
    footer2param = models.DecimalField(db_column='Footer2Param', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer2amt = models.DecimalField(db_column='Footer2Amt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer2localamt = models.DecimalField(db_column='Footer2LocalAmt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer2taxtype = models.CharField(db_column='Footer2TaxType', max_length=14, blank=True, null=True)  # Field name made lowercase.
    footer3param = models.DecimalField(db_column='Footer3Param', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer3amt = models.DecimalField(db_column='Footer3Amt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer3localamt = models.DecimalField(db_column='Footer3LocalAmt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer3taxtype = models.CharField(db_column='Footer3TaxType', max_length=14, blank=True, null=True)  # Field name made lowercase.
    crrencycode = models.CharField(db_column='CrrencyCode', max_length=5)  # Field name made lowercase.
    currencyrate = models.DecimalField(db_column='CurrencyRate', max_digits=19, decimal_places=2)  # Field name made lowercase.
    nettotal = models.DecimalField(db_column='NetTotal', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    localnettotal = models.DecimalField(db_column='LocalNetTotal', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    analysisnettotal = models.DecimalField(db_column='AnalysisNetTotal', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    localanalysisnettotal = models.DecimalField(db_column='LocalAnalysisNetTotal', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    tax = models.DecimalField(db_column='Tax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    localtax = models.DecimalField(db_column='LocalTax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    referdepositdockey = models.BigIntegerField(db_column='ReferDepositDocKey', blank=True, null=True)  # Field name made lowercase.
    transferable = models.CharField(db_column='Transferable', max_length=1)  # Field name made lowercase.
    todoctype = models.CharField(db_column='ToDocType', max_length=2, blank=True, null=True)  # Field name made lowercase.
    todockey = models.BigIntegerField(db_column='ToDocKey', blank=True, null=True)  # Field name made lowercase.
    note = models.CharField(db_column='Note', max_length=255, blank=True, null=True)  # Field name made lowercase.
    remark1 = models.CharField(db_column='Remark1', max_length=40, blank=True, null=True)  # Field name made lowercase.
    remark2 = models.CharField(db_column='Remark2', max_length=40, blank=True, null=True)  # Field name made lowercase.
    remark3 = models.CharField(db_column='Remark3', max_length=40, blank=True, null=True)  # Field name made lowercase.
    remark4 = models.CharField(db_column='Remark4', max_length=40, blank=True, null=True)  # Field name made lowercase.
    printcount = models.SmallIntegerField(db_column='PrintCOunt')  # Field name made lowercase.
    cancelled = models.CharField(db_column='Cancelled', max_length=1)  # Field name made lowercase.
    lastmodified = models.DateTimeField(db_column='LastModified')  # Field name made lowercase.
    lastmodifieduserid = models.CharField(db_column='LastModifiedUserID', max_length=10)  # Field name made lowercase.
    createdtimestamp = models.DateTimeField(db_column='CreatedTimeStamp')  # Field name made lowercase.
    createduserid = models.CharField(db_column='CreatedUserID', max_length=10)  # Field name made lowercase.
    externallink = models.CharField(db_column='ExternalLink', max_length=255, blank=True, null=True)  # Field name made lowercase.
    refdocno = models.CharField(db_column='RefDocNo', max_length=20, blank=True, null=True)  # Field name made lowercase.
    cantransferbyvalue = models.CharField(db_column='CanTransferByValue', max_length=1, blank=True, null=True)  # Field name made lowercase.
    transferedamt = models.DecimalField(db_column='TransferedAmt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    cansync = models.CharField(db_column='CanSync', max_length=1)  # Field name made lowercase.
    lastupdate = models.IntegerField(db_column='LastUpdate')  # Field name made lowercase.
    todtlkey = models.BigIntegerField(db_column='ToDtlKey', blank=True, null=True)  # Field name made lowercase.
    fulltransferoption = models.CharField(db_column='FullTransferOption', max_length=1, blank=True, null=True)  # Field name made lowercase.
    shipvia = models.CharField(db_column='ShipVia', max_length=20, blank=True, null=True)  # Field name made lowercase.
    shipinfo = models.CharField(db_column='ShipInfo', max_length=40, blank=True, null=True)  # Field name made lowercase.
    saleslocation = models.CharField(db_column='SalesLocation', max_length=8, blank=True, null=True)  # Field name made lowercase.
    footer1tax = models.DecimalField(db_column='Footer1Tax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer1localtax = models.DecimalField(db_column='Footer1LocalTax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer2tax = models.DecimalField(db_column='Footer2Tax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer2localtax = models.DecimalField(db_column='Footer2LocalTax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer3tax = models.DecimalField(db_column='Footer3Tax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    footer3localtax = models.DecimalField(db_column='Footer3LocalTax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    extax = models.DecimalField(db_column='ExTax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    localextax = models.DecimalField(db_column='LocalExTax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    yourpono = models.CharField(db_column='YourPONo', max_length=25, blank=True, null=True)  # Field name made lowercase.
    yourpodate = models.DateTimeField(db_column='YourPODate', blank=True, null=True)  # Field name made lowercase.
    guid = models.CharField(db_column='Guid', unique=True, max_length=32)  # Field name made lowercase.
    totaxcurrencyrate = models.DecimalField(db_column='ToTaxCurrencyRate', max_digits=19, decimal_places=2)  # Field name made lowercase.
    calcdiscountonunitprice = models.CharField(db_column='CalcDiscountOnUnitPrice', max_length=1, blank=True, null=True)  # Field name made lowercase.
    totalextax = models.DecimalField(db_column='TotalExTax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    taxableamt = models.DecimalField(db_column='TaxableAmt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    inclusivetax = models.CharField(db_column='InclusiveTax', max_length=1)  # Field name made lowercase.
    footer1taxrate = models.DecimalField(db_column='Footer1TaxRate', max_digits=18, decimal_places=6, blank=True, null=True)  # Field name made lowercase.
    footer2taxrate = models.DecimalField(db_column='Footer2TaxRate', max_digits=18, decimal_places=6, blank=True, null=True)  # Field name made lowercase.
    footer3taxrate = models.DecimalField(db_column='Footer3TaxRate', max_digits=18, decimal_places=6, blank=True, null=True)  # Field name made lowercase.
    isroundadj = models.CharField(db_column='IsRoundAdj', max_length=1)  # Field name made lowercase.
    roundadj = models.DecimalField(db_column='RoundAdj', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    finaltotal = models.DecimalField(db_column='FinalTotal', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    roundingmethod = models.IntegerField(db_column='RoundingMethod')  # Field name made lowercase.
    localtaxableamt = models.DecimalField(db_column='LocalTaxableAmt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    taxcurrencytax = models.DecimalField(db_column='TaxCurrencyTax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    taxcurrencytaxableamt = models.DecimalField(db_column='TaxCurrencyTaxableAmt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    multiprice = models.CharField(db_column='MultiPrice', max_length=8, blank=True, null=True)  # Field name made lowercase.
    taxbranchid = models.CharField(db_column='TaxBranchID', max_length=8, blank=True, null=True)  # Field name made lowercase.
    branchautokey = models.ForeignKey(Branch, models.DO_NOTHING, db_column='BranchAutoKey')  # Field name made lowercase.
    displayterm = models.ForeignKey('Terms', models.DO_NOTHING, db_column='DisplayTerm')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'so'


class Sodtl(models.Model):
    autokey = models.CharField(db_column='Autokey', primary_key=True, max_length=32)  # Field name made lowercase.
    seq = models.IntegerField(db_column='Seq')  # Field name made lowercase.
    indent = models.SmallIntegerField(db_column='Indent', blank=True, null=True)  # Field name made lowercase.
    fontstyle = models.CharField(db_column='FontStyle', max_length=8, blank=True, null=True)  # Field name made lowercase.
    mainitem = models.CharField(db_column='Mainitem', max_length=1)  # Field name made lowercase.
    numbering = models.CharField(db_column='Numbering', max_length=6, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=100, blank=True, null=True)  # Field name made lowercase.
    furtherdescription = models.CharField(db_column='FurtherDescription', max_length=255, blank=True, null=True)  # Field name made lowercase.
    yourpono = models.CharField(db_column='YourPONo', max_length=25, blank=True, null=True)  # Field name made lowercase.
    yourpodate = models.DateTimeField(db_column='YourPODate', blank=True, null=True)  # Field name made lowercase.
    projno = models.CharField(db_column='ProjNo', max_length=10, blank=True, null=True)  # Field name made lowercase.
    deptno = models.CharField(db_column='DeptNo', max_length=10, blank=True, null=True)  # Field name made lowercase.
    uom = models.CharField(db_column='UOM', max_length=8, blank=True, null=True)  # Field name made lowercase.
    useruom = models.CharField(db_column='UserUOM', max_length=8, blank=True, null=True)  # Field name made lowercase.
    qty = models.DecimalField(db_column='Qty', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    rate = models.DecimalField(db_column='Rate', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    smallestqty = models.DecimalField(db_column='SmallestQty', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    transferedqty = models.DecimalField(db_column='TransferedQty', max_digits=25, decimal_places=8)  # Field name made lowercase.
    focqty = models.DecimalField(db_column='FOCQty', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    foctransferedqty = models.DecimalField(db_column='FOCTransferedQty', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    smallestunitprice = models.DecimalField(db_column='SmallestUnitPrice', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    unitprice = models.DecimalField(db_column='UnitPrice', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    discount = models.CharField(db_column='Discount', max_length=20, blank=True, null=True)  # Field name made lowercase.
    discountamt = models.DecimalField(db_column='DiscountAmt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    taxtype = models.CharField(db_column='TaxType', max_length=14, blank=True, null=True)  # Field name made lowercase.
    tax = models.DecimalField(db_column='Tax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    subtotal = models.DecimalField(db_column='SubTotal', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    localsubtotal = models.DecimalField(db_column='LocalSubTotal', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    transferable = models.CharField(db_column='Transferable', max_length=1)  # Field name made lowercase.
    printout = models.CharField(db_column='PrintOut', max_length=1)  # Field name made lowercase.
    dtltype = models.CharField(db_column='DTLType', max_length=1, blank=True, null=True)  # Field name made lowercase.
    calcbypercent = models.DecimalField(db_column='CalcByPercent', max_digits=18, decimal_places=6, blank=True, null=True)  # Field name made lowercase.
    addtosubtotal = models.CharField(db_column='AddToSubTotal', max_length=1)  # Field name made lowercase.
    fromdoctype = models.CharField(db_column='FromDocType', max_length=2, blank=True, null=True)  # Field name made lowercase.
    fromdocno = models.CharField(db_column='FromDocNo', max_length=255, blank=True, null=True)  # Field name made lowercase.
    fromdocdtlkey = models.BigIntegerField(db_column='FromDocDtlKey', blank=True, null=True)  # Field name made lowercase.
    fulltransferoption = models.CharField(db_column='FullTransferOption', max_length=1, blank=True, null=True)  # Field name made lowercase.
    fulltransferfromdoclist = models.CharField(db_column='FullTransferFromDocList', max_length=255, blank=True, null=True)  # Field name made lowercase.
    transferedpoqty = models.DecimalField(db_column='TransferedPOQty', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    foctransferedpoqty = models.DecimalField(db_column='FOCTransferedPOQty', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    estimateddeliverydate = models.CharField(db_column='EstimatedDeliveryDate', max_length=20, blank=True, null=True)  # Field name made lowercase.
    packagedockey = models.BigIntegerField(db_column='PackageDocKey', blank=True, null=True)  # Field name made lowercase.
    parentdtlkey = models.BigIntegerField(db_column='ParentDtlKey', blank=True, null=True)  # Field name made lowercase.
    transferedaoqty = models.DecimalField(db_column='TransferedAOQty', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    subqty = models.DecimalField(db_column='SubQty', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    stockreceived = models.CharField(db_column='StockReceived', max_length=1)  # Field name made lowercase.
    totalpurchaserequestqty = models.DecimalField(db_column='TotalPurchaseRequestQty', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    totaldeliveryrequestqty = models.DecimalField(db_column='TotalDeliveryRequestQty', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    totalassemblyorderrequestqty = models.DecimalField(db_column='TotalAssemblyOrderRequestQty', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    purchasestatus = models.SmallIntegerField(db_column='PurchaseStatus', blank=True, null=True)  # Field name made lowercase.
    deliverystatus = models.SmallIntegerField(db_column='DeliveryStatus', blank=True, null=True)  # Field name made lowercase.
    assemblyorderstatus = models.SmallIntegerField(db_column='AssemblyOrderStatus', blank=True, null=True)  # Field name made lowercase.
    lastopmodified = models.DateTimeField(db_column='LastOPModified', blank=True, null=True)  # Field name made lowercase.
    lastopmodifieduserid = models.CharField(db_column='LastOPModifiedUserID', max_length=10, blank=True, null=True)  # Field name made lowercase.
    lastdrpmodified = models.DateTimeField(db_column='LastDRPModified', blank=True, null=True)  # Field name made lowercase.
    lastaorpmodified = models.DateTimeField(db_column='LastAORPModified', blank=True, null=True)  # Field name made lowercase.
    lastdrpmodifieduserid = models.DateTimeField(db_column='LastDRPModifiedUserID', blank=True, null=True)  # Field name made lowercase.
    lastaorpmodifieduserid = models.DateTimeField(db_column='LastAORPModifiedUserID', blank=True, null=True)  # Field name made lowercase.
    subtotalextax = models.DecimalField(db_column='SubTotalExTax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    localtax = models.DecimalField(db_column='LocalTax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    batchno = models.CharField(db_column='BatchNo', max_length=20, blank=True, null=True)  # Field name made lowercase.
    guid = models.CharField(db_column='Guid', unique=True, max_length=32)  # Field name made lowercase.
    ruleno = models.BigIntegerField(db_column='RuleNo', blank=True, null=True)  # Field name made lowercase.
    deliverydate = models.DateTimeField(db_column='DeliveryDate', blank=True, null=True)  # Field name made lowercase.
    taxableamt = models.DecimalField(db_column='TaxableAmt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    taxadjustment = models.DecimalField(db_column='TaxAdjustment', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    localsubtotalextax = models.DecimalField(db_column='LocalSubTotalExTax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    extradiscountamt = models.DecimalField(db_column='ExtraDiscountAmt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    taxrate = models.DecimalField(db_column='TaxRate', max_digits=18, decimal_places=6, blank=True, null=True)  # Field name made lowercase.
    localtaxadjustment = models.DecimalField(db_column='LocalTaxAdjustment', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    localtaxableamt = models.DecimalField(db_column='LocalTaxableAmt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    taxcurrencytax = models.DecimalField(db_column='TaxCurrencyTax', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    taxcurrencytaxableamt = models.DecimalField(db_column='TaxCurrencyTaxableAmt', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    salesexamtionno = models.CharField(db_column='SalesExamtionNo', max_length=60, blank=True, null=True)  # Field name made lowercase.
    desc2 = models.CharField(db_column='Desc2', max_length=100, blank=True, null=True)  # Field name made lowercase.
    itemcode = models.ForeignKey(Item, models.DO_NOTHING, db_column='ItemCode')  # Field name made lowercase.
    location = models.ForeignKey(Location, models.DO_NOTHING, db_column='Location')  # Field name made lowercase.
    soautokey = models.ForeignKey(So, models.DO_NOTHING, db_column='SOAutoKey')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'sodtl'


class Taxtype(models.Model):
    autokey = models.CharField(db_column='Autokey', primary_key=True, max_length=32)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=120, blank=True, null=True)  # Field name made lowercase.
    taxrate = models.DecimalField(db_column='TaxRate', max_digits=18, decimal_places=6)  # Field name made lowercase.
    inclusive = models.CharField(db_column='Inclusive', max_length=1)  # Field name made lowercase.
    isactive = models.CharField(db_column='IsActive', max_length=1)  # Field name made lowercase.
    lastupdate = models.IntegerField(db_column='LastUpdate')  # Field name made lowercase.
    govtaxcode = models.CharField(db_column='GovTaxCode', max_length=8, blank=True, null=True)  # Field name made lowercase.
    supplypurchase = models.CharField(db_column='SupplyPurchase', max_length=1)  # Field name made lowercase.
    isdefault = models.CharField(db_column='Isdefault', max_length=1)  # Field name made lowercase.
    taxaccno = models.CharField(db_column='TaxAccNo', max_length=12, blank=True, null=True)  # Field name made lowercase.
    iszerorate = models.CharField(db_column='IsZeroRate', max_length=1)  # Field name made lowercase.
    usetrxtaxaccno = models.CharField(db_column='UseTrxTaxAccNo', max_length=1)  # Field name made lowercase.
    accountingbasis = models.IntegerField(db_column='AccountingBasis')  # Field name made lowercase.
    addtocost = models.CharField(db_column='AddToCost', max_length=1)  # Field name made lowercase.
    guid = models.CharField(db_column='Guid', unique=True, max_length=32)  # Field name made lowercase.
    taxsystem = models.CharField(db_column='TaxSystem', max_length=50, blank=True, null=True)  # Field name made lowercase.
    companyautokey = models.ForeignKey(Company, models.DO_NOTHING, db_column='CompanyAutoKey')  # Field name made lowercase.
    taxtype = models.CharField(db_column='TaxType', max_length=14)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'taxtype'


class Terms(models.Model):
    autokey = models.CharField(db_column='Autokey', primary_key=True, max_length=32)  # Field name made lowercase.
    displayterm = models.CharField(db_column='DisplayTerm', unique=True, max_length=50)  # Field name made lowercase.
    terms = models.CharField(db_column='Terms', max_length=30, blank=True, null=True)  # Field name made lowercase.
    lastupdate = models.IntegerField(db_column='LastUpdate')  # Field name made lowercase.
    termtype = models.CharField(db_column='Termtype', max_length=40, blank=True, null=True)  # Field name made lowercase.
    termdays = models.IntegerField(db_column='TermDays', blank=True, null=True)  # Field name made lowercase.
    discountdays = models.IntegerField(db_column='DiscountDays', blank=True, null=True)  # Field name made lowercase.
    discountpercent = models.DecimalField(db_column='DiscountPercent', max_digits=18, decimal_places=6, blank=True, null=True)  # Field name made lowercase.
    companyautokey = models.ForeignKey(Company, models.DO_NOTHING, db_column='CompanyAutokey')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'terms'


class Transaction(models.Model):
    transactionguid = models.CharField(db_column='TransactionGuid', primary_key=True, max_length=32)  # Field name made lowercase.
    docno = models.CharField(db_column='DocNo', max_length=20)  # Field name made lowercase.
    docdate = models.DateTimeField(db_column='DocDate')  # Field name made lowercase.
    debtorname = models.CharField(db_column='DebtorName', max_length=80)  # Field name made lowercase.
    debtorcode = models.CharField(db_column='DebtorCode', max_length=80)  # Field name made lowercase.
    lorryguid = models.ForeignKey(Lorry, models.DO_NOTHING, db_column='LorryGuid')  # Field name made lowercase.
    share = models.SmallIntegerField(db_column='Share', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'transaction'


class Transactiondtl(models.Model):
    transactiondtlguid = models.CharField(db_column='TransactionDtlGuid', primary_key=True, max_length=32)  # Field name made lowercase.
    itemcode = models.CharField(db_column='ItemCode', max_length=80)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=100, blank=True, null=True)  # Field name made lowercase.
    qty = models.DecimalField(db_column='Qty', max_digits=25, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    subtotal = models.DecimalField(db_column='SubTotal', max_digits=19, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    transactionguid = models.ForeignKey(Transaction, models.DO_NOTHING, db_column='TransactionGuid')  # Field name made lowercase.
    itemclass = models.ForeignKey(Itemclass, models.DO_NOTHING, db_column='ItemClass', to_field='ItemClass')  # Field name made lowercase.
    uom = models.CharField(db_column='Uom', max_length=30, blank=True, null=True)  # Field name made lowercase.
    commtype = models.CharField(db_column='CommType', max_length=30, blank=True, null=True)  # Field name made lowercase.
    udfcalmethod = models.CharField(db_column='UdfCalMethod', max_length=8, blank=True, null=True)  # Field name made lowercase.
    udfcalrate = models.DecimalField(db_column='UdfCalRate', max_digits=2, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    isqtyupdated = models.IntegerField(db_column='IsQtyUpdated')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'transactiondtl'


class XTmp(models.Model):
    itemcode = models.CharField(primary_key=True, max_length=20)  # The composite primary key (itemcode, uom) found, that is not supported. The first column is selected.
    uom = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'x_tmp'
        unique_together = (('itemcode', 'uom'),)
