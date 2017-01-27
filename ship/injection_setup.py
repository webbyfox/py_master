# -*- coding: utf-8 -*-
# pylint: disable=unused-import
from .logic import ShipLogic
from .storage import ShipDjangoStorage, ShipPureMemoryStorage


storage = ShipPureMemoryStorage()

# Uncommenting the line below allows to see the applications working using the
# django ORM.
# storage = ShipDjangoStorage()

logic = ShipLogic(storage=storage)
