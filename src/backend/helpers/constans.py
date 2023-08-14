""" Module containing constants used in project. """


class ValidationNamespace():
    """ User validation constants class. """

    def __init__(self):
        """ Class constructor. """
        self.USER_EXISTS = 'User exists in DB.'
        self.UNKNOWN_USER = 'User does not exist.'
        self.DB_ERROR = 'No data in DB.'
        self.NO_VAS_DATA = 'No vas data'


VALIDATION_NAMESPACE = ValidationNamespace()