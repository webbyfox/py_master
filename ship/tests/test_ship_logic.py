# -*- coding: utf-8 -*-
from copy import deepcopy
from unittest import TestCase

from ship.exceptions import DuplicateError, NotFoundException
from ship.storage import ShipDjangoStorage, ShipPureMemoryStorage
from ship.logic import ShipLogic


class ShipLogicInterface:

    maxDiff = None

    ship_data = {
        'name': 'GOODSHIP COTTON',
        'imo_number': '1234567',
        'user_id': 1,
        'notes': None,
    }

    def tearDown(self):
        self.logic.storage.wipe()

    def test_create_ship(self):
        data = deepcopy(self.ship_data)
        actual = self.logic.create_ship(**data)

        self.assertTrue('id' in actual)
        del actual['id']

        self.assertTrue('created' in actual)
        del actual['created']

        self.assertTrue('modified' in actual)
        del actual['modified']

        self.assertEqual(actual['status'], 'ACTIVE')
        del actual['status']

        self.assertEqual(actual, self.ship_data)

    def test_create_ship_raises_duplicate_error(self):
        data = deepcopy(self.ship_data)
        self.logic.create_ship(**data)

        with self.assertRaises(DuplicateError):
            self.logic.create_ship(**data)

    def test_get_ships(self):
        data = deepcopy(self.ship_data)

        expected = self.logic.create_ship(**data)

        # We will create 10 additional ships that we don't expect to see
        # when we retrieve the ships by user_id later on.
        for index in range(9):
            data['imo_number'] = '765432{index}'.format(index=index)
            self.logic.create_ship(**data)

        # Create a ship for a different user that won't be returned when
        # retrieving ships
        data['user_id'] = 666
        self.logic.create_ship(**data)

        ships, total_count = self.logic.get_ships(
            user_ids=[self.ship_data['user_id']],
            order_by='-created',
        )

        self.assertEqual(total_count, 10)
        self.assertEqual(len(ships), 10)
        self.assertEqual(ships[0], expected)

    def test_update_ship(self):
        data = deepcopy(self.ship_data)
        ship = self.logic.create_ship(**data)

        expected = self.logic.update_ship(
            id=ship['id'],
            notes='Here are some fun notes',
        )

        ships, count = self.logic.get_ships(
            id=ship['id'],
        )
        self.assertEqual(count, 1)
        self.assertEqual(ships[0]['notes'], expected['notes'])

    def test_update_non_existent_ship_raises_not_found_exception(self):
        with self.assertRaises(NotFoundException):
            self.logic.update_ship(
                id=1234567889999,
                notes='Not found bud!'
            )

    def test_update_ship_user_id(self):
        data = deepcopy(self.ship_data)
        expected = self.logic.create_ship(**data)

        actual = self.logic.update_ship(
            id=expected['id'],
            user_id=1234,
        )

        self.assertEqual(actual['user_id'], expected['user_id'])

    def test_delete_ship(self):
        data = deepcopy(self.ship_data)
        ship = self.logic.create_ship(**data)

        actual = self.logic.delete_ship(ship['id'])
        self.assertEqual(actual['status'], 'DELETED')

        ships, count = self.logic.get_ships(id=ship['id'])
        self.assertEqual(count, 1)
        self.assertEqual(ships[0]['status'], 'DELETED')


class TestShipLogic_PureMemoryStorage(ShipLogicInterface, TestCase):

    storage = ShipPureMemoryStorage()
    logic = ShipLogic(storage)


class TestShipLogic_DjangoStorage(ShipLogicInterface, TestCase):

    storage = ShipDjangoStorage()
    logic = ShipLogic(storage)

