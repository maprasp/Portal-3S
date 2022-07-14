from django.db import models


class Prometheus(models.Model):
    jobname = models.CharField("nome", max_length=255)
    porta = models.IntegerField("prioridade")

    def __str__(self):
        return self.jobname
