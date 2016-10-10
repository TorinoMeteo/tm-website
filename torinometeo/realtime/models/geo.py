from django.db import models

# Geography

class Nation(models.Model):
    """ Nations
    """
    name = models.CharField('nome', max_length=64)
    alpha2_code = models.CharField('alpha2 code', max_length=2)
    alpha3_code = models.CharField('alpha3 code', max_length=3)
    numeric_code = models.CharField('codice numerico', max_length=4)
    rank = models.IntegerField('importanza')

    class Meta:
        verbose_name = 'nazione'
        verbose_name_plural = 'nazioni'
        ordering = ('rank', 'name', )

    def __unicode__(self):
        return self.name

class Region(models.Model):
    """ Regions
    """
    nation = models.ForeignKey(Nation, verbose_name='nazione')
    name = models.CharField('nome', max_length=64)
    rank = models.IntegerField('importanza')

    class Meta:
        verbose_name = 'regione'
        verbose_name_plural = 'regioni'
        ordering = ('nation__rank', 'rank', 'name', )

    def __unicode__(self):
        return self.name

class Province(models.Model):
    """ Provinces
    """
    region = models.ForeignKey(Region, verbose_name='regione')
    name = models.CharField('nome', max_length=64)
    rank = models.IntegerField('importanza')

    class Meta:
        verbose_name = 'provincia'
        verbose_name_plural = 'province'

    def __unicode__(self):
        return self.name
