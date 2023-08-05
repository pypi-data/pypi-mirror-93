# coding: utf-8

"""
    Pulp 3 API

    Fetch, Upload, Organize, and Distribute Software Packages  # noqa: E501

    The version of the OpenAPI document: v3
    Contact: pulp-list@redhat.com
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import pulpcore.client.pulp_ansible
from pulpcore.client.pulp_ansible.models.paginatedansible_ansible_repository_response_list import PaginatedansibleAnsibleRepositoryResponseList  # noqa: E501
from pulpcore.client.pulp_ansible.rest import ApiException

class TestPaginatedansibleAnsibleRepositoryResponseList(unittest.TestCase):
    """PaginatedansibleAnsibleRepositoryResponseList unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test PaginatedansibleAnsibleRepositoryResponseList
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = pulpcore.client.pulp_ansible.models.paginatedansible_ansible_repository_response_list.PaginatedansibleAnsibleRepositoryResponseList()  # noqa: E501
        if include_optional :
            return PaginatedansibleAnsibleRepositoryResponseList(
                count = 123, 
                next = 'http://api.example.org/accounts/?offset=400&limit=100', 
                previous = 'http://api.example.org/accounts/?offset=200&limit=100', 
                results = [
                    pulpcore.client.pulp_ansible.models.ansible/ansible_repository_response.ansible.AnsibleRepositoryResponse(
                        pulp_href = '0', 
                        pulp_created = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        versions_href = '0', 
                        pulp_labels = pulpcore.client.pulp_ansible.models.pulp_labels.pulp_labels(), 
                        latest_version_href = '0', 
                        name = '0', 
                        description = '0', 
                        remote = '0', )
                    ]
            )
        else :
            return PaginatedansibleAnsibleRepositoryResponseList(
        )

    def testPaginatedansibleAnsibleRepositoryResponseList(self):
        """Test PaginatedansibleAnsibleRepositoryResponseList"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
