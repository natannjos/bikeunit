from django.core.urlresolvers import reverse
from django.db import models


class Grupo(models.Model):

    def get_absolute_url(self):
        return reverse("view_grupo", args=[self.pk])


class Pedal(models.Model):
    grupo = models.ForeignKey(to='pedais.Grupo', default=None)
    destino = models.TextField(default='')

    def __str__(self):
        return self.destino

    class Meta:
        ordering = ('id', )
        unique_together = ('grupo', 'destino')