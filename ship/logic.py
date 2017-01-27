# -*- coding: utf-8 -*-
# pylint: disable=redefined-builtin
"""
Logic classes allow us to write pure Python with interchangeable backends or
"storages". Typically, a logic class would have more complex things in it
besides this very basic CRUD implmentation.
"""


class ShipLogic:

    def __init__(self, storage):
        self.storage = storage

    def create_ship(
        self,
        name,
        imo_number,
        user_id,
        status='ACTIVE',
        notes=None,
    ):
        """ Create a ship object.

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
        return self.storage.persist_ship(
            name=name,
            user_id=user_id,
            imo_number=imo_number,
            notes=notes,
            status=status,
        )

    def get_ships(
        self,
        id=None,
        ids=None,
        user_ids=None,
        status=None,
        order_by=None,
    ):
        """ Retrieve a list of ships for given params, ordered and limited.

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
        return self.storage.retrieve_ships(
            id=id,
            ids=ids,
            user_ids=user_ids,
            status=status,
            order_by=order_by,
        )

    def update_ship(self, id, **kwargs):
        """ Update details of a ship.

        Args:
            id (int): The ID of the ship to be updated.
            kwargs (dict): Key-value pair that we use to setattr() to ship
                before saving it.

        Returns:
            dict: A serialized ship object that has been updated in storage.

        Raises:
            NotFoundException: If the ship was not found.
        """
        return self.storage.update_ship(
            id=id,
            **kwargs
        )

    def delete_ship(self, id):
        """ Set the ship's status to ``DELETED``.

        Args:
            id (int): The ID of the ship's status to set to DELETED

        Raises:
            NotFoundException: If the ship was not found.
        """
        return self.storage.delete_ship(
            id=id,
        )
