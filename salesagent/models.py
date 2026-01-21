from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save
from django.dispatch import receiver
from _lib import panda

# Create your models here.
class SalesAgent(models.Model):
    autokey = models.CharField(primary_key=True, db_column='Autokey',max_length=32, editable=False, unique=True)
    salesagent = models.CharField(max_length=40,db_column='SalesAgent', null= False, unique=True)
    description = models.CharField(max_length=40,db_column='Description', null= True)
    desc2 = models.CharField(max_length=80,db_column='Desc2', null= True)
    isactive = models.CharField(db_column ='IsActive',max_length=1, null=False)
    lastupdate = models.IntegerField(db_column='LastUpdate', null=False)
    signature = models.BinaryField(db_column='Signature', null=True)
    guid = models.CharField(max_length=32,db_column='Guid', null= False, unique=True)
    emailaddress = models.CharField(db_column ='EmailAddress',max_length=200, null=True)
    approveremailaddress = models.CharField(db_column ='ApproverEmailAddress',max_length=200, null=True)

    class Meta:
        # app_label = 'MlItemmaster'
        managed = True
        db_table = "salesagent"
        ordering = ("salesagent",)

    def __str__(self):
        return self.autokey
        
    def get_absolute_url(self):
        return f"/{self.autokey}/"

@receiver(pre_save, sender=SalesAgent)
def pre_save_salesagent(sender, instance, **kwargs):
    print("pre_save_sales_agent")
    # instance.updated_at = panda.panda_today()
    if not instance.autokey :
        instance.autokey = panda.panda_uuid()

    if not instance.guid:
        instance.guid = panda.panda_uuid()