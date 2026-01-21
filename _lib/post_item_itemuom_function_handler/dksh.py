from company.models import Company
from item.models import Item
from itemuom.models import ItemUOM

def create_dksh_item_itemuom(itemcode, description, uom, price, rate, unit_uom, unit_price, unit_rate, is_exist):
    tempcompanyautokey = Company.objects.filter(name='Villy').first()
    filter_itemcode = Item.objects.filter(itemcode=itemcode)
    filter_carton_uom = ItemUOM.objects.filter(itemcode=itemcode, uom=uom)
    filter_unit_uom = ItemUOM.objects.filter(itemcode=itemcode, uom=unit_uom)
    mainsupplier='DKSH'

    if is_exist == 0:
        if not filter_itemcode:
            save_new_item = Item(description=description,itemcode=itemcode,companyautokey=tempcompanyautokey,mainsupplier=mainsupplier, dockkey=1, dutyrate=1, costingmethod=0, lastmodified='2024-01-31T04:07:07.678Z', lastupdate=0)
            save_new_item.save()
            itemcode_intance = Item.objects.get(itemcode=itemcode)
            if rate!= 1:
                if not filter_carton_uom:
                    save_carton_uom = ItemUOM(companyautokey=tempcompanyautokey,itemcode=itemcode_intance,uom=uom,rate=rate,price=price,lastupdate=1)
                    save_carton_uom.save()
                if not filter_unit_uom:
                    save_unit_uom = ItemUOM(companyautokey=tempcompanyautokey,itemcode=itemcode_intance,uom=unit_uom,rate=unit_rate,price=unit_price,lastupdate=1)
                    save_unit_uom.save()
            else:
                if not filter_carton_uom:
                    save_unit_uom = ItemUOM(companyautokey=tempcompanyautokey,itemcode=itemcode_intance,uom=uom,rate=rate,price=price,lastupdate=1)
                    save_unit_uom.save()
        else:
            itemcode_intance = Item.objects.get(itemcode=itemcode)
            if not filter_carton_uom:
                save_carton_uom = ItemUOM(companyautokey=tempcompanyautokey,itemcode=itemcode_intance,uom=uom,rate=rate,price=price,lastupdate=1)
                save_carton_uom.save()
            if not filter_unit_uom:
                save_unit_uom = ItemUOM(companyautokey=tempcompanyautokey,itemcode=itemcode_intance,uom=unit_uom,rate=unit_rate,price=unit_price,lastupdate=1)
                save_unit_uom.save()



