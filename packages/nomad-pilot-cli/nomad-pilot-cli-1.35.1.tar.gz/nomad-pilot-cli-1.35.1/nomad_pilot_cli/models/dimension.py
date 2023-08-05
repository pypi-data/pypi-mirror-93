# coding: utf-8

"""
    Nomad Pilot

    This is the API descriptor for the Nomad Pilot API, responsible for shipping and logistics processing. Developed by [Samarkand Global](https://www.samarkand.global/) in partnership with [SF Express](https://www.sf-express.com/), [eSinotrans](http://air.esinotrans.com/), [sto](http://sto-express.co.uk/). Read the documentation online at [Nomad API Suite](https://api.samarkand.io/). - Install for node with `npm install nomad_pilot_cli` - Install for python with `pip install nomad-pilot-cli` - Install for Maven users `groupId, com.gitlab.samarkand-nomad; artifactId, nomad-pilot-cli`  # noqa: E501

    The version of the OpenAPI document: 1.35.1
    Contact: paul@samarkand.global
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from nomad_pilot_cli.configuration import Configuration


class Dimension(object):
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
        'weight': 'float',
        'height': 'float',
        'length': 'float',
        'width': 'float'
    }

    attribute_map = {
        'weight': 'weight',
        'height': 'height',
        'length': 'length',
        'width': 'width'
    }

    def __init__(self, weight=None, height=None, length=None, width=None, local_vars_configuration=None):  # noqa: E501
        """Dimension - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._weight = None
        self._height = None
        self._length = None
        self._width = None
        self.discriminator = None

        if weight is not None:
            self.weight = weight
        if height is not None:
            self.height = height
        if length is not None:
            self.length = length
        if width is not None:
            self.width = width

    @property
    def weight(self):
        """Gets the weight of this Dimension.  # noqa: E501

        The whole package, not just the products. kilogram.  # noqa: E501

        :return: The weight of this Dimension.  # noqa: E501
        :rtype: float
        """
        return self._weight

    @weight.setter
    def weight(self, weight):
        """Sets the weight of this Dimension.

        The whole package, not just the products. kilogram.  # noqa: E501

        :param weight: The weight of this Dimension.  # noqa: E501
        :type: float
        """

        self._weight = weight

    @property
    def height(self):
        """Gets the height of this Dimension.  # noqa: E501

        the height of current package. centimetre.  # noqa: E501

        :return: The height of this Dimension.  # noqa: E501
        :rtype: float
        """
        return self._height

    @height.setter
    def height(self, height):
        """Sets the height of this Dimension.

        the height of current package. centimetre.  # noqa: E501

        :param height: The height of this Dimension.  # noqa: E501
        :type: float
        """

        self._height = height

    @property
    def length(self):
        """Gets the length of this Dimension.  # noqa: E501

        the length of current package. centimetre.  # noqa: E501

        :return: The length of this Dimension.  # noqa: E501
        :rtype: float
        """
        return self._length

    @length.setter
    def length(self, length):
        """Sets the length of this Dimension.

        the length of current package. centimetre.  # noqa: E501

        :param length: The length of this Dimension.  # noqa: E501
        :type: float
        """

        self._length = length

    @property
    def width(self):
        """Gets the width of this Dimension.  # noqa: E501

        the width of current package. centimetre.  # noqa: E501

        :return: The width of this Dimension.  # noqa: E501
        :rtype: float
        """
        return self._width

    @width.setter
    def width(self, width):
        """Sets the width of this Dimension.

        the width of current package. centimetre.  # noqa: E501

        :param width: The width of this Dimension.  # noqa: E501
        :type: float
        """

        self._width = width

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
        if not isinstance(other, Dimension):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, Dimension):
            return True

        return self.to_dict() != other.to_dict()
