"""
URL configuration for autocount_dashboard project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings      #< add
from django.conf.urls.static import static  #< add
from django.contrib import admin
from django.urls import path,include   #< add
from drf_spectacular.views import SpectacularAPIView,SpectacularSwaggerView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('company/',include('company.urls')),
    path('branch/',include('branch.urls')),
    path('terms/',include('terms.urls')),
    path('location/',include('location.urls')),
    path('debtor/',include('debtor.urls')),
    path('debtortype/',include('debtortype.urls')),
    path('creditor/',include('creditor.urls')),
    path('creditortype/',include('creditortype.urls')),
    path('itemgroup/',include('itemgroup.urls')),
    path('itemtype/',include('itemtype.urls')),
    path('taxtype/',include('taxtype.urls')),
    path('itembrand/',include('itembrand.urls')),
    path('itemclass/',include('itemclass.urls')),
    path('itemcategory/',include('itemcategory.urls')),
    path('item/',include('item.urls')),
    path('itembatch/',include('itembatch.urls')),
    path('itembom/',include('itembom.urls')),
    path('itemuom/',include('itemuom.urls')),
    path('itemprice/',include('itemprice.urls')),
    path('po/',include('po.urls')),
    path('podtl/',include('podtl.urls')),
    path('pi/',include('pi.urls')),
    path('pidtl/',include('pidtl.urls')),
    path('pr/',include('pr.urls')),
    path('prdtl/',include('prdtl.urls')),
    path('so/',include('so.urls')),
    path('sodtl/',include('sodtl.urls')),
    path('cn/',include('cn.urls')),
    path('cndtl/',include('cndtl.urls')),
    path('dn/',include('dn.urls')),
    path('dndtl/',include('dndtl.urls')),
    path('adj/',include('adj.urls')),
    path('adjdtl/',include('adjdtl.urls')),
    path('iv/',include('iv.urls')),
    path('ivdtl/',include('ivdtl.urls')),
    path('filereader/',include('filereader.urls')),
    path('posthandler/',include('posthandler.urls')),
    path('gr/',include('gr.urls')),
    path('grdtl/',include('grdtl.urls')),
    path('salesagent/',include('salesagent.urls')),
    path('commissionitemclass/',include('commissionitemclass.urls')),
    path('crewrate/',include('crewrate.urls')),
    path('crewratedtl/',include('crewratedtl.urls')),
    path('lorry/',include('lorry.urls')),
    path('lorryplate/',include('lorryplate.urls')),
    path('crew/',include('crew.urls')),
    path('crewdtl/',include('crewdtl.urls')),
    path('transaction/',include('transaction.urls')),
    path('transactiondtl/',include('transactiondtl.urls')),
    path('acitem/',include('acitem.urls')),
    path('acitemuom/',include('acitemuom.urls')),
    path('acsalesagent/',include('acsalesagent.urls')),
    path('acterms/',include('acterms.urls')),
    path('acdebtor/',include('acdebtor.urls')),
    path('aciv/',include('aciv.urls')),
    path('acivdtl/',include('acivdtl.urls')),
    path("api/schema/",SpectacularAPIView.as_view(),name="schema"),
    path("api/schema/docs",SpectacularSwaggerView.as_view(url_name="schema")),
    path("_debug_/",include("debug_toolbar.urls"))
]
