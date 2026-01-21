from itemgroup.models import ItemGroup
from company.models import Company
from itemtype.models import ItemType
from taxtype.models import TaxType
from itembrand.models import ItemBrand
from itemclass.models import ItemClass
from itemcategory.models import ItemCategory
from creditor.models import Creditor
from item.models import Item
from itemuom.models import ItemUOM

def create_cola_item_itemuom(itemcode, description, uom, price, rate, single_uom, single_price, single_rate):
    tempcompanyautokey = Company.objects.first()
    tempitemgroup = ItemGroup.objects.first()
    tempitemtype = ItemType.objects.first()
    temptaxtype = TaxType.objects.first()
    tempitembrand = ItemBrand.objects.first()
    tempitemclass = ItemClass.objects.first()
    tempitemcategory = ItemCategory.objects.first()
    tempcreditor = Creditor.objects.filter(companyname='Cola').first()

    filter_itemcode = Item.objects.filter(itemcode=itemcode)
            
    if not filter_itemcode:
        save_new_item = Item(description=description,itemcode=itemcode,companyautokey=tempcompanyautokey,itemgroup=tempitemgroup,taxtype=temptaxtype,itemtype=tempitemtype,itembrand=tempitembrand,itemclass=tempitemclass,itemcategory=tempitemcategory,mainsupplier=tempcreditor, dockkey=1, dutyrate=1, costingmethod=0, lastmodified='2024-01-31T04:07:07.678Z', lastupdate=1)
        save_new_item.save()
        print('im new item')
        if rate != 1:
            itemcode_intance = Item.objects.get(itemcode=itemcode)
            save_single_uom = ItemUOM(companyautokey=tempcompanyautokey,itemcode=itemcode_intance,uom=single_uom,rate=single_rate,price=single_price,lastupdate=1)
            save_multiple_uom =  ItemUOM(companyautokey=tempcompanyautokey,itemcode=itemcode_intance,uom=uom,rate=rate,price=price,lastupdate=1)
            save_single_uom.save()
            save_multiple_uom.save()
            print("i'm new uom !!!!")
        else:
            itemcode_intance = Item.objects.get(itemcode=itemcode)
            save_single_uom = ItemUOM(companyautokey=tempcompanyautokey,itemcode=itemcode_intance,uom=uom,rate=rate,price=price,lastupdate=1)
            save_single_uom.save()
    else:
        itemcode_intance = Item.objects.get(itemcode=itemcode)
        filter_single_item_uom = ItemUOM.objects.filter(itemcode=itemcode, uom=uom)
        if not filter_single_item_uom:
            save_single_uom = ItemUOM(companyautokey=tempcompanyautokey,itemcode=itemcode_intance,uom=uom,rate=rate,price=price,lastupdate=1)
            save_single_uom.save()