#
# Copyright (C) 2020 IHS Markit.
# All Rights Reserved
#
import logging
import warnings

import requests

from dli.client.components.urls import package_urls
from dli.client.components import SirenComponent, SirenAdapterResponse
from dli.client.exceptions import CatalogueEntityNotFoundException
from dli.client.utils import filter_out_unknown_keys, to_camel_cased_dict

logger = logging.getLogger(__name__)

class Package(SirenComponent):

    __USE_V2_ROUTE = False

    _KNOWN_FIELDS = {"name",
                     "description",
                     "keywords",
                     "topic",
                     "access",
                     "internalData",
                     "dataSensitivity",
                     "contractIds",
                     "termsAndConditions",
                     "derivedDataNotes",
                     "derivedDataRights",
                     "distributionNotes",
                     "distributionRights",
                     "internalUsageNotes",
                     "internalUsageRights",
                     "documentation",
                     "publisher",
                     "techDataOpsId",
                     "accessManagerId",
                     "managerId",
                     "intendedPurpose",
                     "isInternalWithinOrganisation"}
    """
    A mixin providing common package operations
    """

    def get_package(self, id=None, name=None):
        """
        Fetches package metadata for an existing package.

        :param str id: The id of the package.
        :param str name: The name of the package. We will perform a case
        sensitive exact match on this name in the database. If you want
        a non-exact match or a case insensitive match, then please consider
        using the `packages` call instead with the `search_term` parameter
        and an `ilike` matcher, for example:

        .. code:: python

            client.packages(search_term='name ilike example')

        :returns: A package instance
        :rtype: collections.namedtuple

        - **Sample**

        .. code-block:: python

                # Look up by package id
                package = client.get_package('my_package_id')
                # or
                package = client.get_package(id='my_package_id')

                # Alternatively look up by package name
                package = client.get_package(name='my_package')

        """

        if id is None and name is None:
            raise ValueError("Either package id or name must be specified to look up package")

        return self._get_package(package_id=id, name=name)

    def get_package_datasets(self, package_id, count=100):
        """
        Returns a list of all datasets registered under a package.

        :param str package_id: The id of the package.
        :param int count: Optional. Count of datasets to be returned. Defaults to 100.

        :returns: List of all datasets registered under the package.
        :rtype: list[collections.namedtuple]

        - **Sample**

        .. code-block:: python

                datasets = client.get_package_datasets(
                    package_id,
                    count=100
                )
        """
        response = self.session.get(
            package_urls.v2_package_datasets.format(id=package_id),
            params={'page_size': count}
        )

        return self._DatasetFactory._from_v2_list_response(response.json())


    def register_package(
        self,
        name,
        description,
        topic,
        access,
        internal_data,
        data_sensitivity,
        terms_and_conditions,
        publisher,
        access_manager_id,
        tech_data_ops_id,
        manager_id,
        keywords=None,
        contract_ids=None,
        derived_data_notes=None,
        derived_data_rights=None,
        distribution_notes=None,
        distribution_rights=None,
        internal_usage_notes=None,
        internal_usage_rights=None,
        documentation=None,
        intended_purpose=None,
        is_internal_within_organisation=None,
    ):
        """
        .. deprecated:: 1.11.0
            Deprecation Warning: retrieving a package (and other CRUD package operations) using SDK get_package will be deprecated in near future (by 2020-09-08). The API should be used instead, full details on how to use API can be found by signing in to 'https://catalogue-uat.datalake.ihsmarkit.com' then opening the page 'https://catalogue-uat.datalake.ihsmarkit.com/__api/v2/swagger?urls.primaryName=packages'.

        Submit a request to create a new package in the Data Catalogue.

        Packages are parent structures that contain metadata relating
        to a group of Datasets.

        See description for each parameter, and whether they are optional or mandatory.

        :param str name: A descriptive name of a package. It should be unique across the Data Catalogue.
        :param str description: A short description of a package.
        :param str topic: Topic the data in the package is about. Not applicable, if the package is not industry specific.
        :param str access: Accepted values are: `Restricted` or `Unrestricted`.
                            If access to the package is flagged as `Restricted`,
                            access manager_id will have to grant or deny access to the underlying data.
                            If access is flagged as `Unrestricted`, user will be able to gain
                            access instantaneously after submitting the access request form.
        :param str internal_data: DEPRECATED - Note this is not used on V2 Accepted values are: `Yes`, `No` or `Both`. Package is marked as `Yes` if underlying data is created internally at IHS Markit, or No if externally, e.g. S&P, Russell, etc.
        :param str data_sensitivity: Accepted values are: `Private`, `Public` or `Top Secret`. Sensitivity level of the data contained within the package
        :param str terms_and_conditions: Terms and conditions for the package.
            Default T&C for IHSM organisations only can be obtained through
            `get_default_package_terms_and_conditions` function. None, empty
            or blank string will result in ValueError.
        :param str publisher: Business unit or legal entity responsible for the content.
                              For example, S&P, Dow Jones, IHS Markit.
        :param str access_manager_id: Account ID for the Data Lake Account
                                      that is responsible for managing access to the packages on Data Catalogue.
        :param str tech_data_ops_id: Account ID for the Data Lake Account that is responsible for uploading the data to Data Lake.
        :param str manager_id: Account ID for the Data Lake Account that is responsible for creating and maintaining metadata for packages and datasets on Data Catalogue.
        :param list[str] keywords: Optional. List of keywords that can be used to find this
                         package through the search interface.

        :param list[str] contract_ids: Optional. Internally, this will be the Salesforce contract ID and/or CARM ID. Externally, this could be any ID.
        :param str derived_data_notes: Optional. Provides details, comments on derived data.
                                   Extension to the Derived Data Rights field.
        :param str derived_data_rights: Optional. Accepted values are `Yes`, `No`, `With Limitations`, `N/A`.
                                    A flag to indicate whether we have rights to derived data.
        :param str distribution_notes: Optional. Provides details, comments on data distribution rights.
                                   Extension to the Distribution Rights field.
        :param str distribution_rights: Optional. Accepted values are `Yes`, `No`, `With Limitations`, `N/A`.
                                    A flag to indicate whether data can be distributed.
        :param str internal_usage_notes: Optional. Provides details, comments on internal data usage.
                                     Extension to Internal Usage Rights.
        :param str internal_usage_rights: Optional. Accepted values are: `Yes`, `No`, `With Limitations`, `N/A`.
                                      A flag to indicate whether data can be used internally.
        :param str documentation: Optional. Documentation about this package in markdown format.
        :param str intended_purpose: Optional. Provides details about intended usage of the data contained
                                     in the package, e.g. permanent storage, temporary storage, POC.
        :param bool is_internal_within_organisation: Optional. Default True. Defines whether the package can be viewed by external organisations or not. Default setting resolves to package being invisible to external organisations.
        :returns: Created package
        :rtype: collections.namedtuple

        - **Sample**

        .. code-block:: python

                package = client.register_package(
                    name="my package",
                    description="my package description",
                    topic="Automotive",
                    access="Restricted",
                    internal_data="Yes",
                    data_sensitivity="Public",
                    terms_and_conditions="Terms",
                    publisher="my publisher",
                    access_manager_id="123",
                    tech_data_ops_id="1234",
                    manager_id="334"
                )
        """
        warnings.warn(
            "Deprecation Warning: registering a package (and other CRUD package operations) using SDK "
            "register_package will be deprecated in near future (by November 2020). The API should be used "
            "instead, find details on how to use API can be found by signing in to 'https://catalogue-uat.datalake.ihsmarkit.com' then opening the page 'https://catalogue-uat.datalake.ihsmarkit.com/__api/v2/swagger?urls.primaryName=packages'.",
            PendingDeprecationWarning
        )

        self._validate_terms_and_conditions(terms_and_conditions)

        if Package.__USE_V2_ROUTE:
            payload = {
                "name": name,
                "description": description,
                "keywords": keywords,
                "topic": topic,
                "access": access,
                "data_sensitivity": data_sensitivity,
                "contract_ids": contract_ids,
                "terms_and_conditions": terms_and_conditions,
                "derived_data_notes": derived_data_notes,
                "derived_data_rights": derived_data_rights,
                "distribution_notes": distribution_notes,
                "distribution_rights": distribution_rights,
                "internal_usage_notes": internal_usage_notes,
                "internal_usage_rights": internal_usage_rights,
                "documentation": documentation,
                "publisher": publisher,
                "tech_data_ops_id": tech_data_ops_id,
                "access_manager_id": access_manager_id,
                "manager_id": manager_id,
                "intended_purpose": intended_purpose,
                "is_internal_within_organisation": is_internal_within_organisation,
            }

            payload = {
                "data": {
                    "attributes": {
                        k: v for k, v in payload.items() if v is not None
                    }
                }
            }

            json = self.session.post(
                package_urls.v2_package_index, json=payload
            ).json()

            return self._Package(json)
        else:
            payload = {
                "name": name,
                "description": description,
                "keywords": keywords,
                "topic": topic,
                "access": access,
                "internalData": internal_data,
                "dataSensitivity": data_sensitivity,
                "contractIds": contract_ids,
                "termsAndConditions": terms_and_conditions,
                "derivedDataNotes": derived_data_notes,
                "derivedDataRights": derived_data_rights,
                "distributionNotes": distribution_notes,
                "distributionRights": distribution_rights,
                "internalUsageNotes": internal_usage_notes,
                "internalUsageRights": internal_usage_rights,
                "documentation": documentation,
                "publisher": publisher,
                "techDataOpsId": tech_data_ops_id,
                "accessManagerId": access_manager_id,
                "managerId": manager_id,
                "intendedPurpose": intended_purpose,
                "isInternalWithinOrganisation": is_internal_within_organisation,
            }

            payload = {k: v for k, v in payload.items() if v is not None}

            if payload["internalData"] is None:
                payload["internalData"] = 'No'

            json = self.session.post(
                package_urls.package_index, json=payload
            ).json()

            return self._Package._from_v1_response_to_v2(json)

    def edit_package(
        self,
        package_id,
        **kwargs
    ):
        """
        .. deprecated:: 1.11.0
           Deprecation Warning: retrieving a package (and other CRUD package operations) using SDK get_package will be deprecated in near future (by 2020-09-08). The API should be used instead, full details on how to use API can be found by signing in to 'https://catalogue-uat.datalake.ihsmarkit.com' then opening the page 'https://catalogue-uat.datalake.ihsmarkit.com/__api/v2/swagger?urls.primaryName=packages'.

        Updates one or more fields in a package.
        If keyword argument is not specified field keeps its old value.
        Optional enum and text type fields can be unset by passing ``None``.

        :param str package_id: Package ID of the package being edited.

        Keyword arguments:

        :keyword str name: Optional. A descriptive name of a package. It should be unique across the Data Catalogue.
        :keyword str description: Optional. A short description of a package.
        :keyword str topic: Optional. Topic the data in the package is about. Not applicable, if the package is not industry specific.
        :keyword str access: Optional. Accepted values are: `Restricted` or `Unrestricted`.
                            If access to the package is flagged as `Restricted`,
                            access manager will have to grant or deny access to the underlying data.
                            If access is flagged as `Unrestricted`, user will be able to gain
                            access instantaneously after submitting the access request form.
        :keyword str internal_data: Accepted values are: `Yes`, `No` or `Both`. Package is marked as Yes if underlying data is created internally at IHS Markit, or No if externally, e.g. S&P, Russell, etc.
        :keyword str data_sensitivity: Optional. Accepted values are: `Private`, `Public` or `Top Secret`. Sensitivity level of the data contained within the package
        :keyword str terms_and_conditions: Terms and conditions for the package.
            Default T&C for IHSM organisations only can be obtained through
            `get_default_package_terms_and_conditions` function. None, empty
            or blank string will result in ValueError.
        :keyword str publisher: Optional. Business unit or legal entity responsible for the content.
                            For example, S&P, Dow Jones, IHS Markit.
        :keyword list[str] keywords: Optional. List of keywords that can be used to find this
                            package through the search interface.
        :keyword str access_manager_id: Optional. Account ID for the Data Lake Account that is responsible for managing access to the packages on Data Catalogue.
        :keyword str tech_data_ops_id: Optional. Account ID for the Data Lake Account that is responsible for uploading the data to Data Lake.
        :keyword str manager_id: Optional. Account ID for the Data Lake Account that is responsible for creating and maintaining metadata for packages and datasets on Data Catalogue.
        :keyword list[str] contract_ids: Optional. Internally, this will be the Salesforce contract ID and/or CARM ID. Externally, this could be any ID.
        :keyword str derived_data_notes: Optional. Provides details, comments on derived data.
                                   Extension to the Derived Data Rights field.
        :keyword str derived_data_rights: Optional. Accepted values are `Yes`, `No`, `With Limitations`, `N/A`. A flag to indicate whether we have rights to derived data.
        :keyword str distribution_notes: Optional. Provides details, comments on data distribution rights.
                                   Extension to the Distribution Rights field.
        :keyword str distribution_rights: Optional. Accepted values are `Yes`, `No`, `With Limitations`, `N/A`.
                                    A flag to indicate whether data can be distributed.
        :keyword str internal_usage_notes: Optional. Provides details, comments on internal data usage.
                                     Extension to Internal Usage Rights.
        :keyword str internal_usage_rights: Optional. Accepted values are: `Yes`, `No`, `With Limitations`, `N/A`.
                                      A flag to indicate whether data can be used internally.
        :keyword str documentation: Optional. Documentation about this package in markdown format.
        :keyword str intended_purpose: Optional. Provides details about intended usage of the data contained
                                     in the package, e.g. permanent storage, temporary storage, POC.
        :keyword bool is_internal_within_organisation: Optional. Defines whether the package can be viewed by external organisations or not. Default setting resolves to package being invisible to external organisations.

        :returns: The updated Package.
        :rtype: collections.namedtuple

        - **Sample**

        .. code-block:: python

                package = client.edit_package(
                    package_id="my-package-id",
                    description="Updated my package description",
                )
        """
        warnings.warn(
            "Deprecation Warning: editing a package (and other CRUD package operations) using SDK "
            "edit_package will be deprecated in near future (by November 2020). The API should be used "
            "instead, find details on how to use API can be found by signing in to 'https://catalogue-uat.datalake.ihsmarkit.com' then opening the page 'https://catalogue-uat.datalake.ihsmarkit.com/__api/v2/swagger?urls.primaryName=packages'.",
            PendingDeprecationWarning
        )
        fields = filter_out_unknown_keys(to_camel_cased_dict(kwargs),
                                         Package._KNOWN_FIELDS)
        self._validate_fields(fields)

        # v2 package comes snake_case, so we must do some tom-jiggery
        # back to camelCase from the model
        package = self._get_package(package_id=package_id)
        package_as_dict = to_camel_cased_dict(package.__dict__)

        # clean the package dict with fields that aren't known to us.
        # This is needed to make us less brittle to changes such as DL-4933
        # where the Catalogue team are returning new fields on the GET
        # endpoint that are read-only and such `organisation_short_code` which
        # will fail validation if passed to the PUT endpoint.
        for key in list(package_as_dict.keys()):
            if key not in Package._KNOWN_FIELDS:
                del package_as_dict[key]

        package_as_dict.update(fields)
        #v2 also misses 'internalData'
        package_as_dict.update({'internalData': 'No'})

        json = self.session.put(
            package_urls.package_edit.format(id=package_id), json=package_as_dict
        ).json()

        return self._Package._from_v1_response_to_v2(json)

    def delete_package(self, package_id):
        """
        .. deprecated:: 1.11.0
           Deprecation Warning: retrieving a package (and other CRUD package operations) using SDK get_package will be deprecated in near future (by 2020-09-08). The API should be used instead, full details on how to use API can be found by signing in to 'https://catalogue-uat.datalake.ihsmarkit.com' then opening the page 'https://catalogue-uat.datalake.ihsmarkit.com/__api/v2/swagger?urls.primaryName=packages'.

        Performs deletion of an existing package. This will delete all underlying datasets for the package as well.

        :param str package_id: The id of the package to be deleted.

        :returns: None

        - **Sample**

        .. code-block:: python

                client.delete_package(package_id)

        """
        warnings.warn(
            "Deprecation Warning: deleting a package (and other CRUD package operations) using SDK "
            "delete_package will be deprecated in near future (by November 2020). The API should be used "
            "instead, find details on how to use API can be found by signing in to 'https://catalogue-uat.datalake.ihsmarkit.com' then opening the page 'https://catalogue-uat.datalake.ihsmarkit.com/__api/v2/swagger?urls.primaryName=packages'.",
            PendingDeprecationWarning
        )
        self.session.delete(
            package_urls.package_edit.format(id=package_id)
        )

    @staticmethod
    def get_default_package_terms_and_conditions(organisation_name: str):
        """
        Returns a string representing the default Terms And Conditions for packages created in DataLake.

        :returns: The default DataLake Terms And Conditions
        :rtype: str
        """
        if organisation_name == 'IHS Markit':
            return ('By submitting this Data request and checking the "Accept Terms and Conditions" '
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
        else:
            return ''

    #
    # Private functions
    #
    def _get_package(self, **kwargs):
        vals = []

        if 'package_id' in kwargs:
            vals = self.packages(
                search_term=[f"id={kwargs['package_id']}"]).values()

        elif 'name' in kwargs:
            vals = self.packages(
                search_term=[f"name={kwargs['name']}"]).values()

        vals = list(vals)

        if len(vals) == 1:
            if hasattr(vals[0], "id"):
                vals[0].package_id = vals[0].id

            return vals[0]
        elif len(vals) < 1:
            r = requests.Response()
            r.status_code = 404
            r.request = (lambda: True)
            r.request.method = f"Package {kwargs['package_id'] if kwargs.get('package_id') else kwargs['name']}"
            r.request.url = ""
            raise CatalogueEntityNotFoundException(
                message=f"Package "
                f"{kwargs['package_id'] if kwargs.get('package_id') else kwargs['name']}",
                response=r
            )
        else:
            return vals

    @staticmethod
    def _validate_fields(fields):
        if 'termsAndConditions' in fields:
            Package._validate_terms_and_conditions(fields.get("termsAndConditions"))

    @staticmethod
    def _validate_terms_and_conditions(field):
        if not field or not field.strip():
            raise ValueError("Terms and conditions must be defined "
                             "and be non empty, non blank string")
