"""Extension to the Cerberus Validator with common checks."""

from json import load, JSONDecodeError
from os.path import isdir, isfile
from os import access, R_OK, W_OK, X_OK
from cerberus import Validator


class BaseValidator(Validator):
    """Additional format checks."""

    def _isdir(self, field, value):
        """Validate value is a valid, existing directory."""
        if not isdir(value):
            self._error(field, "{} is not a valid directory or does not exist.".format(value))
            return False
        return True


    def _isfile(self, field, value):
        """Validate value is a valid, existing file."""
        if not isfile(value):
            self._error(field, "{} is not a valid file or does not exist.".format(value))
            return False
        return True


    def _isreadable(self, field, value):
        """Validate value is a readable file."""
        if not access(value, R_OK):
            self._error(field, "{} is not readable.".format(value))
            return False
        return True


    def _iswriteable(self, field, value):
        """Validate value is a writeable file."""
        if not access(value, W_OK):
            self._error(field, "{} is not writeable.".format(value))
            return False
        return True


    def _isexecutable(self, field, value):
        """Validate value is an executable file."""
        if not access(value, X_OK):
            self._error(field, "{} is not executable.".format(value))
            return False
        return True


    def _isjsonfile(self, field, value):
        """Validate the JSON file is decodable."""
        if self._isfile(field, value) and self._isreadable(field, value):
            with open(value, "r") as file_ptr:
                try:
                    schema = load(file_ptr)
                except JSONDecodeError as ex:
                    self._error(field, "The file is not decodable JSON: {}".format(ex))
                else:
                    return schema
        return {}


    def _str_errors(self, error):
        str_tuple = (
            'Document path: ' + error.document_path,
            'Schema path: ' + error.schema_path,
            'Code: ' + error.code,
            'Rule: ' + error.rule,
            'Constraint: ' + error.constraint,
            'Value: ' + error.value,
            'Info: ' + error.info)
        return '\n'.join(str_tuple)