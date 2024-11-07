from django.contrib import admin
from .models import *

# Register your models here.
class  adminclient (admin.ModelAdmin):
    list_display =("nom","Email","phone","quartier","enregistré_par","sexe","age","adresse","date")
    

class adminfacture(admin.ModelAdmin):
    list_display=("client","Administrateur","date_creation","total","payer","dernière_modification","type_facture","commentaire")


admin.site.register(client,adminclient)
admin.site.register(facture,adminfacture)
admin.site.register(articles)