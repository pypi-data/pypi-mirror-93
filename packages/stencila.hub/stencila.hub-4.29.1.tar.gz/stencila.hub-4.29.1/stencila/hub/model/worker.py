"""
    Stencila Hub API

    ## Authentication  Many endpoints in the Stencila Hub API require an authentication token. These tokens carry many privileges, so be sure to keep them secure. Do not place your tokens in publicly accessible areas such as client-side code. The API is only served over HTTPS to avoid exposing tokens and other data on the network.  To obtain a token, [`POST /api/tokens`](#operations-tokens-tokens_create) with either a `username` and `password` pair, or an [OpenID Connect](https://openid.net/connect/) token. Then use the token in the `Authorization` header of subsequent requests with the prefix `Token` e.g.      curl -H \"Authorization: Token 48866b1e38a2e9db0baada2140b2327937f4a3636dd5f2dfd8c212341c88d34\" https://hub.stenci.la/api/projects/  Alternatively, you can use `Basic` authentication with the token used as the username and no password. This can be more convenient when using command line tools such as [cURL](https://curl.haxx.se/) e.g.      curl -u 48866b1e38a2e9db0baada2140b2327937f4a3636dd5f2dfd8c212341c88d34: https://hub.stenci.la/api/projects/  Or, the less ubiquitous, but more accessible [httpie](https://httpie.org/):      http --auth 48866b1e38a2e9db0baada2140b2327937f4a3636dd5f2dfd8c212341c88d34: https://hub.stenci.la/api/projects/  In both examples above, the trailing colon is not required but avoids being asked for a password.  ## Versioning  The Stencila Hub is released using semantic versioning. The current version is available from the [`GET /api/status`](/api/status) endpoint. Please see the [Github release page](https://github.com/stencila/hub/releases) and the [changelog](https://github.com/stencila/hub/blob/master/CHANGELOG.md) for details on each release. We currently do not provide versioning of the API but plan to do so soon (probably by using a `Accept: application/vnd.stencila.hub+json;version=1.0` request header). If you are using, or interested in using, the API please contact us and we may be able to expedite this.   # noqa: E501

    The version of the OpenAPI document: v1
    Contact: hello@stenci.la
    Generated by: https://openapi-generator.tech
"""


import re  # noqa: F401
import sys  # noqa: F401

import nulltype  # noqa: F401

from stencila.hub.model_utils import (  # noqa: F401
    ApiTypeError,
    ModelComposed,
    ModelNormal,
    ModelSimple,
    cached_property,
    change_keys_js_to_python,
    convert_js_args_to_python_args,
    date,
    datetime,
    file_type,
    none_type,
    validate_get_composed_info,
)


class Worker(ModelNormal):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.

    Attributes:
      allowed_values (dict): The key is the tuple path to the attribute
          and the for var_name this is (var_name,). The value is a dict
          with a capitalized key describing the allowed value and an allowed
          value. These dicts store the allowed enum values.
      attribute_map (dict): The key is attribute name
          and the value is json key in definition.
      discriminator_value_class_map (dict): A dict to go from the discriminator
          variable value to the discriminator class name.
      validations (dict): The key is the tuple path to the attribute
          and the for var_name this is (var_name,). The value is a dict
          that stores validations for max_length, min_length, max_items,
          min_items, exclusive_maximum, inclusive_maximum, exclusive_minimum,
          inclusive_minimum, and regex.
      additional_properties_type (tuple): A tuple of classes accepted
          as additional properties values.
    """

    allowed_values = {
    }

    validations = {
        ('hostname',): {
            'max_length': 512,
            'min_length': 1,
        },
        ('queues',): {
        },
        ('software',): {
            'max_length': 256,
        },
        ('os',): {
            'max_length': 64,
        },
        ('signature',): {
            'max_length': 512,
        },
    }

    additional_properties_type = None

    _nullable = False

    @cached_property
    def openapi_types():
        """
        This must be a method because a model may have properties that are
        of type self, this must run after the class is loaded

        Returns
            openapi_types (dict): The key is attribute name
                and the value is attribute type.
        """
        return {
            'hostname': (str,),  # noqa: E501
            'queues': ([int],),  # noqa: E501
            'id': (int,),  # noqa: E501
            'active': (bool,),  # noqa: E501
            'created': (datetime,),  # noqa: E501
            'started': (datetime, none_type,),  # noqa: E501
            'updated': (datetime, none_type,),  # noqa: E501
            'finished': (datetime, none_type,),  # noqa: E501
            'utcoffset': (int, none_type,),  # noqa: E501
            'pid': (int, none_type,),  # noqa: E501
            'freq': (float, none_type,),  # noqa: E501
            'software': (str, none_type,),  # noqa: E501
            'os': (str, none_type,),  # noqa: E501
            'details': ({str: (bool, date, datetime, dict, float, int, list, str, none_type)}, none_type,),  # noqa: E501
            'signature': (str, none_type,),  # noqa: E501
        }

    @cached_property
    def discriminator():
        return None


    attribute_map = {
        'hostname': 'hostname',  # noqa: E501
        'queues': 'queues',  # noqa: E501
        'id': 'id',  # noqa: E501
        'active': 'active',  # noqa: E501
        'created': 'created',  # noqa: E501
        'started': 'started',  # noqa: E501
        'updated': 'updated',  # noqa: E501
        'finished': 'finished',  # noqa: E501
        'utcoffset': 'utcoffset',  # noqa: E501
        'pid': 'pid',  # noqa: E501
        'freq': 'freq',  # noqa: E501
        'software': 'software',  # noqa: E501
        'os': 'os',  # noqa: E501
        'details': 'details',  # noqa: E501
        'signature': 'signature',  # noqa: E501
    }

    _composed_schemas = {}

    required_properties = set([
        '_data_store',
        '_check_type',
        '_spec_property_naming',
        '_path_to_item',
        '_configuration',
        '_visited_composed_classes',
    ])

    @convert_js_args_to_python_args
    def __init__(self, hostname, queues, *args, **kwargs):  # noqa: E501
        """Worker - a model defined in OpenAPI

        Args:
            hostname (str): The `hostname` of the worker.
            queues ([int]): The queues that this worker is listening to.

        Keyword Args:
            _check_type (bool): if True, values for parameters in openapi_types
                                will be type checked and a TypeError will be
                                raised if the wrong type is input.
                                Defaults to True
            _path_to_item (tuple/list): This is a list of keys or values to
                                drill down to the model in received_data
                                when deserializing a response
            _spec_property_naming (bool): True if the variable names in the input data
                                are serialized names, as specified in the OpenAPI document.
                                False if the variable names in the input data
                                are pythonic names, e.g. snake case (default)
            _configuration (Configuration): the instance to use when
                                deserializing a file_type parameter.
                                If passed, type conversion is attempted
                                If omitted no type conversion is done.
            _visited_composed_classes (tuple): This stores a tuple of
                                classes that we have traveled through so that
                                if we see that class again we will not use its
                                discriminator again.
                                When traveling through a discriminator, the
                                composed schema that is
                                is traveled through is added to this set.
                                For example if Animal has a discriminator
                                petType and we pass in "Dog", and the class Dog
                                allOf includes Animal, we move through Animal
                                once using the discriminator, and pick Dog.
                                Then in Dog, we will make an instance of the
                                Animal class but this time we won't travel
                                through its discriminator because we passed in
                                _visited_composed_classes = (Animal,)
            id (int): [optional]  # noqa: E501
            active (bool): [optional]  # noqa: E501
            created (datetime): The time that the worker started (time of the first event for the worker).. [optional]  # noqa: E501
            started (datetime, none_type): The time that the worker started (only recorded on a 'worker-online' event).. [optional]  # noqa: E501
            updated (datetime, none_type): The time that the last heatbeat was received for the worker.. [optional]  # noqa: E501
            finished (datetime, none_type): The time that the worker finished (only recorded on a 'worker-offline' event). [optional]  # noqa: E501
            utcoffset (int, none_type): The `utcoffset` of the worker.. [optional]  # noqa: E501
            pid (int, none_type): The `pid` of the worker.. [optional]  # noqa: E501
            freq (float, none_type): The worker's heatbeat frequency (in seconds). [optional]  # noqa: E501
            software (str, none_type): The name and version of the worker's software.. [optional]  # noqa: E501
            os (str, none_type): Operating system that the worker is running on.. [optional]  # noqa: E501
            details ({str: (bool, date, datetime, dict, float, int, list, str, none_type)}, none_type): Details about the worker including queues and statsSee https://docs.celeryproject.org/en/stable/userguide/workers.html#statistics. [optional]  # noqa: E501
            signature (str, none_type): The signature of the worker used to identify it. It is possible, but unlikely, that two or more active workers have the same signature.. [optional]  # noqa: E501
        """

        _check_type = kwargs.pop('_check_type', True)
        _spec_property_naming = kwargs.pop('_spec_property_naming', False)
        _path_to_item = kwargs.pop('_path_to_item', ())
        _configuration = kwargs.pop('_configuration', None)
        _visited_composed_classes = kwargs.pop('_visited_composed_classes', ())

        if args:
            raise ApiTypeError(
                "Invalid positional arguments=%s passed to %s. Remove those invalid positional arguments." % (
                    args,
                    self.__class__.__name__,
                ),
                path_to_item=_path_to_item,
                valid_classes=(self.__class__,),
            )

        self._data_store = {}
        self._check_type = _check_type
        self._spec_property_naming = _spec_property_naming
        self._path_to_item = _path_to_item
        self._configuration = _configuration
        self._visited_composed_classes = _visited_composed_classes + (self.__class__,)

        self.hostname = hostname
        self.queues = queues
        for var_name, var_value in kwargs.items():
            if var_name not in self.attribute_map and \
                        self._configuration is not None and \
                        self._configuration.discard_unknown_keys and \
                        self.additional_properties_type is None:
                # discard variable.
                continue
            setattr(self, var_name, var_value)
