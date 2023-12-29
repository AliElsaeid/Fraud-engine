
from django.contrib import admin
from django.urls import path , include
from engine.views import index


urlpatterns = [
    path('admin/', admin.site.urls),
      path('api/', include('engine.urls' , namespace='engine')),
      path('',index , name='index'),

     

]
