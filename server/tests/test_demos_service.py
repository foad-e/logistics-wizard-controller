import unittest
from datetime import datetime
from json import loads
import server.services.demos as demo_service
from server.exceptions import (ValidationException,
                               UnprocessableEntityException,
                               ResourceDoesNotExistException)


###########################
#        Unit Tests       #
###########################

class CreateDemoTestCase(unittest.TestCase):
    """Tests for `services/demos.py - create_demo()`."""

    def test_demo_create_success(self):
        """With correct values, is a valid demo returned?"""

        # Create demo
        demo_name = datetime.now().isoformat("T")
        demo = demo_service.create_demo(demo_name)

        # TODO: Update to use assertIsInstance(a,b)
        # Check all expected object values are present
        demo_json = loads(demo)
        self.assertTrue(demo_json.get('id'))
        self.assertTrue(demo_json.get('guid'))
        self.assertTrue(demo_json.get('name') == demo_name)
        self.assertTrue(demo_json.get('createdAt'))
        self.assertTrue(demo_json.get('users'))

        # Check that the default supplychainmanager user was created
        created_user_json = demo_json.get('users')[0]
        self.assertTrue(created_user_json.get('id'))
        self.assertTrue(created_user_json.get('demoId'))
        self.assertTrue(created_user_json.get('username'))
        self.assertTrue(created_user_json.get('email'))
        self.assertTrue(created_user_json.get('roles'))

        # Check that the proper role was created
        scm_role_json = created_user_json.get('roles')[0]
        self.assertTrue(scm_role_json.get('id'))
        self.assertTrue(scm_role_json.get('name') == "supplychainmanager")
        self.assertTrue(scm_role_json.get('created'))
        self.assertTrue(scm_role_json.get('modified'))

        # Destroy demo
        demo_service.delete_demo_by_guid(demo_json.get('guid'))

    def test_demo_create_email(self):
        """Is an invalid email detected correctly?"""

        # Test invalid email throws ValidationException
        demo_name = datetime.now().isoformat("T")
        invalid_email = "email@example@example.com"
        self.assertRaises(UnprocessableEntityException,
                          demo_service.create_demo,
                          demo_name, invalid_email)

        # Test valid email completes
        demo_name = datetime.now().isoformat("T")
        invalid_email = "firstname-lastname@example.com"
        demo = demo_service.create_demo(demo_name, invalid_email)
        self.assertTrue(loads(demo).get('id'))


class RetrieveDemoTestCase(unittest.TestCase):
    """Tests for `services/demos.py - get_demo_by_guid()`."""

    def test_demo_retrieve_success(self):
        """With correct values, is a valid demo returned?"""

        # Create and then retrieve demo
        demo_name = datetime.now().isoformat("T")
        created_demo = demo_service.create_demo(demo_name)
        retrieved_demo = demo_service.get_demo_by_guid(loads(created_demo).get('guid'))

        # TODO: Update to use assertIsInstance(a,b)
        # Check all expected object values are present
        demo_json = loads(retrieved_demo)
        self.assertTrue(demo_json.get('id') == loads(created_demo).get('id'))
        self.assertTrue(demo_json.get('guid') == loads(created_demo).get('guid'))
        self.assertTrue(demo_json.get('name') == loads(created_demo).get('name'))
        self.assertTrue(demo_json.get('createdAt') == loads(created_demo).get('createdAt'))
        self.assertTrue(demo_json.get('users'))

        # Check that the users are valid
        for user_json in demo_json.get('users'):
            self.assertTrue(user_json.get('id'))
            self.assertTrue(user_json.get('demoId'))
            self.assertTrue(user_json.get('username'))
            self.assertTrue(user_json.get('email'))

            # Check that user roles are valid, if present
            if user_json.get('roles'):
                for role_json in user_json.get('roles'):
                    self.assertTrue(role_json.get('id'))
                    self.assertTrue(role_json.get('name'))
                    self.assertTrue(role_json.get('created'))
                    self.assertTrue(role_json.get('modified'))

        # Destroy demo
        demo_service.delete_demo_by_guid(demo_json.get('guid'))

    def test_demo_retrieve_invalid_input(self):
        """With invalid guid, is correct error thrown?"""

        # Attempt to retrieve demo with invalid guid
        self.assertRaises(ResourceDoesNotExistException,
                          demo_service.get_demo_by_guid,
                          'ABC123')


class DeleteDemoTestCase(unittest.TestCase):
    """Tests for `services/demos.py - delete_demo_by_guid()`."""

    def test_demo_delete_success(self):
        """With correct values, is a valid demo deleted?"""

        # Create demo
        demo_name = datetime.now().isoformat("T")
        demo = demo_service.create_demo(demo_name)

        # Destroy demo and check for successful return
        self.assertTrue(demo_service.delete_demo_by_guid(loads(demo).get('guid')) is None)

    def test_demo_delete_invalid_input(self):
        """With invalid guid, is correct error thrown?"""

        # Attempt to delete demo with invalid guid
        self.assertRaises(ResourceDoesNotExistException,
                          demo_service.delete_demo_by_guid,
                          'ABC123')


class RetrieveDemoRetailersTestCase(unittest.TestCase):
    """Tests for `services/demos.py - get_demo_retailers()`."""

    def test_demo_retrieve_retailers_success(self):
        """With correct values, are valid demo retailers returned?"""

        # Create and then retrieve demo
        demo_name = datetime.now().isoformat("T")
        created_demo = demo_service.create_demo(demo_name)
        demo_guid = loads(created_demo).get('guid')
        retailers = demo_service.get_demo_retailers(demo_guid)
        retailers_json = loads(retailers)

        # TODO: Update to use assertIsInstance(a,b)
        # Check that the retailers are valid
        for retailer_json in retailers_json:
            self.assertTrue(retailer_json.get('id'))
            self.assertTrue(retailer_json.get('address'))

            address_json = retailer_json.get('address')
            self.assertTrue(address_json.get('city'))
            self.assertTrue(address_json.get('state'))
            self.assertTrue(address_json.get('country'))
            self.assertTrue(address_json.get('latitude'))
            self.assertTrue(address_json.get('longitude'))

        # Destroy demo
        demo_service.delete_demo_by_guid(demo_guid)


if __name__ == '__main__':
    unittest.main()