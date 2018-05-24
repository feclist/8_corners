import datetime


def get_nested_value(dict, attributes):
    """
    Retrieves a nested object within a dictionary according
    to given attributes. Attributes is a string of attributes
    separated by a '.'.

    Example:
     Having 'attr1.attr2' resolves to dict['attr1']['attr2']

    :param dict: A dictionary object containing the nested value
    :param attributes: A string with attributes.
    :return: The nested value in the dict
    """
    val = dict
    for attr in attributes.split('.'):
        val = val[attr]
    return val


def unix_to_datetime_string(date):
    return datetime.datetime.fromtimestamp(int(date)).strftime('%Y-%m-%d %H:%M:%S')
