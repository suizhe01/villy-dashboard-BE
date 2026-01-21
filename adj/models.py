from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save
from django.dispatch import receiver
from _lib import panda
from branch.models import Branch

# Create your models here.
class ADJ(models.Model):
    autokey = models.CharField(primary_key=True, db_column='Autokey',max_length=32, editable=False, unique=True)
    branchautokey = models.ForeignKey(Branch,
                                       models.DO_NOTHING,
                                       db_column='BranchAutoKey',
                                       related_name='ADJBranchAutokey'
                                       )
    docno = models.CharField(max_length=20,db_column='DocNo', null= False)
    docdate = models.DateTimeField(db_column='DocDate', null=False)
    description = models.CharField(max_length=80,db_column='Description', null= True)
    total = models.DecimalField(db_column='Total', max_digits=19, decimal_places=2, null=True)
    note = models.CharField(max_length=255,db_column='Note', null= True)
    remark1 = models.CharField(max_length=40,db_column='Remark1', null= True)
    remark2 = models.CharField(max_length=40,db_column='Remark2', null= True)
    remark3 = models.CharField(max_length=40,db_column='Remark3', null= True)
    remark4 = models.CharField(max_length=40,db_column='Remark4', null= True)
    printcount = models.SmallIntegerField(db_column='PrintCount', null=False)
    cancelled = models.CharField(max_length=1,db_column='Cancelled', null= False)
    lastmodified = models.DateTimeField(db_column='LastModified', null=False)
    lastmodifieduserid = models.CharField(max_length=10,db_column='LastModifiedUserID', null= False)
    createdtimestamp = models.DateTimeField(db_column='CreatedTimeStamp', null=False)
    createduserid = models.CharField(max_length=10,db_column='CreatedUserID', null= False)
    externallink = models.CharField(max_length=255,db_column='ExternalLink', null= True)
    refdocno = models.CharField(max_length=20,db_column='RefDocNo', null= True)
    lastupdate = models.IntegerField(db_column='LastUpdate', null=False)
    cansync = models.CharField(max_length=1,db_column='CanSync', null= False)
    guid = models.CharField(max_length=32,db_column='Guid', null= False, unique=True)

    class Meta:
        # app_label = 'MlItemmaster'
        managed = True
        db_table = "adj"
        ordering = ("docno",)

    def __str__(self):
        return self.autokey
    
    def get_absolute_url(self):
        return f"/{self.autokey}/"
    
@receiver(pre_save, sender=ADJ)
def pre_save_company(sender, instance, **kwargs):
    print("pre_save")
    # instance.updated_at = panda.panda_today()
    if instance.autokey == "":
        instance.autokey = panda.panda_uuid()