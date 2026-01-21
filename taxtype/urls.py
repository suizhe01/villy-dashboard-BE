#urls.py
from django.urls import include, path, include
from rest_framework import routers
from . import views


app_name = "taxtype"
router = routers.DefaultRouter()
router.register(r"taxtype", views.TaxTypeViewSet)
# router_parent = routers.SimpleRouter()
# router_parent.register(r"ml_MlItemmaster_parent", views.MlItemmasterViewSet_parent)
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("", include(router.urls)),
    # path("", include(router_parent.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]