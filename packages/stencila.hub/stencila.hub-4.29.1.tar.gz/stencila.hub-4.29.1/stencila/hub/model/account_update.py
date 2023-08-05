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


class AccountUpdate(ModelNormal):
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
        ('theme',): {
            'BOOTSTRAP': "bootstrap",
            'ELIFE': "elife",
            'F1000': "f1000",
            'GALLERIA': "galleria",
            'GIGA': "giga",
            'LATEX': "latex",
            'NATURE': "nature",
            'PLOS': "plos",
            'RPNG': "rpng",
            'SKELETON': "skeleton",
            'STENCILA': "stencila",
            'TUFTE': "tufte",
            'WILMORE': "wilmore",
        },
    }

    validations = {
        ('name',): {
            'min_length': 1,
        },
        ('display_name',): {
            'max_length': 256,
        },
        ('location',): {
            'max_length': 256,
        },
        ('website',): {
            'max_length': 200,
        },
        ('email',): {
            'max_length': 254,
        },
        ('first_name',): {
            'min_length': 1,
        },
        ('last_name',): {
            'min_length': 1,
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
            'name': (str,),  # noqa: E501
            'id': (int,),  # noqa: E501
            'user': (int, none_type,),  # noqa: E501
            'creator': (int,),  # noqa: E501
            'created': (datetime,),  # noqa: E501
            'display_name': (str, none_type,),  # noqa: E501
            'location': (str, none_type,),  # noqa: E501
            'image': (str, none_type,),  # noqa: E501
            'website': (str, none_type,),  # noqa: E501
            'email': (str, none_type,),  # noqa: E501
            'theme': (str,),  # noqa: E501
            'extra_head': (str, none_type,),  # noqa: E501
            'extra_top': (str, none_type,),  # noqa: E501
            'extra_bottom': (str, none_type,),  # noqa: E501
            'hosts': (str, none_type,),  # noqa: E501
            'first_name': (str,),  # noqa: E501
            'last_name': (str,),  # noqa: E501
        }

    @cached_property
    def discriminator():
        return None


    attribute_map = {
        'name': 'name',  # noqa: E501
        'id': 'id',  # noqa: E501
        'user': 'user',  # noqa: E501
        'creator': 'creator',  # noqa: E501
        'created': 'created',  # noqa: E501
        'display_name': 'displayName',  # noqa: E501
        'location': 'location',  # noqa: E501
        'image': 'image',  # noqa: E501
        'website': 'website',  # noqa: E501
        'email': 'email',  # noqa: E501
        'theme': 'theme',  # noqa: E501
        'extra_head': 'extraHead',  # noqa: E501
        'extra_top': 'extraTop',  # noqa: E501
        'extra_bottom': 'extraBottom',  # noqa: E501
        'hosts': 'hosts',  # noqa: E501
        'first_name': 'firstName',  # noqa: E501
        'last_name': 'lastName',  # noqa: E501
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
    def __init__(self, name, *args, **kwargs):  # noqa: E501
        """AccountUpdate - a model defined in OpenAPI

        Args:
            name (str): Name of the account. Lowercase and no spaces or leading numbers. Will be used in URLS e.g. https://hub.stenci.la/awesome-org

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
            user (int, none_type): The user for this account. Only applies to personal accounts.. [optional]  # noqa: E501
            creator (int): The user who created the account.. [optional]  # noqa: E501
            created (datetime): The time the account was created.. [optional]  # noqa: E501
            display_name (str, none_type): Name to display in account profile.. [optional]  # noqa: E501
            location (str, none_type): Location to display in account profile.. [optional]  # noqa: E501
            image (str, none_type): Image for the account.. [optional]  # noqa: E501
            website (str, none_type): URL to display in account profile.. [optional]  # noqa: E501
            email (str, none_type): An email to display in account profile. Will not be used by Stencila to contact you.. [optional]  # noqa: E501
            theme (str): The default theme for the account.. [optional]  # noqa: E501
            extra_head (str, none_type): Content to inject into the <head> element of HTML served for this account.. [optional]  # noqa: E501
            extra_top (str, none_type): Content to inject at the top of the <body> element of HTML served for this account.. [optional]  # noqa: E501
            extra_bottom (str, none_type): Content to inject at the bottom of the <body> element of HTML served for this account.. [optional]  # noqa: E501
            hosts (str, none_type): A space separated list of valid hosts for the account. Used for setting Content Security Policy headers when serving content for this account.. [optional]  # noqa: E501
            first_name (str): Your first names (given names).. [optional] if omitted the server will use the default value of ""  # noqa: E501
            last_name (str): Your last names (family names, surnames).. [optional] if omitted the server will use the default value of ""  # noqa: E501
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

        self.name = name
        for var_name, var_value in kwargs.items():
            if var_name not in self.attribute_map and \
                        self._configuration is not None and \
                        self._configuration.discard_unknown_keys and \
                        self.additional_properties_type is None:
                # discard variable.
                continue
            setattr(self, var_name, var_value)
