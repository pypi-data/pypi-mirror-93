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


class SessionFinishUpOptions(object):
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
        'startup_log': 'str',
        'new_session': 'bool',
        'head_node_ip': 'str',
        'cluster_launch_errored': 'bool'
    }

    attribute_map = {
        'startup_log': 'startup_log',
        'new_session': 'new_session',
        'head_node_ip': 'head_node_ip',
        'cluster_launch_errored': 'cluster_launch_errored'
    }

    def __init__(self, startup_log=None, new_session=None, head_node_ip=None, cluster_launch_errored=None, local_vars_configuration=None):  # noqa: E501
        """SessionFinishUpOptions - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._startup_log = None
        self._new_session = None
        self._head_node_ip = None
        self._cluster_launch_errored = None
        self.discriminator = None

        if startup_log is not None:
            self.startup_log = startup_log
        self.new_session = new_session
        self.head_node_ip = head_node_ip
        self.cluster_launch_errored = cluster_launch_errored

    @property
    def startup_log(self):
        """Gets the startup_log of this SessionFinishUpOptions.  # noqa: E501


        :return: The startup_log of this SessionFinishUpOptions.  # noqa: E501
        :rtype: str
        """
        return self._startup_log

    @startup_log.setter
    def startup_log(self, startup_log):
        """Sets the startup_log of this SessionFinishUpOptions.


        :param startup_log: The startup_log of this SessionFinishUpOptions.  # noqa: E501
        :type: str
        """

        self._startup_log = startup_log

    @property
    def new_session(self):
        """Gets the new_session of this SessionFinishUpOptions.  # noqa: E501


        :return: The new_session of this SessionFinishUpOptions.  # noqa: E501
        :rtype: bool
        """
        return self._new_session

    @new_session.setter
    def new_session(self, new_session):
        """Sets the new_session of this SessionFinishUpOptions.


        :param new_session: The new_session of this SessionFinishUpOptions.  # noqa: E501
        :type: bool
        """
        if self.local_vars_configuration.client_side_validation and new_session is None:  # noqa: E501
            raise ValueError("Invalid value for `new_session`, must not be `None`")  # noqa: E501

        self._new_session = new_session

    @property
    def head_node_ip(self):
        """Gets the head_node_ip of this SessionFinishUpOptions.  # noqa: E501


        :return: The head_node_ip of this SessionFinishUpOptions.  # noqa: E501
        :rtype: str
        """
        return self._head_node_ip

    @head_node_ip.setter
    def head_node_ip(self, head_node_ip):
        """Sets the head_node_ip of this SessionFinishUpOptions.


        :param head_node_ip: The head_node_ip of this SessionFinishUpOptions.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and head_node_ip is None:  # noqa: E501
            raise ValueError("Invalid value for `head_node_ip`, must not be `None`")  # noqa: E501

        self._head_node_ip = head_node_ip

    @property
    def cluster_launch_errored(self):
        """Gets the cluster_launch_errored of this SessionFinishUpOptions.  # noqa: E501


        :return: The cluster_launch_errored of this SessionFinishUpOptions.  # noqa: E501
        :rtype: bool
        """
        return self._cluster_launch_errored

    @cluster_launch_errored.setter
    def cluster_launch_errored(self, cluster_launch_errored):
        """Sets the cluster_launch_errored of this SessionFinishUpOptions.


        :param cluster_launch_errored: The cluster_launch_errored of this SessionFinishUpOptions.  # noqa: E501
        :type: bool
        """
        if self.local_vars_configuration.client_side_validation and cluster_launch_errored is None:  # noqa: E501
            raise ValueError("Invalid value for `cluster_launch_errored`, must not be `None`")  # noqa: E501

        self._cluster_launch_errored = cluster_launch_errored

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
        if not isinstance(other, SessionFinishUpOptions):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, SessionFinishUpOptions):
            return True

        return self.to_dict() != other.to_dict()
