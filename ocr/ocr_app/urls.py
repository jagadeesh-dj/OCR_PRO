from django.urls import path
from ocr_app import views
urlpatterns=[
    path('',views.home,name='home'),
    path('upload/',views.upload,name='upload'),
    # path('data/',views.output,name='data'),
    path('txtfile/',views.txtfile,name="txtfile"),
    path('fileview/',views.fileview,name='fileview'),
    path('download/<str:file_name>/',views.download,name='download'),
    path('delete/<str:file_name>/',views.delete,name='delete'),
    path('edit/<str:file_name>/',views.edit,name='edit')
]