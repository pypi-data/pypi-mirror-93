# coding: utf-8

"""
    Managed Ray API

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: 0.1.0
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from openapi_client.configuration import Configuration


class ComputeTemplateQuery(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'orgwide': 'bool',
        'project_id': 'str'
    }

    attribute_map = {
        'orgwide': 'orgwide',
        'project_id': 'project_id'
    }

    def __init__(self, orgwide=False, project_id=None, local_vars_configuration=None):  # noqa: E501
        """ComputeTemplateQuery - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._orgwide = None
        self._project_id = None
        self.discriminator = None

        if orgwide is not None:
            self.orgwide = orgwide
        if project_id is not None:
            self.project_id = project_id

    @property
    def orgwide(self):
        """Gets the orgwide of this ComputeTemplateQuery.  # noqa: E501


        :return: The orgwide of this ComputeTemplateQuery.  # noqa: E501
        :rtype: bool
        """
        return self._orgwide

    @orgwide.setter
    def orgwide(self, orgwide):
        """Sets the orgwide of this ComputeTemplateQuery.


        :param orgwide: The orgwide of this ComputeTemplateQuery.  # noqa: E501
        :type: bool
        """

        self._orgwide = orgwide

    @property
    def project_id(self):
        """Gets the project_id of this ComputeTemplateQuery.  # noqa: E501


        :return: The project_id of this ComputeTemplateQuery.  # noqa: E501
        :rtype: str
        """
        return self._project_id

    @project_id.setter
    def project_id(self, project_id):
        """Sets the project_id of this ComputeTemplateQuery.


        :param project_id: The project_id of this ComputeTemplateQuery.  # noqa: E501
        :type: str
        """

        self._project_id = project_id

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, ComputeTemplateQuery):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ComputeTemplateQuery):
            return True

        return self.to_dict() != other.to_dict()
