#!/usr/bin/python
#
# Copyright 2018-2021 Polyaxon, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# coding: utf-8

"""
    Polyaxon SDKs and REST API specification.

    Polyaxon SDKs and REST API specification.  # noqa: E501

    The version of the OpenAPI document: 1.5.4
    Contact: contact@polyaxon.com
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from polyaxon_sdk.configuration import Configuration


class V1RunSettings(object):
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
        'namespace': 'str',
        'agent': 'V1RunSettingsCatalog',
        'queue': 'V1RunSettingsCatalog',
        'artifacts_store': 'V1RunSettingsCatalog',
        'hub': 'V1RunReferenceCatalog',
        'registry': 'V1RunReferenceCatalog'
    }

    attribute_map = {
        'namespace': 'namespace',
        'agent': 'agent',
        'queue': 'queue',
        'artifacts_store': 'artifacts_store',
        'hub': 'hub',
        'registry': 'registry'
    }

    def __init__(self, namespace=None, agent=None, queue=None, artifacts_store=None, hub=None, registry=None, local_vars_configuration=None):  # noqa: E501
        """V1RunSettings - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._namespace = None
        self._agent = None
        self._queue = None
        self._artifacts_store = None
        self._hub = None
        self._registry = None
        self.discriminator = None

        if namespace is not None:
            self.namespace = namespace
        if agent is not None:
            self.agent = agent
        if queue is not None:
            self.queue = queue
        if artifacts_store is not None:
            self.artifacts_store = artifacts_store
        if hub is not None:
            self.hub = hub
        if registry is not None:
            self.registry = registry

    @property
    def namespace(self):
        """Gets the namespace of this V1RunSettings.  # noqa: E501


        :return: The namespace of this V1RunSettings.  # noqa: E501
        :rtype: str
        """
        return self._namespace

    @namespace.setter
    def namespace(self, namespace):
        """Sets the namespace of this V1RunSettings.


        :param namespace: The namespace of this V1RunSettings.  # noqa: E501
        :type: str
        """

        self._namespace = namespace

    @property
    def agent(self):
        """Gets the agent of this V1RunSettings.  # noqa: E501


        :return: The agent of this V1RunSettings.  # noqa: E501
        :rtype: V1RunSettingsCatalog
        """
        return self._agent

    @agent.setter
    def agent(self, agent):
        """Sets the agent of this V1RunSettings.


        :param agent: The agent of this V1RunSettings.  # noqa: E501
        :type: V1RunSettingsCatalog
        """

        self._agent = agent

    @property
    def queue(self):
        """Gets the queue of this V1RunSettings.  # noqa: E501


        :return: The queue of this V1RunSettings.  # noqa: E501
        :rtype: V1RunSettingsCatalog
        """
        return self._queue

    @queue.setter
    def queue(self, queue):
        """Sets the queue of this V1RunSettings.


        :param queue: The queue of this V1RunSettings.  # noqa: E501
        :type: V1RunSettingsCatalog
        """

        self._queue = queue

    @property
    def artifacts_store(self):
        """Gets the artifacts_store of this V1RunSettings.  # noqa: E501


        :return: The artifacts_store of this V1RunSettings.  # noqa: E501
        :rtype: V1RunSettingsCatalog
        """
        return self._artifacts_store

    @artifacts_store.setter
    def artifacts_store(self, artifacts_store):
        """Sets the artifacts_store of this V1RunSettings.


        :param artifacts_store: The artifacts_store of this V1RunSettings.  # noqa: E501
        :type: V1RunSettingsCatalog
        """

        self._artifacts_store = artifacts_store

    @property
    def hub(self):
        """Gets the hub of this V1RunSettings.  # noqa: E501


        :return: The hub of this V1RunSettings.  # noqa: E501
        :rtype: V1RunReferenceCatalog
        """
        return self._hub

    @hub.setter
    def hub(self, hub):
        """Sets the hub of this V1RunSettings.


        :param hub: The hub of this V1RunSettings.  # noqa: E501
        :type: V1RunReferenceCatalog
        """

        self._hub = hub

    @property
    def registry(self):
        """Gets the registry of this V1RunSettings.  # noqa: E501


        :return: The registry of this V1RunSettings.  # noqa: E501
        :rtype: V1RunReferenceCatalog
        """
        return self._registry

    @registry.setter
    def registry(self, registry):
        """Sets the registry of this V1RunSettings.


        :param registry: The registry of this V1RunSettings.  # noqa: E501
        :type: V1RunReferenceCatalog
        """

        self._registry = registry

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
        if not isinstance(other, V1RunSettings):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, V1RunSettings):
            return True

        return self.to_dict() != other.to_dict()
