#!/usr/bin/python

from ansible.errors import AnsibleError
import jmespath, validators

__metaclass__ = type

try:
    from __main__ import display
except ImportError:
    from ansible.utils.display import Display

    display = Display()

def ipv4(input):
    try:
        return validators.ipv4(input)
    except ValidationFailure:
        return False

def ipv6(input):
    try:
        return validators.ipv6(input)
    except ValidationFailure:
        return False

def port(input):
    try:
        return isInteger(input) and validators.between(input, 0, 65535)
    except ValidationFailure:
        return False

def email(input):
    try:
        return validators.email(input)
    except ValidationFailure:
        return False

def host(input):
    try:
        return validators.domain(input)
    except ValidationFailure:
        return False

def isInteger(input):
    try:
        cast_float = float(input)
        cast_integer = int(input)
    except ValueError:
        return False
    else:
        return cast_float == cast_integer

def isFloat(input):
    try:
        float(input)
        return True
    except ValueError:
        return False

def isNumber(input):
    return isInteger(input) or isFloat(input)

custom_filters = {
    'ipv4': ipv4,
    'ipv6': ipv6,
    'port': port,
    'email': email,
    'host': host,
    'integer': isInteger,
    'float': isFloat,
    'number': isNumber
}

def validate(collection, vars):
    if not isinstance(collection, list):
        raise AnsibleError("Param must be a <type 'list'>, %s given." % type(collection))

    if not isinstance(vars, dict):
        raise AnsibleError("Param must be a <type 'dict'>, %s given." % type(vars))

    for element in collection:
        path = jmespath.search(element['path'], vars)

        try:
            match = element['match']
        except KeyError:
            match = False

        if path is None:
            raise AnsibleError("Variable %s is undefined." % element['path'])

        if match is False:
            continue

        filter = custom_filters.get(match, False)

        if filter:
            if not filter(path):
                raise AnsibleError("Variable %s is not a valid %s." % (path, match))
            else:
                continue

    return 'Validation success!'

class FilterModule(object):
    def filters(self):
        return {
            'validate': validate
        }
