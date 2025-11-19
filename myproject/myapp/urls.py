
from django.urls import path
from . import views

urlpatterns = [
    # path('',views.add,name = 'add'),
    path('',views.sample_view,name = "sample_view"),
    path('',views.addstudents,name = "addstuents"),
    # path('',views.job1,name = "job1")
]