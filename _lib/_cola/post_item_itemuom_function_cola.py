from django.http import JsonResponse
from rest_framework import status
import pandas as pd
from itemuom.models import ItemUOM
from company.models import Company
from item.models import Item
from datetime import datetime

def create_cola_item_itemuom_selling(item_code, description, uom, price, rate, unit_uom, unit_price, unit_rate):
    try:
        temcompanyautokey = Company.objects.filter(name='Villy').first()
        if not temcompanyautokey:
            raise ValueError("Company 'Villy' not found")

        filter_itemcode = Item.objects.filter(itemcode=item_code).first()
        filter_uom = ItemUOM.objects.filter(itemcode=item_code, uom=uom).first()
        filter_unit_uom = ItemUOM.objects.filter(itemcode=item_code, uom=unit_uom).first()
        mainsupplier = 'Cola'
        date_time_now = datetime.now()

        if not filter_itemcode:
            save_new_item = Item(itembrand='cola',itemcode=item_code,description=description,companyautokey=temcompanyautokey,mainsupplier=mainsupplier,dockkey=1,dutyrate=1,costingmethod=0,lastmodified=date_time_now,lastupdate=0)
            save_new_item.save()
            itemcode_instance = Item.objects.get(itemcode=item_code)
            if not filter_uom:
                save_uom = ItemUOM(companyautokey=temcompanyautokey,itemcode=itemcode_instance,uom=uom,rate=rate,price=price,lastupdate=0)
                save_uom.save()
            
            if not filter_unit_uom:
                save_unit_uom = ItemUOM(companyautokey=temcompanyautokey,itemcode=itemcode_instance,uom=unit_uom,rate=unit_rate,price=unit_price,lastupdate=0)
                save_unit_uom.save()
        else:
            itemcode_instance = Item.objects.get(itemcode=item_code)
            # itemcode_instance.itembrand = 'lipton'
            # itemcode_instance.save()
            if not filter_uom:
                save_uom = ItemUOM(companyautokey=temcompanyautokey,itemcode=itemcode_instance,uom=uom,rate=rate,price=price,lastupdate=0)
                save_uom.save()
            else:
                uom_object = ItemUOM.objects.get(itemcode=item_code, uom=uom)
                uom_object.rate = rate
                uom_object.price = price
                uom_object.save()
            
            if not filter_unit_uom:
                save_unit_uom = ItemUOM(companyautokey=temcompanyautokey,itemcode=itemcode_instance,uom=unit_uom,rate=unit_rate,price=unit_price,lastupdate=0)
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

def create_cola_item_itemuom_invoice(item_code, description,uom,rate,price, unit_uom, unit_price, unit_rate):
    temcompanyautokey = Company.objects.filter(name='Villy').first()
    filter_itemcode = Item.objects.filter(itemcode=item_code).first()
    filter_uom = ItemUOM.objects.filter(itemcode=item_code, uom=uom).first()
    filter_unit_uom = ItemUOM.objects.filter(itemcode=item_code, uom=unit_uom).first()
    mainsupplier = 'COLA'
    date_time_now = datetime.now()

    if not filter_itemcode:
        save_new_item = Item(itembrand='COLA',itemcode=item_code,description=description,companyautokey=temcompanyautokey,mainsupplier=mainsupplier,dockkey=1,dutyrate=1,costingmethod=0,lastmodified=date_time_now,lastupdate=0)
        save_new_item.save()
        itemcode_instance = Item.objects.get(itemcode=item_code)
        if not filter_uom:
            save_uom = ItemUOM(companyautokey=temcompanyautokey,itemcode=itemcode_instance,uom=uom,rate=rate,price=price,lastupdate=0)
            save_uom.save()
        if not filter_unit_uom:
                save_unit_uom = ItemUOM(companyautokey=temcompanyautokey,itemcode=itemcode_instance,uom=unit_uom,rate=unit_rate,price=unit_price,lastupdate=0)
                save_unit_uom.save()
    else:
        itemcode_instance = Item.objects.get(itemcode=item_code)
        if not filter_uom:
            save_uom = ItemUOM(companyautokey=temcompanyautokey,itemcode=itemcode_instance,uom=uom,rate=rate,price=price,lastupdate=0)
            save_uom.save()
        else:
            uom_object = ItemUOM.objects.get(itemcode=item_code, uom=uom)
            uom_object.rate = rate
            uom_object.price = price
            uom_object.save()

        if not filter_unit_uom:
                save_unit_uom = ItemUOM(companyautokey=temcompanyautokey,itemcode=itemcode_instance,uom=unit_uom,rate=unit_rate,price=unit_price,lastupdate=0)
                save_unit_uom.save()
        else:
            unit_uom_object = ItemUOM.objects.get(itemcode=item_code, uom=unit_uom)
            unit_uom_object.rate = unit_rate
            unit_uom_object.price = unit_price
            unit_uom_object.save()

def create_cola_item_itemuom_cn(item_code, description,uom,rate,price, unit_uom, unit_price, unit_rate):
    temcompanyautokey = Company.objects.filter(name='Villy').first()
    filter_itemcode = Item.objects.filter(itemcode=item_code).first()
    filter_uom = ItemUOM.objects.filter(itemcode=item_code, uom=uom).first()
    filter_unit_uom = ItemUOM.objects.filter(itemcode=item_code, uom=unit_uom).first()
    mainsupplier = 'COLA'
    date_time_now = datetime.now()

    if not filter_itemcode:
        save_new_item = Item(itembrand='COLA',itemcode=item_code,description=description,companyautokey=temcompanyautokey,mainsupplier=mainsupplier,dockkey=1,dutyrate=1,costingmethod=0,lastmodified=date_time_now,lastupdate=0)
        save_new_item.save()
        itemcode_instance = Item.objects.get(itemcode=item_code)
        if not filter_uom:
            save_uom = ItemUOM(companyautokey=temcompanyautokey,itemcode=itemcode_instance,uom=uom,rate=rate,price=price,lastupdate=0)
            save_uom.save()
        if not filter_unit_uom:
                save_unit_uom = ItemUOM(companyautokey=temcompanyautokey,itemcode=itemcode_instance,uom=unit_uom,rate=unit_rate,price=unit_price,lastupdate=0)
                save_unit_uom.save()
    else:
        itemcode_instance = Item.objects.get(itemcode=item_code)
        if not filter_uom:
            save_uom = ItemUOM(companyautokey=temcompanyautokey,itemcode=itemcode_instance,uom=uom,rate=rate,price=price,lastupdate=0)
            save_uom.save()
        else:
            uom_object = ItemUOM.objects.get(itemcode=item_code, uom=uom)
            uom_object.rate = rate
            uom_object.price = price
            uom_object.save()

        if not filter_unit_uom:
                save_unit_uom = ItemUOM(companyautokey=temcompanyautokey,itemcode=itemcode_instance,uom=unit_uom,rate=unit_rate,price=unit_price,lastupdate=0)
                save_unit_uom.save()
        else:
            unit_uom_object = ItemUOM.objects.get(itemcode=item_code, uom=unit_uom)
            unit_uom_object.rate = unit_rate
            unit_uom_object.price = unit_price
            unit_uom_object.save()