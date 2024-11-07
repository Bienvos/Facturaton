from django.core.paginator import (Paginator,EmptyPage,PageNotAnInteger)
from .models import *


def pagination(request, invoices):
    # page par defaut
        default_page =1
        page = request.GET.get('page',default_page)
        
        # elements par page
        items_per_page =4

        paginator=Paginator(invoices,items_per_page)


        try:

            element = paginator.page(page)

        except PageNotAnInteger:
            element = paginator.page(default_page)

        except EmptyPage:
            element = paginator.page(paginator.num_pages)
        
        return element

def get_obj(pk):
     
    obj = facture.objects.get(pk=pk)
    article = obj.articles_set.all()

    context ={
            'obj':obj,
            'articles':article
        }

    return context
     