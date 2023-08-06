import unittest
from FixedWidthTextParser.Seismic.SpsParser import Sps21Parser, Relation, Sps00Parser, Point


class Sps21ParserTest(unittest.TestCase):
    def test_get_fields(self):
        parser = Sps21Parser()
        fields = parser.get_fields_point()

        self.assertEqual(15, len(fields))
        self.assertEqual(['RECORD_ID', 'LINE', 'POINT', 'POINT_IDX', 'POINT_CODE', 'STATIC_COR', 'POINT_DEPTH', 'DATUM',
                          'UPHOLE_TIME', 'WATER_DEPTH', 'EASTING', 'NORTHING', 'ELEVATION', 'DAY_OF_YEAR', 'TIME'],
                         fields)

    def test_parse_point(self):
        parser = Sps21Parser()
        record = 'S  21528.00  27830.00  1P1             0       756755.8 2561875.5 138.1265120558'

        data = parser.parse_point(record)
        self.assertEqual('S', data[0])
        self.assertEqual(21528.00, data[1])
        self.assertEqual(27830.00, data[2])
        self.assertEqual(1, data[3])
        self.assertEqual('P1', data[4])
        self.assertEqual(None, data[5])
        self.assertEqual(None, data[6])
        self.assertEqual(None, data[7])
        self.assertEqual(0, data[8])
        self.assertEqual(None, data[9])
        self.assertEqual(756755.8, data[10])
        self.assertEqual(2561875.5, data[11])
        self.assertEqual(138.1, data[12])
        self.assertEqual(265, data[13])
        self.assertEqual('120558', data[14])

    def test_parse_point2obj(self):
        parser = Sps21Parser()
        record = 'S  21528.00  27830.00  1P1             0       756755.8 2561875.5 138.1265120558'

        obj = parser.parse_point2obj(record)

        self.assertEqual('S', obj.type)
        self.assertEqual(21528.00, obj.line)
        self.assertEqual(27830.00, obj.point)
        self.assertEqual(1, obj.point_idx)
        self.assertEqual('P1', obj.point_code)
        self.assertEqual(None, obj.static_cor)
        self.assertEqual(None, obj.point_depth)
        self.assertEqual(None, obj.datum)
        self.assertEqual(0, obj.uphole_time)
        self.assertEqual(None, obj.water_depth)
        self.assertEqual(756755.8, obj.easting)
        self.assertEqual(2561875.5, obj.northing)
        self.assertEqual(138.1, obj.elevation)
        self.assertEqual(265, obj.day_of_year)
        self.assertEqual('120558', obj.time)

        record = 'H  21528.00  27830.00  1P1             0       756755.8 2561875.5 138.1265120558'

        obj = parser.parse_point2obj(record)
        self.assertIsNone(obj)

    def test_parse_wrong_record_point(self):
        parser = Sps21Parser()
        record = 'B  21528.00  27830.00  1P1             0       756755.8 2561875.5 138.1265120558'

        data = parser.parse_point(record)
        self.assertIsNone(data)

    def test_parse_not_implemented(self):
        parser = Sps21Parser()
        record = 'X  21528.00  27830.00  1P1             0       756755.8 2561875.5 138.1265120558'

        with self.assertRaises(Exception):
            parser.parse(record)

    def test_format_not_implemented(self):
        parser = Sps21Parser()

        with self.assertRaises(Exception):
            parser.format([])

    def test_csv_point(self):
        parser = Sps21Parser()

        data = parser.get_fields_point()
        csv = parser.csv_from_array(data)
        self.assertEqual(
            'RECORD_ID,LINE,POINT,POINT_IDX,POINT_CODE,STATIC_COR,POINT_DEPTH,DATUM,UPHOLE_TIME,WATER_DEPTH,EASTING,NORTHING,ELEVATION,DAY_OF_YEAR,TIME',
            csv
        )

    def test_parse_relation(self):
        parser = Sps21Parser()
        record = 'X  1001   8287311  19248.00  27516.001    1  4351  27023.00  18875.00  19743.001'

        data = parser.parse_relation(record)

        self.assertEqual('X', data[0])
        self.assertEqual('1001', data[1])
        self.assertEqual(82873, data[2])
        self.assertEqual(1, data[3])
        self.assertEqual('1', data[4])
        self.assertEqual(19248.00, data[5])
        self.assertEqual(27516.00, data[6])
        self.assertEqual(1, data[7])
        self.assertEqual(1, data[8])
        self.assertEqual(435, data[9])
        self.assertEqual(1, data[10])
        self.assertEqual(27023.00, data[11])
        self.assertEqual(18875.00, data[12])
        self.assertEqual(19743.00, data[13])
        self.assertEqual(1, data[14])

        relation = Relation(data)
        self.assertEqual('X', relation.type)
        self.assertEqual('1001', relation.tape)
        self.assertEqual(82873, relation.ffid)
        self.assertEqual(1, relation.ffid_increment)
        self.assertEqual('1', relation.instrument)
        self.assertEqual(19248.00, relation.line)
        self.assertEqual(27516.00, relation.point)
        self.assertEqual(1, relation.point_idx)
        self.assertEqual(1, relation.from_channel)
        self.assertEqual(435, relation.to_channel)
        self.assertEqual(1, relation.channel_increment)
        self.assertEqual(27023.00, relation.rcv_line)
        self.assertEqual(18875.00, relation.from_rcv)
        self.assertEqual(19743.00, relation.to_rcv)
        self.assertEqual(1, relation.rcv_idx)

    def test_parse_wrong_record_relation(self):
        parser = Sps21Parser()
        record = 'B  1001   8287311  19248.00  27516.001    1  4351  27023.00  18875.00  19743.001'

        data = parser.parse_relation(record)
        self.assertIsNone(data)

    def test_csv_relation(self):
        parser = Sps21Parser()

        data = parser.get_fields_relation()
        csv = parser.csv_from_array(data)

        self.assertEqual(
            'RECORD_ID,TAPE_NUMBER,RECORD_NUMBER,RECORD_INCREMENT,INSTRUMENT_CODE,S_LINE,POINT,POINT_IDX,FROM_CHANNEL,TO_CHANNEL,CHANNEL_INCREMENT,R_LINE,FROM_RECEIVER,TO_RECEIVER,RECEIVER_IDX',
            csv
        )

    def test_parsing_empty_string(self):
        parser = Sps21Parser()
        record = ''

        data = parser.parse_point(record)
        self.assertIsNone(data)

        data = parser.parse_relation(record)
        self.assertIsNone(data)

    def test_format_point(self):
        parser = Sps21Parser()
        record = 'S  21528.00  27830.00  1P1             0       756755.8 2561875.5 138.1265120558'

        point = Point(parser.parse_point(record))

        formatted = parser.format_point(point)

        self.assertEqual(record, formatted)


class Sps00ParserTest(unittest.TestCase):
    def test_get_fields(self):
        parser = Sps00Parser()
        fields = parser.get_fields_point()

        self.assertEqual(15, len(fields))
        self.assertEqual(['RECORD_ID', 'LINE', 'POINT', 'POINT_IDX', 'POINT_CODE', 'STATIC_COR', 'POINT_DEPTH', 'DATUM',
                          'UPHOLE_TIME', 'WATER_DEPTH', 'EASTING', 'NORTHING', 'ELEVATION', 'DAY_OF_YEAR', 'TIME'],
                         fields)

    def test_parse_point(self):
        parser = Sps00Parser()
        #                   1         2         3         4         5         6         7
        #         01234567890123456789012345678901234567890123456789012345678901234567890123456789
        record = 'S3762                39611A2     7.2   0  64.8 454773.4 3008241.9  -0.2177042821'

        data = parser.parse_point(record)
        self.assertEqual('S', data[0])
        self.assertEqual(3762, data[1])
        self.assertEqual(3961, data[2])
        self.assertEqual(1, data[3])
        self.assertEqual('A2', data[4])
        self.assertEqual(None, data[5])
        self.assertEqual(7.2, data[6])
        self.assertEqual(0, data[7])
        self.assertEqual(None, data[8])
        self.assertEqual(64.8, data[9])
        self.assertEqual(454773.4, data[10])
        self.assertEqual(3008241.9, data[11])
        self.assertEqual(-0.2, data[12])
        self.assertEqual(177, data[13])
        self.assertEqual('042821', data[14])


if __name__ == '__main__':
    unittest.main()
