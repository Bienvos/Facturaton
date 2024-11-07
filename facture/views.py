from django.shortcuts import render
from django.views import View
from .models import facture,client,articles
from django.contrib import messages
from django.db import transaction
from .utils import pagination,get_obj


from django.http import HttpResponse
from django.template.loader import get_template
import pdfkit
import datetime
# import io 
#from io import BytesIO
# from xhtml2pdf import pisa







#test pour creation des permissions
#from django.contrib.auth.decorators import login_required
#from django.contrib.auth.mixins import LoginRequiredMixin
# import datetime
# import pdfkit
# from django.template.loader import get_template
# from django.http import HttpResponse

# Create your views here.

class fac(View):
    """ Vue sur tous les factures"""

    template_name ="index.html"
    invoices =facture.objects.select_related('client','Administrateur').all().order_by('-date_creation')

    context ={
        "invoices":invoices
    }

    def get(self,request,*args,**kwargs):

        items = pagination(request,self.invoices)

        self.context['invoices'] = items

        return render(request,self.template_name,self.context)
    

    def post(self,request,*args,**kwargs):
            #    modal modifier
            
        if request.POST.get('id_modified'):
            
            payer = request.POST.get('modified')

            try:
                obj = facture.objects.get(id = request.POST.get('id_modified'))
                if payer =="True":
                    obj.payer = True
                else :
                    obj.payer = False

                obj.save()

                messages.success(request, " Facture Modifier avec Succès !!!")


            except Exception as e:
                
                messages.error(request , f"Désole ,nous avons rencontrer un probleme de type {e}")
            
            # modal supprimer

        

        if request.POST.get('id_supprimer'):

            try:
                obj = facture.objects.get(pk=request.POST.get('id_supprimer'))
                obj.delete()
                messages.success(request,"Facture supprimer avec succès !!")
            except Exception as e :
                messages.error(request,f" Erreur de type {e}")

        

            
        items = pagination(request,self.invoices)

        self.context['invoices'] = items

        return render(request,self.template_name,self.context)
       

    

       
    

class Newcfacture(View):
    """ Vue sur nouveau client"""
    template_name ="facture.html"

    def get(self,request,*args,**kwargs):
        return render(request,self.template_name)
    
    def post(self,request,*args,**kwargs):
        donnes ={
            "nom":request.POST.get("nom"),
            "Email":request.POST.get("Email"),
            "phone":request.POST.get("Phone"),
            "sexe":request.POST.get("sexe"),
            "age":request.POST.get("Age"),
            "adresse":request.POST.get("Adresse"),
            "quartier": request.POST.get("quartier"),
            "enregistré_par":request.user
        }

        created =client.objects.create(**donnes)

        try:
            if created:

             messages.success(request," Le client a éte ajouter avec succès !")
        
            else:
             messages.error(request,"Erreur d'enregistrement, essayer encore !")

        except Exception as e :
           messages.error(request, f" le systeme a detecte une erreur provenant du serveur de type{e}")
            
        

        return render(request,self.template_name)
    

class newclient(View):
       """ Vue d'ajout de la facture """

       client1 =client.objects.select_related('enregistré_par').all()

       context = {
          "clients":client1
       }
       template_name ="client.html"
       def get(self,request,*args, **kwargs):
          return render(request,self.template_name,self.context)
       

       @transaction.atomic()
       def post(self,request,*args,**kwargs):
          """ vue permettant d'enregistrer tous
              les elements de la facture
          """


          elements=[]


          try:
              cl = request.POST.get('client')
              type =request.POST.get('type_facture')
              article =request.POST.getlist('article')
              qte = request.POST.getlist('qte')
              unit = request.POST.getlist('unit-a')
              total_a = request.POST.getlist('total-a')
              total = request.POST.get('total')
              commentaire =request.POST.get('commentaire')

              donnees ={
                  'client_id':cl,
                  'Administrateur': request.user,
                  'total':total,
                  'type_facture':type,
                  'commentaire':commentaire
              }

              fact = facture.objects.create(**donnees)


              for index,art in enumerate(article):
                  data = articles(
                      facture_id = fact.id,
                      nom = art,
                      prix_unitaire = unit[index],
                      quantité =qte[index],
                      total = total_a[index],
                  )

                  elements.append(data)

              created = articles.objects.bulk_create(elements)

              if created :
                  messages.success(request,"La Facture a été enregidtrer avec succès !")
              else :
                 messages.error(request,"Erreur d'enregistrement , ressayer encore ")

          except Exception as e:
                messages.error(request,f"désole une erreur de type {e} est survenu")

            
               

                
              
          return render(request,self.template_name,self.context)


class factures(View):
    """ cette vue permet de visualiser une facture"""
    template_name ="fac_pdf.html"
    
    def get(self,request,*args,**kwargs):

        pk = kwargs.get('pk')

        context =get_obj(pk)
        

        

        return render(request,self.template_name,context)










# def generer(request,id):
#     factur = facture.objects.get(pk=id)
#     # artcless =articles.objects.() 
#     obj_name =factur.client.nom
#     obj_adresse = factur.client.adresse
#     obj_date = factur.date_creation

#     template = get_template('factures.html')
#     context = {'obj_name':obj_name, 'obj_adresse':obj_adresse,'obj_date':obj_date}
#     html = template.render(context)
#     options={
#         'page-size':'letter',
#         'encoding':'UTF-8'
#     }

#     pdf = pdfkit.from_string(html,False,options)
#     reponse = HttpResponse(pdf,content_type='application/pdf')
#     reponse['Content-Disposition'] = "attachment"
#     return reponse


# ------------------------------------------------------------------------------------------------
# def voir_pdf(request,*args,**kwargs):
#     pk = kwargs.get('pk')
#     context = get_obj(pk)

#     template_path = 'factures.html'
#     context = {'obj': context}
#     # # Create a Django response object, and specify content_type as pdf
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'filename="facture"'
#     # # find the template and render it.
#     template = get_template(template_path)
#     html = template.render(context)

#     # # create a pdf
#     pisa_status = pisa.CreatePDF(html, response)
#     # # if error then show some funny view
#     if pisa_status.err:
#        return HttpResponse('We had some errors <pre>' + html + '</pre>')
#     return response
    #--------------------------------------------------------------------------
    #    pk = kwargs.get('pk')
    #    context = get_obj(pk)

    #    html = render_to_string("invoice-pdf.html",context)
    #    result = BytesIO()

    #    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)

    #    if not pdf.err:
    #         response = HttpResponse(result.getvalue(), content_type='application/pdf')
    #         response['Content-Disposition'] = 'attachment; filename="Facture_Entrep.pdf"'
    #         return response
    #    else:
    #       return HttpResponse('Erreur lors de la génération du PDF', status=500)
    

    

    
def pdf_file(request , *args, **kwargs):
    """ cette vue permet de generer un pdf du fichier html"""
    pk = kwargs.get('pk')
    context = get_obj(pk)
    context['date']=datetime.datetime.today()

   # obtenir le fichier html a  generer le pdf

    template = get_template('factures.html')

   # renvoyer les variables du context directement dans le template
    html = template.render(context)

    # chemin vers wkhtmltopdf

#     # chemin = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
#     # Configurez pdfkit pour utiliser ce chemin
#     # config = pdfkit.configuration(wkhtmltopdf =chemin)

#     #fichier de sortie
#     #out_path ="fichier.pdf"

  # options du pdf

    options ={
        'page-size': 'Letter',
        'encoding': 'UTF-8'
    }
    
    # generation du pdf
    

    pdf=pdfkit.from_string(html,False,options=options)

    reponse = HttpResponse(pdf, content_type ='application/pdf')
    reponse['Content-Disposition']= "attachement"
    return reponse



    
    








    
    
