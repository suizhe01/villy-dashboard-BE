from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save
from django.dispatch import receiver
from _lib import panda

# Create your models here.
class Company(models.Model):
    autokey = models.CharField(primary_key=True,db_column='Autokey', max_length=32, editable=False, unique=True)
    code = models.CharField(max_length=32,db_column='Code', unique= True)
    name = models.CharField(max_length=255,db_column='Name', null=False)
    address = models.CharField(max_length = 255,db_column='Address', null =False, blank=False)
    registrationnum = models.CharField(max_length=32,db_column='RegistrationNum', unique=True)

    class Meta:
        # app_label = 'MlItemmaster'
        managed = True
        db_table = "company"
        ordering = ("code",)

    def __str__(self):
        return self.autokey
    
    def get_absolute_url(self):
        return f"/{self.autokey}/"
    
@receiver(pre_save, sender=Company)
def pre_save_company(sender, instance, **kwargs):
    print("pre_save")
    # instance.updated_at = panda.panda_today()
    if instance.autokey == "":
        instance.autokey = panda.panda_uuid()