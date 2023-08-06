"""
    Parser
"""


class Parser:
    """
        Parser
    """

    def __init__(self, definition=None):
        """
        Text line format definition
        """
        self.definition = definition

    def set_definition(self, definition):
        """
        Set definition
        :param definition:
        :return:
        """
        self.definition = definition

    def parse(self, text_line):
        """
        Parse text line record
        :param text_line:
        :return:
        """
        self.is_definition()
        data = []
        for field in self.definition:
            parsed_val = self.substr(text_line, self.definition[field][0], self.definition[field][1]).strip()
            if len(self.definition[field]) == 4:
                data.append(self.convert(self.definition[field][2], parsed_val, self.definition[field][3]))
            else:
                data.append(self.convert(self.definition[field][2], parsed_val))

        return data

    def parse2object(self, text_line):
        self.is_definition()
        key = 0
        data = self.parse(text_line)
        obj = ParsedObject()
        for field in self.definition:
            setattr(obj, field, data[key])
            key += 1

        return obj

    def get_fields(self):
        """
        Get definition fields name
        :return:
        """
        return list(self.definition.keys())

    def csv_from_array(self, array_data, delimiter=','):
        """
        Create CSV from array data
        :param array_data:
        :param delimiter:
        :return:
        """
        return delimiter.join(array_data)

    def array_from_csv(self, csv, delimiter=','):
        """
        Create array data from CSV
        :param csv:
        :param delimiter:
        :return:
        """
        return csv.split(delimiter)

    def parse_int(self, value, default=None):
        """
        Parse integer from string
        :param value:
        :param default:
        :return:
        """
        try:
            return int(float(value.strip()))
        except:
            return default

    def parse_float(self, value, default=None):
        """
        Parse float from string
        :param value:
        :param default:
        :return:
        """
        try:
            return float(value.strip())
        except:
            return default

    def substr(self, text, start, length):
        """
        :param text:
        :param start:
        :param length:
        :return:
        """
        return text[start:start + length]

    def convert(self, value_type, string_value, default_value=None):
        """
        Converts string value to value as per value_type
        :param value_type:
        :param string_value:
        :param default_value:
        :return:
        """
        if value_type == 'string':
            if len(string_value) == 0:
                return default_value
            return string_value
        elif value_type == 'integer':
            return self.parse_int(string_value, default_value)
        elif value_type == 'float':
            return self.parse_float(string_value, default_value)
        else:
            return string_value

    def is_definition(self):
        """
        Check if format definition is set
        :return:
        """
        if self.definition is None:
            raise Exception('Text line format definition missing !')

    # *** TO OVERRIDE ***
    def format_from_array(self, array_data):
        """
        Converts array to text line according to the definition
        """
        raise NotImplementedError()


class ParsedObject:
    pass
