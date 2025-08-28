from django.db import models


class Sanisette(models.Model):
    type = models.CharField(max_length=50)
    adresse = models.CharField(max_length=255)
    complement_adresse = models.CharField(max_length=255, blank=True, null=True)
    arrondissement = models.CharField(max_length=5)
    horaire = models.CharField(max_length=100, blank=True, null=True)
    acces_pmr = models.CharField(max_length=10, blank=True, null=True)
    relais_bebe = models.CharField(max_length=10, blank=True, null=True)
    url_fiche_equipement = models.URLField(blank=True, null=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    gestionnaire = models.CharField(max_length=255, blank=True, null=True)
    source = models.URLField(blank=True, null=True)

    class Meta:
        unique_together = ("adresse", "latitude", "longitude")

    def __str__(self):
        return f"{self.adresse} ({self.arrondissement})"
