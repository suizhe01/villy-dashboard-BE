# excelreader/urls.py
from django.urls import path
from .views import \
post_dutchlady_item_itemuom, post_dutchlady_pi_pidtl_purchase, post_dutchlady_iv_ivdtl_invoice,post_dutchlady_cn_cndtl,post_dutchlady_gr_grdtl_purchase,\
post_lipton_item_itemuom,post_lipton_pi_pidtl_purchase,post_lipton_iv_ivdtl_invoice,post_lipton_cn_cndtl,\
post_mamee_item_itemuom, post_mamee_pi_pidtl_purchase,post_mamee_iv_ivdtl_invoice,post_mamee_cn_cndtl,post_mamee_gr_grdtl_purchase,\
post_dksh_item_itemuom, post_dksh_gr_grdtl_purchase,post_dksh_iv_ivdtl_invoice,post_dksh_cn_cndtl,\
post_cola_item_itemuom,post_cola_iv_ivdtl_invoice, post_cola_cn_cndtl,\
post_redbull_item_itemuom,post_redbull_iv_ivdtl_invoice,post_redbull_cn_cndtl,\
post_mp_item_itemuom, post_mp_iv_ivdtl_invoice, post_mp_cn_cndtl,\
post_kara_item_itemuom, post_kara_iv_ivdtl_invoice, post_kara_cn_cndtl,\
        post_dob_yltc_item_itemuom,post_dob_yltc_iv_ivdtl_invoice,\
        post_dob_sunquick_item_itemuom, post_dob_sunquick_iv_ivdtl_invoice,\
        post_dob_mamee_item_itemuom,post_dob_mamee_iv_ivdtl_invoice,\
        post_dob_tohtonku_item_itemuom,post_dob_tohtonku_iv_ivdtl_invoice,\
                                            post_commission,\
                                            commission_add_lorry_crew_transaction,\
                                            calculate_commission,display_commission_by_crew_id, display_commission_by_crew_guid,display_commission_by_lorry_guid,\
                                            custom_get_crew,\
                                            custom_create_crew,\
                                            custom_delete_crew, custom_delete_transaction,\
                                            export_crew,\
                                            search_transaction,\
                                            print_commission_list_report,\
                                            custom_update_lorry_plate


urlpatterns = [
    # dutch lady
    path('post_dutchlady_item_itemuom/', post_dutchlady_item_itemuom, name='post_dutchlady_item_itemuom'),
    path('post_dutchlady_gr_grdtl_purchase/', post_dutchlady_gr_grdtl_purchase, name='post_dutchlady_gr_grdtl_purchase'),
    path('post_dutchlady_pi_pidtl_purchase/', post_dutchlady_pi_pidtl_purchase, name='post_dutchlady_pi_pidtl_purchase'),
    path('post_dutchlady_iv_ivdtl_invoice/', post_dutchlady_iv_ivdtl_invoice, name='post_dutchlady_iv_ivdtl_invoice'),
    path('post_dutchlady_cn_cndtl/', post_dutchlady_cn_cndtl, name='post_dutchlady_cn_cndtl'),

    # lipton
    path('post_lipton_item_itemuom/', post_lipton_item_itemuom, name='post_lipton_item_itemuom'),
    # path('post_lipton_gr_grdtl/', post_lipton_gr_grdtl, name='post_lipton_gr_grdtl'),
    path('post_lipton_pi_pidtl_purchase/',post_lipton_pi_pidtl_purchase, name='post_lipton_pi_pidtl_purchase'),
    path('post_lipton_iv_ivdtl_invoice/',post_lipton_iv_ivdtl_invoice, name='post_lipton_iv_ivdtl_invoice'),
    path('post_lipton_cn_cndtl/',post_lipton_cn_cndtl, name='post_lipton_cn_cndtl'),
    
    # mamee
    path('post_mamee_item_itemuom/' , post_mamee_item_itemuom, name='post_mamee_item_itemuom'),
    # path('post_mamee_item_itemuom_invoice/',post_mamee_item_itemuom_invoice, name='post_mamee_item_itemuom_invoice'),
    path('post_mamee_gr_grdtl_purchase/', post_mamee_gr_grdtl_purchase, name='post_mamee_gr_grdtl_purchase'),
    path('post_mamee_pi_pidtl_purchase/', post_mamee_pi_pidtl_purchase, name='post_mamee_pi_pidtl_purchase'),
    path('post_mamee_iv_ivdtl_invoice/',post_mamee_iv_ivdtl_invoice,name='post_mamee_iv_ivdtl_invoice'),
    path('post_mamee_cn_cndtl/', post_mamee_cn_cndtl, name='post_mamee_cn_cndtl'),

    # DKSH
    path('post_dksh_item_itemuom/', post_dksh_item_itemuom, name='post_dksh_item_itemuom'),
    path('post_dksh_gr_grdtl_purchase/', post_dksh_gr_grdtl_purchase, name='post_dksh_gr_grdtl_purchase'),
    path('post_dksh_iv_ivdtl_invoice/', post_dksh_iv_ivdtl_invoice, name='post_dksh_iv_ivdtl_invoice'),
    path('post_dksh_cn_cndtl/', post_dksh_cn_cndtl, name='post_dksh_cn_cndtl'),
    
    
    # cola
    path('post_cola_item_itemuom/', post_cola_item_itemuom, name='post_cola_item_itemuom'),
    path('post_cola_iv_ivdtl_invoice/', post_cola_iv_ivdtl_invoice, name='post_cola_iv_ivdtl_invoice'),
    path('post_cola_cn_cndtl/', post_cola_cn_cndtl, name='post_cola_cn_cndtl'),
    
    # redbull
    path('post_redbull_item_itemuom/', post_redbull_item_itemuom, name='post_redbull_item_itemuom'),
    # path('post_redbull_item_itemuom_cn/', post_redbull_item_itemuom_cn, name='post_redbull_item_itemuom_cn'),
    path('post_redbull_iv_ivdtl_invoice/', post_redbull_iv_ivdtl_invoice, name='post_redbull_iv_ivdtl_invoice'),
    path('post_redbull_cn_cndtl/', post_redbull_cn_cndtl, name='post_redbull_cn_cndtl'),

    # mp
    path('post_mp_item_itemuom/', post_mp_item_itemuom, name='post_mp_item_itemuom'),
    path('post_mp_iv_ivdtl_invoice/', post_mp_iv_ivdtl_invoice, name='post_mp_iv_ivdtl_invoice'),
    path('post_mp_cn_cndtl/', post_mp_cn_cndtl, name='post_mp_cn_cndtl'),
    
    # kara
    path('post_kara_item_itemuom/', post_kara_item_itemuom, name='post_kara_item_itemuom'),
    path('post_kara_iv_ivdtl_invoice/', post_kara_iv_ivdtl_invoice, name='post_kara_iv_ivdtl_invoice'),
    path('post_kara_cn_cndtl/', post_kara_cn_cndtl, name='post_kara_cn_cndtl'),

    # dob yltc
    path('post_dob_yltc_item_itemuom/', post_dob_yltc_item_itemuom, name='post_dob_yltc_item_itemuom'),
    path('post_dob_yltc_iv_ivdtl_invoice/', post_dob_yltc_iv_ivdtl_invoice, name='post_dob_yltc_iv_ivdtl_invoice'),
    
    # dob sunquick
    path('post_dob_sunquick_item_itemuom/', post_dob_sunquick_item_itemuom, name='post_dob_sunquick_item_itemuom'),
    path('post_dob_sunquick_iv_ivdtl_invoice/', post_dob_sunquick_iv_ivdtl_invoice, name='post_dob_sunquick_iv_ivdtl_invoice'),
    
    # dob mamee
    path('post_dob_mamee_item_itemuom/', post_dob_mamee_item_itemuom, name='post_dob_mamee_item_itemuom'),
    path('post_dob_mamee_iv_ivdtl_invoice/', post_dob_mamee_iv_ivdtl_invoice, name='post_dob_mamee_iv_ivdtl_invoice'),

    # dob tohtonku
    path('post_dob_tohtonku_item_itemuom/', post_dob_tohtonku_item_itemuom, name='post_dob_tohtonku_item_itemuom'),
    path('post_dob_tohtonku_iv_ivdtl_invoice/', post_dob_tohtonku_iv_ivdtl_invoice, name='post_dob_tohtonku_iv_ivdtl_invoice'),

    
    # commission
    path('post_commission/', post_commission, name='post_commission'),
    path('commission_add_lorry_crew_transaction/', commission_add_lorry_crew_transaction, name='commission_add_lorry_crew_transaction'),

    path('calculate_commission/', calculate_commission, name='calculate_commission'),
    path('display_commission_by_crew_id/', display_commission_by_crew_id, name='display_commission_by_crew_id'),
    path('display_commission_by_crew_guid/', display_commission_by_crew_guid, name='display_commission_by_crew_guid'),
    path('display_commission_by_lorry_guid/', display_commission_by_lorry_guid, name='display_commission_by_lorry_guid'),
    path('export_crew/', export_crew, name='export_crew'),
    
    # custom get
    path('custom_get_crew/', custom_get_crew, name='custom_get_crew'),
    

    # custom create
    path('custom_create_crew/', custom_create_crew, name='custom_create_crew'),

    # custom delete
    path('custom_delete_crew/', custom_delete_crew, name='custom_delete_crew'),
    path('custom_delete_transaction/', custom_delete_transaction, name='custom_delete_transaction'),
    
    # custom update
    path('custom_update_lorry_plate/', custom_update_lorry_plate, name='custom_update_lorry_plate'),

    # search function
    path('search_transaction/', search_transaction, name='search_transaction'),

    # print list report
    path('print_commission_list_report/', print_commission_list_report, name='print_commission_list_report'),
    
]
