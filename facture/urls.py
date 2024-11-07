from django.urls import path
from facture.views import fac,Newcfacture,newclient,factures,pdf_file

urlpatterns =[
    path("",fac.as_view(), name ="homepage"),
    path("nouveau_fac",Newcfacture.as_view(),name="nouveau_fac"),
    path("nouveau_cl",newclient.as_view(),name="nouveau_cl"),
    path("vue/<int:pk>", factures.as_view(), name="facture_pdf"),
    # path("<int:pk>",voir_pdf, name="pdf"),
    path('<int:pk>',pdf_file, name="generer")
]