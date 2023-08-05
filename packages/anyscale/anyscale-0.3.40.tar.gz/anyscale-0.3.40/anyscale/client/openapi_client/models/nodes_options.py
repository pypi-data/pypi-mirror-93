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


class NodesOptions(object):
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
        'provider_config': 'object',
        'cluster_name': 'str',
        'instance_ids': 'list[str]'
    }

    attribute_map = {
        'provider_config': 'provider_config',
        'cluster_name': 'cluster_name',
        'instance_ids': 'instance_ids'
    }

    def __init__(self, provider_config=None, cluster_name=None, instance_ids=None, local_vars_configuration=None):  # noqa: E501
        """NodesOptions - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._provider_config = None
        self._cluster_name = None
        self._instance_ids = None
        self.discriminator = None

        self.provider_config = provider_config
        self.cluster_name = cluster_name
        self.instance_ids = instance_ids

    @property
    def provider_config(self):
        """Gets the provider_config of this NodesOptions.  # noqa: E501


        :return: The provider_config of this NodesOptions.  # noqa: E501
        :rtype: object
        """
        return self._provider_config

    @provider_config.setter
    def provider_config(self, provider_config):
        """Sets the provider_config of this NodesOptions.


        :param provider_config: The provider_config of this NodesOptions.  # noqa: E501
        :type: object
        """
        if self.local_vars_configuration.client_side_validation and provider_config is None:  # noqa: E501
            raise ValueError("Invalid value for `provider_config`, must not be `None`")  # noqa: E501

        self._provider_config = provider_config

    @property
    def cluster_name(self):
        """Gets the cluster_name of this NodesOptions.  # noqa: E501


        :return: The cluster_name of this NodesOptions.  # noqa: E501
        :rtype: str
        """
        return self._cluster_name

    @cluster_name.setter
    def cluster_name(self, cluster_name):
        """Sets the cluster_name of this NodesOptions.


        :param cluster_name: The cluster_name of this NodesOptions.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and cluster_name is None:  # noqa: E501
            raise ValueError("Invalid value for `cluster_name`, must not be `None`")  # noqa: E501

        self._cluster_name = cluster_name

    @property
    def instance_ids(self):
        """Gets the instance_ids of this NodesOptions.  # noqa: E501


        :return: The instance_ids of this NodesOptions.  # noqa: E501
        :rtype: list[str]
        """
        return self._instance_ids

    @instance_ids.setter
    def instance_ids(self, instance_ids):
        """Sets the instance_ids of this NodesOptions.


        :param instance_ids: The instance_ids of this NodesOptions.  # noqa: E501
        :type: list[str]
        """
        if self.local_vars_configuration.client_side_validation and instance_ids is None:  # noqa: E501
            raise ValueError("Invalid value for `instance_ids`, must not be `None`")  # noqa: E501

        self._instance_ids = instance_ids

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
        if not isinstance(other, NodesOptions):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, NodesOptions):
            return True

        return self.to_dict() != other.to_dict()
