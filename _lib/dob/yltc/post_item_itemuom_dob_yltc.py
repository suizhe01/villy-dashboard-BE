from django.http import JsonResponse
from rest_framework import status
import pandas as pd
from itemuom.models import ItemUOM
from company.models import Company
from item.models import Item
from datetime import datetime
from _lib.panda import current_date_time

def create_dob_yltc_item_itemuom_invoice(itemcode, description, uom, price, rate, unit_uom, unit_price, unit_rate):
    tempcompanyautokey = Company.objects.filter(name='Villy').first()
    mainsupplier='DOB_YLTC'
    filter_itemcode = Item.objects.filter(itemcode=itemcode)
    filter_uom = ItemUOM.objects.filter(itemcode=itemcode, uom=uom)
    datetimenow = current_date_time()
    dockey = 1
    dutyrate = 1
    costingmethod = 0
    lastupdate = 0

    if not filter_itemcode:
        save_new_item = Item(description=description,itemcode=itemcode,companyautokey=tempcompanyautokey,mainsupplier=mainsupplier, dockkey=dockey, dutyrate=dutyrate, costingmethod=costingmethod, lastmodified=datetimenow, lastupdate=lastupdate)
        save_new_item.save()
        itemcode_instance = Item.objects.get(itemcode=itemcode)

        filter_unit_uom = ItemUOM.objects.filter(itemcode=itemcode, uom=unit_uom)
        if not filter_uom:
            save_uom = ItemUOM(companyautokey=tempcompanyautokey,itemcode=itemcode_instance,uom=uom,rate=rate,price=price,lastupdate=lastupdate)
            save_uom.save()

        if not filter_unit_uom:
            save_unit_uom = ItemUOM(companyautokey=tempcompanyautokey,itemcode=itemcode_instance,uom=unit_uom,rate=unit_rate,price=unit_price,lastupdate=0)
            save_unit_uom.save()
    else:
        itemcode_instance = Item.objects.get(itemcode=itemcode)

        if not filter_uom:
            save_uom = ItemUOM(companyautokey=tempcompanyautokey,itemcode=itemcode_instance,uom=uom,rate=rate,price=price,lastupdate=lastupdate)
            save_uom.save()

        filter_unit_uom = ItemUOM.objects.filter(itemcode=itemcode, uom=unit_uom)
        if not filter_unit_uom:
            save_unit_uom = ItemUOM(companyautokey=tempcompanyautokey,itemcode=itemcode_instance,uom=unit_uom,rate=unit_rate,price=unit_price,lastupdate=0)
            save_unit_uom.save()