from django.urls import path
from .views import RequestValidation


app_name='engine'

urlpatterns = [
 path('validate-request/', RequestValidation.as_view(), name='validate-request'),
           
]


