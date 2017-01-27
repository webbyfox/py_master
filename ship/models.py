# -*- coding: utf-8 -*-
from django.db import models


class Ship(models.Model):

    name = models.CharField(max_length=127, blank=False, null=False)
    imo_number = models.CharField(max_length=7, blank=False, null=False)
    user_id = models.PositiveIntegerField(blank=False, null=False)
    modified = models.DateTimeField(auto_now=True, blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    notes = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=7,
        blank=False,
        null=False,
        default='ACTIVE',
        choices=(('ACTIVE', 'ACTIVE'), ('DELETED', 'DELETED'))
    )

    class Meta:
        unique_together = (
            ('imo_number', 'user_id'),
        )

    def __str__(self):
        return '{name} -- {imo_number}'.format(
            name=self.name,
            imo_number=self.imo_number,
        )
