from django.db import models
from django.contrib.auth.models import User
# Create your models here.


choix =[
    ('M',"Masculin"),
    ('F',"Feminin")
]

type_facture =[
    ('R',"Réçue"),
    ('P',"Proformat"),
    ('F',"Facture")
]

class client(models.Model):
    """
    nom = table des clients
    """
    nom =models.CharField(max_length=100)
    Email = models.EmailField()
    phone = models.CharField(max_length =20)
    quartier = models.CharField(max_length=12)
    enregistré_par =models.ForeignKey(User, on_delete=models.PROTECT)
    sexe = models.CharField(max_length=1,choices=choix)
    age = models.CharField(max_length=10)
    adresse = models.CharField(max_length=30)
    date = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name ="client"
        verbose_name_plural ="clients"


    def __str__(self):
        return self.nom
    

class facture(models.Model):
    """
    nom = tables de factures
    """
    client = models.ForeignKey(client, on_delete=models.PROTECT)
    Administrateur =models.ForeignKey(User, on_delete=models.PROTECT)
    date_creation= models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=500,decimal_places=2)
    payer = models.BooleanField(default =False)
    dernière_modification =models.DateTimeField(auto_now_add=True)
    type_facture =models.CharField(max_length=10, choices=type_facture)
    commentaire = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name ="Facture"
        verbose_name_plural ="Factures"
    
    def __str__(self):
        return f"{self.client.nom}_{self.date_creation}"
    
    @property
    def get_total(self):
        articls = self.articles_set.all()
        total = sum(articl.get_total for articl in articls)
        return total
    

class articles(models.Model):
    """
    nom = table des articles
    Description = liste des articles disponible dans la boutique
    """
    facture =models.ForeignKey(facture, on_delete=models.CASCADE)
    nom = models.CharField(max_length=32)
    prix_unitaire =models.DecimalField(max_digits=100000,decimal_places=2)
    quantité = models.IntegerField()
    total = models.DecimalField(max_digits=100000, decimal_places=2)

    class Meta :
        verbose_name = "Article"
        verbose_name_plural ="Articles"

    def __str__(self):
        return self.nom
    
    @property
    def get_total(self):
        total = self.quantité * self.prix_unitaire
        return total

    
    
