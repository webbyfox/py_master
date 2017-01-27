################################
Pole Star Python Assessment Test
################################

The Assessment
--------------

There are currently 7 ``NotImplmentedErrors`` raised if you run the tests (``./manage.py test``) you will receive something similar to:

  Ran 28 tests in 0.023s
  
  FAILED (errors=14)

Implement the 7 methods and make the tests pass:

* ``ship.serializers:ShipSerializer.create``
* ``ship.serializers:ShipSerializer.update``
* ``ship.storage:ShipPureMemoryStorage.persist_ship``
* ``ship.storage:ShipPureMemoryStorage.retrieve_ships``
* ``ship.storage:ShipPureMemoryStorage.update_ship``
* ``ship.storage:ShipPureMemoryStorage.delete_ship``

Check your implementation by using the pre-created users (included in the ``db.sqlite3`` database):

**assessor** user:

  http://localhost:8000/api/v1/ships/?auth_token=58195d745e92851dab1fc05ebc74eee36f8c76ab

**user2** user:

  http://localhost:8000/api/v1/ships/?auth_token=bc42658f4b1dde1447ecdb201c782148648298b5


Setup
-----

Setup the project as you normally would using virtualenv. Then ``pip install -r requirements.txt`` to install Django and Django REST framework.

Users
-----

Using the include ``db.sqlite3`` database two users have been created

+----------+------------------------------------------+
| Username |Token                                     |
+==========+==========================================+
| assessor | 58195d745e92851dab1fc05ebc74eee36f8c76ab |
+----------+------------------------------------------+
| user2    | bc42658f4b1dde1447ecdb201c782148648298b5 |
+----------+------------------------------------------+

Background, Dependency Injection and what are these storage.py and logic.py files!
----------------------------------------------------------------------------------

We use a form of dependency injection. That's why when you enter the ``ship`` directory you see ``storage.py``, ``logic.py`` and ``injection_setup.py``

Storage
-------
Storage classes allows us to rapidly change out which backend we want to
use. This should be as simple as changing one line of code:

    logic = ShipLogic(storage=ShipMongoStorage())
    
assuming we have written ``ShipMongoStorage``.
Using a StorageInterface class (in ``tests``) to define the test cases we wish
to run we can run a test suite against multiple backends and ensure that no
matter which storage we use in production we will always get the same results.

Logic
-----
Logic classes allow us to write pure Python with interchangeable backends or
"storages". Typically, a logic class would have more complex things in it
besides this very basic CRUD implmentation.

Having ``logic.py`` files also allows us to collect all of our business logic
in one place and not have it scattered across ``models.py``, ``views.py`` or 
in the templates themselves!!
