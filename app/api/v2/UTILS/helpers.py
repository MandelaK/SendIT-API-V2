"""This module contains helpers we will use for validating"""


def validate_string(word):
    """This function validates strings that we get from
    the user before we add the values to our database"""
    if type(word) is not str:
        return False
    elif bool(word.strip()) is False:
        return False
    elif validate_int(word):
        return False
    else:
        return True


def validate_int(number):
    """This function validates the numbers we get from
    the user before we can add them to our database"""
    try:
        int(number)
    except ValueError:
        return False
    else:
        # we will not pass a number greater than zero anywhere
        # in our app, so we reject zero alltogether
        if int(number) <= 0:
            return False
        return True


def validate_phone_number(phone):
    """This will simply check if the number is integer and less than 10
    or greater than 13."""

    if not phone:
        return False
    elif len(phone) <= 9 or len(phone) >= 14:
        return False
    elif validate_int(phone):
        return True
    else:
        return False
