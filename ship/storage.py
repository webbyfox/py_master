# -*- coding: utf-8 -*-
# pylint: disable=redefined-builtin
"""
Storage classes allows us to rapidly change out which backend we want to
use. This should be as simple as changing one line of code:

    logic = ShipLogic(storage=ShipMongoStorage())

assuming we have written ``ShipMongoStorage``.

Using a StorageInterface class to define the test cases we wish to run
we can run a test suite against multiple backends and ensure that no matter
which storage we use we will always get the same results.
"""
import logging

from django.db import IntegrityError

from .exceptions import DuplicateError, NotFoundException
from .models import Ship


logger = logging.getLogger(__name__)


class ShipPureMemoryStorage:

    def wipe(self):
        """ Used during testing to ensure each unittest is indepedent. """

    def persist_ship(
        self,
        name,
        imo_number,
        user_id,
        status='ACTIVE',
        notes=None,
    ):
        """ Persists the ship into storage.

        Args:
            name (str): The name of the ship.
            imo_number (str): A 7 digit string for the ship's IMO.
            user_id (str): The ID of the user who owns the ship.
            status (`obj`:str, optional): An optional status string. Defaults
                to ``ACTIVE``.
            notes (`obj`:str, optional): An optional string to add notes to the
                ship.

        Returns:
            dict: Serialized ship object which is now in the storage.
        """
        #raise NotImplementedError('This must be implemented!')
        ship = Ship()
        ship.name = name
        ship.imo_number = imo_number
        ship.user_id = user_id
        ship.status = status
        ship.notes = notes

        return dict(
        (name, getattr(ship, name)) for name in dir(f) if not name.startswith('__')
        )

    def retrieve_ships(
        self,
        id=None,
        ids=None,
        user_ids=None,
        status=None,
        order_by=None,
    ):
        """ Retrieve a list of ships for given params and order if required.

        Args:
            id (`obj`:int, optional): The ID of the given ship to be retrieved.
            ids (`obj`:list, optional): A list of IDs of ships to be retrieved.
            user_ids (`obj`:list, optional): A list of user IDs whos ships
                need to be retrieved.
            status (`obj`:string, optional): The status of ships to be
                retrieved.
            order_by (`obj`:str, optional): The field on which to sort the
                retrieved ships by.

        Returns:
            tuple: (list, int) - List of serialized ship objects. Int the total
                count of ship objects found.
        """
        #raise NotImplementedError('This must be implemented!')
        ship = ship()


    def update_ship(self, id, **kwargs):
        """ Update details of a ship.

        Args:
            id (int): The ID of the ship to be updated
            kwargs (dict): Key-value pair that we use to setattr() to ship
                before saving it.

        Returns:
            dict: A serialized ship object that has been updated in storage.

        Raises:
            NotFoundException: If the ship was not found.
        """
        raise NotImplementedError('This must be implemented!')

    def delete_ship(self, id, user_id):
        """ Set the ship's status to ``DELETED``.

        Args:
            id (int): The ID of the ship's status to set to DELETED

        Raises:
            NotFoundException: If the ship was not found.
        """
        raise NotImplementedError('This must be implemented!')


class ShipDjangoStorage:

    ship_model = Ship

    INTEGRITY_ERROR_ARG = (
        'UNIQUE constraint failed: ship_ship.imo_number, ship_ship.user_id'
    )

    def wipe(self):
        """ Used during testing to ensure each unittest is indepedent. """
        self.ship_model.objects.all().delete()

    @staticmethod
    def _serialize_ship(obj):
        """ Serialize a ship object in to a ``dict`` object.

        Args:
            obj (`obj`:Ship): A ship object that exists in the database.

        Returns:
            dict: A serialized ship object.
        """
        return {
            'created': obj.created,
            'id': obj.id,
            'imo_number': obj.imo_number,
            'modified': obj.modified,
            'name': obj.name,
            'notes': obj.notes,
            'status': obj.status,
            'user_id': obj.user_id,
        }

    def persist_ship(
        self,
        name,
        imo_number,
        user_id,
        status='ACTIVE',
        notes=None,
    ):
        """ Persists the ship into storage.

        Args:
            name (str): The name of the ship.
            imo_number (str): A 7 digit string for the ship's IMO.
            user_id (str): The ID of the user who owns the ship.
            status (`obj`:str, optional): An optional status string. Defaults
                to ``ACTIVE``.
            notes (`obj`:str, optional): An optional string to add notes to the
                ship.

        Returns:
            dict: Serialized ship object which is now in the storage.
        """
        try:
            ship = self.ship_model.objects.create(
                name=name,
                imo_number=imo_number,
                user_id=user_id,
                status=status,
                notes=notes,
            )
        except Exception as err:  # pylint: disable=broad-except
            logger.exception('Oops something went wrong persisting a ship.')
            if (
                isinstance(err, IntegrityError) and
                err.args == (self.INTEGRITY_ERROR_ARG,)
            ):
                raise DuplicateError(err)
            else:
                raise err

        return self._serialize_ship(ship)

    def retrieve_ships(
        self,
        id=None,
        ids=None,
        user_ids=None,
        status=None,
        order_by=None,
    ):
        """ Retrieve a list of ships for given params and order if required.

        Args:
            id (`obj`:int, optional): The ID of the given ship to be retrieved.
            ids (`obj`:list, optional): A list of IDs of ships to be retrieved.
            user_ids (`obj`:list, optional): A list of user IDs whos ships
                need to be retrieved.
            status (`obj`:string, optional): The status of ships to be
                retrieved.
            order_by (`obj`:str, optional): The field on which to sort the
                retrieved ships by.

        Returns:
            tuple: (list, int) - List of serialized ship objects. Int the total
                count of ship objects found.
        """
        ships = self.ship_model.objects.all()

        if id:
            ships = ships.filter(id=id)

        if ids:
            ships = ships.filter(id__in=ids)

        if user_ids:
            ships = ships.filter(user_id__in=user_ids)

        if status:
            ships = ships.filter(status=status)

        if order_by:
            ships.order_by(order_by)

        total_count = ships.count()
        serialized_ships = [
            self._serialize_ship(ship)
            for ship in ships
        ]

        return serialized_ships, total_count

    def update_ship(self, id, **kwargs):
        """ Update details of a ship.

        Args:
            id (int): The ID of the ship to be updated
            kwargs (dict): Key-value pair that we use to setattr() to ship
                before saving it.

        Returns:
            dict: A serialized ship object that has been updated in storage.

        Raises:
            NotFoundException: If the ship was not found.
        """
        if 'user_id' in kwargs:
            logger.debug('Cannot change the owner of the ship.')
            del kwargs['user_id']

        try:
            ship = self.ship_model.objects.get(id=id)
        except self.ship_model.DoesNotExist:
            raise NotFoundException

        # Naively set attribute values on an object. If the key is not a valid
        # attribute key then ``.save()`` should succeed without any issues.
        for key, value in kwargs.items():
            setattr(ship, key, value)

        ship.save()

        return self._serialize_ship(ship)

    def delete_ship(self, id):
        """ Set the ship's status to ``DELETED``.

        Args:
            id (int): The ID of the ship's status to set to DELETED

        Raises:
            NotFoundException: If the ship was not found.
        """
        return self.update_ship(id=id, status='DELETED')
