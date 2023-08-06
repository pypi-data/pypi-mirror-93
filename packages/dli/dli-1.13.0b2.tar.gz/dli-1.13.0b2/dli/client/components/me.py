#
# Copyright (C) 2020 IHS Markit.
# All Rights Reserved
#
import warnings

from dli.client.components import SirenComponent, SirenAdapterResponse
from dli.client.utils import ensure_count_is_valid
from dli.client.components.urls import me_urls


class Me(SirenComponent):
    """Functions related to the current logged in user."""

    def _get_my_entities(self, entity, my_entities_func, count):
        ensure_count_is_valid(count)

        result = my_entities_func(page_size=count)
        return result.get_entities(rel=entity)

    def get_my_packages(self, count=100):
        """
        Returns a list of packages where session user account is: a Manager, Tech Data Ops or Access Manager.

        :param int count: The number of items to retrieve, optional. Defaults to 100.

        :returns: List of my packages.
        :rtype: list[collections.namedtuple]

        - **Sample**

        .. code-block:: python

                my_packages = client.get_my_packages()

        """
        ensure_count_is_valid(count)

        response = self.session.get(
            me_urls.my_packages, params={'page_size': count}
        )

        return SirenAdapterResponse(response).to_many_siren('package')

    def get_my_accounts(self):
        """
        Returns a list of all the accounts associated with user session.

        :returns: list of all associated accounts.
        :rtype: list[collections.namedtuple]

        - **Sample**

        .. code-block:: python

                my_accounts = client.get_my_accounts()

        """
        response = self.session.get(me_urls.my_accounts)
        return SirenAdapterResponse(response).to_many_siren('')
