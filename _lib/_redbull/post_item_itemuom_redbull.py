from django.http import JsonResponse
from rest_framework import status
import pandas as pd
from itemuom.models import ItemUOM
from company.models import Company
from item.models import Item
from datetime import datetime
from _lib.panda import current_date_time

def create_redbull_item_itemuom_selling(item_code, description, uom, price, rate, unit_uom, unit_price, unit_rate):
    try:
        tempcompanyautokey = Company.objects.filter(name='Villy').first()
        if not tempcompanyautokey:
            raise ValueError("Company 'Villy' not found")

        filter_itemcode = Item.objects.filter(itemcode=item_code).first()
        filter_uom = ItemUOM.objects.filter(itemcode=item_code, uom=uom).first()
        mainsupplier = 'Redbull'
        date_time_now = datetime.now()

        if not filter_itemcode:
            save_new_item = Item(itembrand='redbull',itemcode=item_code,description=description,companyautokey=tempcompanyautokey,mainsupplier=mainsupplier,dockkey=1,dutyrate=1,costingmethod=0,lastmodified=date_time_now,lastupdate=0)
            save_new_item.save()
            itemcode_instance = Item.objects.get(itemcode=item_code)
            if not filter_uom:
                save_uom = ItemUOM(companyautokey=tempcompanyautokey,itemcode=itemcode_instance,uom=uom,rate=rate,price=price,lastupdate=0)
                save_uom.save()

            filter_unit_uom = ItemUOM.objects.filter(itemcode=item_code, uom=unit_uom).first()
            
            if not filter_unit_uom:
                save_unit_uom = ItemUOM(companyautokey=tempcompanyautokey,itemcode=itemcode_instance,uom=unit_uom,rate=unit_rate,price=unit_price,lastupdate=0)
                save_unit_uom.save()
        else:
            itemcode_instance = Item.objects.get(itemcode=item_code)
            # itemcode_instance.itembrand = 'lipton'
            # itemcode_instance.save()
            if not filter_uom:
                save_uom = ItemUOM(companyautokey=tempcompanyautokey,itemcode=itemcode_instance,uom=uom,rate=rate,price=price,lastupdate=0)
                save_uom.save()
            else:
                uom_object = ItemUOM.objects.get(itemcode=item_code, uom=uom)
                uom_object.rate = rate
                uom_object.price = price
                uom_object.save()

            filter_unit_uom = ItemUOM.objects.filter(itemcode=item_code, uom=unit_uom).first()
            
            if not filter_unit_uom:
                save_unit_uom = ItemUOM(companyautokey=tempcompanyautokey,itemcode=itemcode_instance,uom=unit_uom,rate=unit_rate,price=unit_price,lastupdate=0)
                save_unit_uom.save()
            else:
                unit_uom_object = ItemUOM.objects.get(itemcode=item_code, uom=unit_uom)
                unit_uom_object.rate = unit_rate
                unit_uom_object.price = unit_price
                unit_uom_object.save()
        return True
    except Exception as e:
        print(f"Error in handle_item_itemuom: {e}")
        return False

def create_redbull_item_itemuom_invoice(itemcode, description, uom, price, rate, unit_uom, unit_price, unit_rate):
    tempcompanyautokey = Company.objects.filter(name='Villy').first()
    mainsupplier='Redbull'
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
            
def create_redbull_item_itemuom_cn(itemcode, description, ctn_uom,ctn_rate,ctn_price,otr_uom,otr_rate,otr_price,unit_uom,unit_rate,unit_price):
    tempcompanyautokey = Company.objects.filter(name='Villy').first()
    mainsupplier='Redbull'
    filter_itemcode = Item.objects.filter(itemcode=itemcode)
    filter_ctn_uom = ItemUOM.objects.filter(itemcode=itemcode, uom=ctn_uom)
    filter_otr_uom = ItemUOM.objects.filter(itemcode=itemcode, uom=otr_uom)
    filter_unit_uom = ItemUOM.objects.filter(itemcode=itemcode, uom=unit_uom)
    datetimenow = current_date_time()
    dockey = 1
    dutyrate = 1
    costingmethod = 0
    lastupdate = 0

    if not filter_itemcode:
        save_new_item = Item(description=description,itemcode=itemcode,companyautokey=tempcompanyautokey,mainsupplier=mainsupplier, dockkey=dockey, dutyrate=dutyrate, costingmethod=costingmethod, lastmodified=datetimenow, lastupdate=lastupdate)
        save_new_item.save()
        itemcode_instance = Item.objects.get(itemcode=itemcode)
        if not filter_ctn_uom:
            save_ctn_uom = ItemUOM(companyautokey=tempcompanyautokey,itemcode=itemcode_instance,uom=ctn_uom,rate=ctn_rate,price=ctn_price,lastupdate=lastupdate)
            save_ctn_uom.save()
        if not filter_otr_uom:
            save_otr_uom = ItemUOM(companyautokey=tempcompanyautokey,itemcode=itemcode_instance,uom=otr_uom,rate=otr_rate,price=otr_price,lastupdate=lastupdate)
            save_otr_uom.save()
        if not filter_unit_uom:
            save_unit_uom = ItemUOM(companyautokey=tempcompanyautokey,itemcode=itemcode_instance,uom=unit_uom,rate=unit_rate,price=unit_price,lastupdate=lastupdate)
            save_unit_uom.save()
    else:
        itemcode_instance = Item.objects.get(itemcode=itemcode)
        if not filter_ctn_uom:
            save_ctn_uom = ItemUOM(companyautokey=tempcompanyautokey,itemcode=itemcode_instance,uom=ctn_uom,rate=ctn_rate,price=ctn_price,lastupdate=lastupdate)
            save_ctn_uom.save()
        if not filter_otr_uom:
            save_otr_uom = ItemUOM(companyautokey=tempcompanyautokey,itemcode=itemcode_instance,uom=otr_uom,rate=otr_rate,price=otr_price,lastupdate=lastupdate)
            save_otr_uom.save()
        if not filter_unit_uom:
            save_unit_uom = ItemUOM(companyautokey=tempcompanyautokey,itemcode=itemcode_instance,uom=unit_uom,rate=unit_rate,price=unit_price,lastupdate=lastupdate)
            save_unit_uom.save()