# coding: utf-8

"""
    Anyscale API

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: 0.1.0
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from anyscale_client.configuration import Configuration


class TextQuery(object):
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
        'equals': 'str',
        'contains': 'str'
    }

    attribute_map = {
        'equals': 'equals',
        'contains': 'contains'
    }

    def __init__(self, equals=None, contains=None, local_vars_configuration=None):  # noqa: E501
        """TextQuery - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._equals = None
        self._contains = None
        self.discriminator = None

        if equals is not None:
            self.equals = equals
        if contains is not None:
            self.contains = contains

    @property
    def equals(self):
        """Gets the equals of this TextQuery.  # noqa: E501

        Property is an exact match of this value.  # noqa: E501

        :return: The equals of this TextQuery.  # noqa: E501
        :rtype: str
        """
        return self._equals

    @equals.setter
    def equals(self, equals):
        """Sets the equals of this TextQuery.

        Property is an exact match of this value.  # noqa: E501

        :param equals: The equals of this TextQuery.  # noqa: E501
        :type: str
        """

        self._equals = equals

    @property
    def contains(self):
        """Gets the contains of this TextQuery.  # noqa: E501

        Property contains this value.  # noqa: E501

        :return: The contains of this TextQuery.  # noqa: E501
        :rtype: str
        """
        return self._contains

    @contains.setter
    def contains(self, contains):
        """Sets the contains of this TextQuery.

        Property contains this value.  # noqa: E501

        :param contains: The contains of this TextQuery.  # noqa: E501
        :type: str
        """

        self._contains = contains

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
        if not isinstance(other, TextQuery):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, TextQuery):
            return True

        return self.to_dict() != other.to_dict()
