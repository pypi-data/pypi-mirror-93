import uuid
from functools import partial

import pytest

from dli.client.exceptions import CatalogueEntityNotFoundException
from tests.common import SdkIntegrationTestCase


@pytest.mark.integration
class PackageTestCase(SdkIntegrationTestCase):

    def test_get_unknown_package_raises_package_not_found(self):
        with self.assertRaises(CatalogueEntityNotFoundException):
            self.client.get_package(name="unknown")


    @pytest.mark.xfail(reason="Need to figure out how to mock permissions")
    def test_can_get_package_by_id_or_name(self):
        package_id = self.create_package(
            name="test_get_package_returns_non_siren_response"
        )
        package = self.client.get_package(package_id)
        self.assertEqual(package.id, package_id)

        package_by_name = self.client.get_package(name=package.name)
        self.assertEqual(package_by_name.id, package_id)

    def test_cannot_get_package_without_package_id_or_name(self):
        with self.assertRaises(ValueError):
            self.client.get_package(None)

    def test_get_datasets_in_package(self):
        client = self.client
        package_id = self.create_package("test_get_datasets_in_package")
        builder = self.dataset_builder(package_id, "test_package_functions").with_external_storage("somewhere")
        self.client.register_dataset(builder)
        datasets = client.get_package_datasets(package_id)
        self.assertEqual(len(datasets), 1)

    def test_can_delete_package(self):
        package_id = self.create_package(
            "test_can_delete_package"
        )
        self.client.delete_package(package_id)
        with self.assertRaises(CatalogueEntityNotFoundException):
            self.client.get_package(package_id)

    def test_delete_unknown_package_raises_exception(self):
        with self.assertRaises(CatalogueEntityNotFoundException):
            self.client.delete_package("unknown")


@pytest.mark.integration
class EditPackageTestCase(SdkIntegrationTestCase):

    def setUp(self):
        super().setUp()

        self.create = partial(
            self.client.register_package,
            name="EditPackageTestCase" + str(uuid.uuid4()),
            description="my package description",
            topic="Automotive",
            access="Restricted",
            internal_data="Yes",
            data_sensitivity="Public",
            terms_and_conditions="Terms",
            publisher="Bloomberg",
            access_manager_id="datalake-mgmt",
            tech_data_ops_id="datalake-mgmt",
            manager_id="datalake-mgmt"
        )

    def test_edit_unknown_package_raises_unknown_package_exception(self):
        with self.assertRaises(CatalogueEntityNotFoundException):
            self.client.edit_package(package_id="unknown")

    def test_edit_package_should_ignore_extra_keys_and_succeed_when_unknown_key_passed_with_kwargs(self):
        package = self.create()
        updated_package = self.client.edit_package(package.id, i_do_not_exist='sabotage')
        self.assertTrue('i_do_not_exist' not in updated_package.__dict__)

    def test_edit_package_should_unset_field_when_passed_none(self):
        package = self.create(
            intended_purpose="Intended purpose",
            documentation="Documentation",
            internal_usage_rights="Yes",
            internal_usage_notes="internal usage notes",
            distribution_rights="Yes",
            distribution_notes="distribution notes",
            derived_data_rights="Yes",
            derived_data_notes="derived data notes"
        )
        self.assertTrue('intended_purpose' in package.__dict__)
        self.assertTrue('internal_usage_rights' in package.__dict__)
        self.assertTrue('internal_usage_notes' in package.__dict__)
        self.assertTrue('distribution_rights' in package.__dict__)
        self.assertTrue('distribution_notes' in package.__dict__)
        self.assertTrue('derived_data_rights' in package.__dict__)
        self.assertTrue('derived_data_notes' in package.__dict__)

        updated_package = self.client.edit_package(
            package.id,
            intended_purpose=None,
            documentation=None,
            internal_usage_rights=None,
            internal_usage_notes=None,
            distribution_rights=None,
            distribution_notes=None,
            derived_data_rights=None,
            derived_data_notes=None
        )
        self.assertTrue('intended_purpose' not in updated_package.__dict__)
        self.assertTrue('internal_usage_rights' not in updated_package.__dict__)
        self.assertTrue('internal_usage_notes' not in updated_package.__dict__)
        self.assertTrue('distribution_rights' not in updated_package.__dict__)
        self.assertTrue('distribution_notes' not in updated_package.__dict__)
        self.assertTrue('derived_data_rights' not in updated_package.__dict__)
        self.assertTrue('derived_data_notes' not in updated_package.__dict__)

    def test_edit_package_should_stay_the_same_when_terms_and_conditions_are_not_provided(self):
        package = self.create(
            intended_purpose="Intended purpose",
            documentation="Documentation",
            internal_usage_rights="Yes",
            internal_usage_notes="internal usage notes",
            distribution_rights="Yes",
            distribution_notes="distribution notes",
            derived_data_rights="Yes",
            derived_data_notes="derived data notes",
            terms_and_conditions="Terms"
        )
        assert package.terms_and_conditions == "Terms"

        updated_package = self.client.edit_package(
            package.id,
            derived_data_notes=None
        )
        assert updated_package.terms_and_conditions == "Terms"

    def test_edit_package_should_raise_value_error_when_terms_and_conditions_are_set_to_none(self):
        package = self.create(
            intended_purpose="Intended purpose",
            documentation="Documentation",
            internal_usage_rights="Yes",
            internal_usage_notes="internal usage notes",
            distribution_rights="Yes",
            distribution_notes="distribution notes",
            derived_data_rights="Yes",
            derived_data_notes="derived data notes",
            terms_and_conditions="Terms"
        )
        assert package.terms_and_conditions == "Terms"

        with self.assertRaises(ValueError):
            self.client.edit_package(
                package.id,
                terms_and_conditions=None
            )

    def test_edit_package_should_raise_value_error_when_terms_and_conditions_are_empty_string(self):
        package = self.create(
            intended_purpose="Intended purpose",
            documentation="Documentation",
            internal_usage_rights="Yes",
            internal_usage_notes="internal usage notes",
            distribution_rights="Yes",
            distribution_notes="distribution notes",
            derived_data_rights="Yes",
            derived_data_notes="derived data notes",
            terms_and_conditions="Terms"
        )
        assert package.terms_and_conditions == "Terms"

        with self.assertRaises(ValueError):
            self.client.edit_package(
                package.id,
                terms_and_conditions=""
            )

    def test_edit_package_should_raise_value_error_when_terms_and_conditions_are_blank_string(self):
        package = self.create(
            intended_purpose="Intended purpose",
            documentation="Documentation",
            internal_usage_rights="Yes",
            internal_usage_notes="internal usage notes",
            distribution_rights="Yes",
            distribution_notes="distribution notes",
            derived_data_rights="Yes",
            derived_data_notes="derived data notes",
            terms_and_conditions="Terms"
        )
        assert package.terms_and_conditions == "Terms"

        with self.assertRaises(ValueError):
            self.client.edit_package(
                package.id,
                terms_and_conditions="   "
            )

    def test_edit_package_should_update_terms_and_conditions_field_when_passed_new_value(self):
        package = self.create(
            intended_purpose="Intended purpose",
            documentation="Documentation",
            internal_usage_rights="Yes",
            internal_usage_notes="internal usage notes",
            distribution_rights="Yes",
            distribution_notes="distribution notes",
            derived_data_rights="Yes",
            derived_data_notes="derived data notes",
            terms_and_conditions="Terms"
        )
        assert package.terms_and_conditions == "Terms"

        updated_package = self.client.edit_package(
            package.id,
            terms_and_conditions="Updated terms",
        )
        assert updated_package.terms_and_conditions == "Updated terms"

    def test_edit_package_allows_changing_single_field(self):
        package = self.create(intended_purpose="Testing")
        self.assertEqual(package.intended_purpose, "Testing")

        edited = self.client.edit_package(
            package.id, description="enhanced description"
        )
        self.assertEqual(edited.package_id, package.id)
        self.assertEqual(edited.description, "enhanced description")

        # accounts were not changed
        self.assertEqual(edited.manager_id, package.manager_id)
        self.assertEqual(edited.tech_data_ops_id, package.tech_data_ops_id)
        self.assertEqual(edited.publisher, package.publisher)
        self.assertEqual(edited.access_manager_id, package.access_manager_id)

        # name is still the same
        self.assertEqual(edited.name, package.name)

        self.assertEqual(edited.intended_purpose, package.intended_purpose)

    def test_edit_can_change_account_ids(self):
        package = self.create()
        assert package.tech_data_ops_id == "datalake-mgmt"

        edited = self.client.edit_package(
            package.id,
            tech_data_ops_id="iboxx"
        )

        self.assertEqual(edited.package_id, package.id)
        self.assertEqual(edited.tech_data_ops_id, "iboxx")

    def test_edit_package_should_unset_documentation_field_when_passed_none(
        self
    ):
        """
        The package.documentation is a special case as it is referenced inside
        the package_model code, so the attribute is declared in the
        constructor so is always present even when not on the
        Catalogue's response JSON.
        :return:
        """
        package = self.create()
        assert package.documentation is None

        # Edit to add value.
        updated_package = self.client.edit_package(
            package.id,
            documentation='some-documentation',
        )
        assert updated_package.documentation == 'some-documentation'
        # Assert that some other known fields are not present.
        self.assertTrue('intended_purpose' not in updated_package.__dict__)
        self.assertTrue('internal_usage_rights' not in updated_package.__dict__)

        # Edit again to remove value.
        updated_package = self.client.edit_package(
            package.id,
            documentation=None,
        )
        assert updated_package.documentation is None
        # Assert that some other known fields are not present.
        self.assertTrue('intended_purpose' not in updated_package.__dict__)
        self.assertTrue('internal_usage_rights' not in updated_package.__dict__)

@pytest.mark.integration
class RegisterPackageTestCase(SdkIntegrationTestCase):

    def setUp(self):
        super().setUp()

    def test_create_package_with_none_terms_and_conditions_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.client.register_package(
                name="EditPackageTestCase" + str(uuid.uuid4()),
                description="my package description",
                topic="Automotive",
                access="Restricted",
                internal_data="Yes",
                data_sensitivity="Public",
                terms_and_conditions=None,
                publisher="Bloomberg",
                access_manager_id="datalake-mgmt",
                tech_data_ops_id="datalake-mgmt",
                manager_id="datalake-mgmt")

    def test_create_package_with_empty_terms_and_conditions_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.client.register_package(
                name="EditPackageTestCase" + str(uuid.uuid4()),
                description="my package description",
                topic="Automotive",
                access="Restricted",
                internal_data="Yes",
                data_sensitivity="Public",
                terms_and_conditions="",
                publisher="Bloomberg",
                access_manager_id="datalake-mgmt",
                tech_data_ops_id="datalake-mgmt",
                manager_id="datalake-mgmt")

    def test_create_package_with_blank_terms_and_conditions_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.client.register_package(
                name="EditPackageTestCase" + str(uuid.uuid4()),
                description="my package description",
                topic="Automotive",
                access="Restricted",
                internal_data="Yes",
                data_sensitivity="Public",
                terms_and_conditions="      ",
                publisher="Bloomberg",
                access_manager_id="datalake-mgmt",
                tech_data_ops_id="datalake-mgmt",
                manager_id="datalake-mgmt")

    def test_create_package_with_non_empty_terms_and_conditions_creates_package_with_provided_value(self):
        package = self.client.register_package(
            name="EditPackageTestCase" + str(uuid.uuid4()),
            description="my package description",
            topic="Automotive",
            access="Restricted",
            internal_data="Yes",
            data_sensitivity="Public",
            terms_and_conditions="Terms and conditions",
            publisher="Bloomberg",
            access_manager_id="datalake-mgmt",
            tech_data_ops_id="datalake-mgmt",
            manager_id="datalake-mgmt")

        assert package.terms_and_conditions is not None
        assert package.terms_and_conditions == "Terms and conditions"


@pytest.mark.integration
class GetDefaultTermsAndConditionsTestCase(SdkIntegrationTestCase):
    _DEFAULT_TERMS_AND_CONDITIONS = ('By submitting this Data request and checking the "Accept Terms and Conditions" '
                                     'box, you acknowledge and agree to the following:\n'
                                     '\n'
                                     '* To promptly notify the relevant Access Manager/Producer of your intended use '
                                     'of the Data;\n'
                                     '* To obtain the terms and conditions relevant to such use for such Data from '
                                     'the Producer;\n'
                                     '* To distribute such terms and conditions to each member of your '
                                     'Consumer Group who may use the Data;\n'
                                     '* To use the Data solely for such intended use, subject to such terms and '
                                     'conditions;\n'
                                     '* To ensure that the Data is only accessed by members of your Consumer Group, '
                                     'and only used by such members for such intended use, subject to such terms and '
                                     'conditions;\n'
                                     '* To adhere to any additional requests of Producer with respect to the Data '
                                     '(including but not limited to ceasing use of the Data and deleting the Data, '
                                     'and ensuring other members of the Consumer Group do so, upon revocation of your '
                                     'license by Producer).\n'
                                     '\n'
                                     'Please refer to the <a href="/terms-of-use" target="_blank">EULA</a> for any '
                                     'defined terms used above. '
                                     'The <a href="/terms-of-use" target="_blank">EULA</a> '
                                     'is the document you agreed to adhere to by accessing the Lake.')

    def test_get_default_terms_and_conditions_returns_proper_text(self):
        from dli.client.components.package import Package

        result = Package.get_default_package_terms_and_conditions(
            organisation_name='some_organisation_name')
        assert result == ''

        default_text = Package.get_default_package_terms_and_conditions(
            organisation_name='IHS Markit')
        assert default_text == self._DEFAULT_TERMS_AND_CONDITIONS
