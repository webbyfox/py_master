# -*- coding: utf-8 -*-
from copy import deepcopy
from unittest import TestCase

from ship.exceptions import DuplicateError, NotFoundException
from ship.storage import ShipDjangoStorage, ShipPureMemoryStorage


class ShipStorageInterface:

    maxDiff = None

    ship_data = {
        'name': 'GOODSHIP COTTON',
        'imo_number': '1234567',
        'user_id': 1,
        'notes': None,
    }

    def tearDown(self):
        self.storage.wipe()

    def test_persist_ship(self):
        data = deepcopy(self.ship_data)
        actual = self.storage.persist_ship(**data)

        self.assertTrue('id' in actual)
        del actual['id']

        self.assertTrue('created' in actual)
        del actual['created']

        self.assertTrue('modified' in actual)
        del actual['modified']

        self.assertEqual(actual['status'], 'ACTIVE')
        del actual['status']

        self.assertEqual(actual, self.ship_data)

    def test_persist_ship_raises_duplicate_error(self):
        data = deepcopy(self.ship_data)
        self.storage.persist_ship(**data)

        with self.assertRaises(DuplicateError):
            self.storage.persist_ship(**data)

    def test_retrieve_ships(self):
        data = deepcopy(self.ship_data)

        expected = self.storage.persist_ship(**data)

        # We will create 10 additional ships that we don't expect to see
        # when we retrieve the ships by user_id later on.
        for index in range(9):
            data['imo_number'] = '765432{index}'.format(index=index)
            self.storage.persist_ship(**data)

        # Create a ship for a different user that won't be returned when
        # retrieving ships
        data['user_id'] = 666
        self.storage.persist_ship(**data)

        ships, total_count = self.storage.retrieve_ships(
            user_ids=[self.ship_data['user_id']],
            order_by='-created',
        )

        self.assertEqual(total_count, 10)
        self.assertEqual(len(ships), 10)
        self.assertEqual(ships[0], expected)

    def test_update_ship(self):
        data = deepcopy(self.ship_data)
        ship = self.storage.persist_ship(**data)

        expected = self.storage.update_ship(
            id=ship['id'],
            notes='Here are some fun notes',
        )

        ships, count = self.storage.retrieve_ships(
            id=ship['id'],
        )
        self.assertEqual(count, 1)
        self.assertEqual(ships[0]['notes'], expected['notes'])

    def test_update_non_existent_ship_raises_not_found_exception(self):
        with self.assertRaises(NotFoundException):
            self.storage.update_ship(
                id=1234567889999,
                notes='Not found bud!'
            )

    def test_update_ship_user_id(self):
        data = deepcopy(self.ship_data)
        expected = self.storage.persist_ship(**data)

        actual = self.storage.update_ship(
            id=expected['id'],
            user_id=1234,
        )

        self.assertEqual(actual['user_id'], expected['user_id'])

    def test_delete_ship(self):
        data = deepcopy(self.ship_data)
        ship = self.storage.persist_ship(**data)

        actual = self.storage.delete_ship(ship['id'])
        self.assertEqual(actual['status'], 'DELETED')

        ships, count = self.storage.retrieve_ships(id=ship['id'])
        self.assertEqual(count, 1)
        self.assertEqual(ships[0]['status'], 'DELETED')


class TestShipPureMemoryStorage(ShipStorageInterface, TestCase):

    storage = ShipPureMemoryStorage()


class TestShipDjangoStorage(ShipStorageInterface, TestCase):

    storage = ShipDjangoStorage()
