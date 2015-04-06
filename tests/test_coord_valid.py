import unittest


class TestCoordValid(unittest.TestCase):

    def test_negative_values_invalid(self):
        from ModestMaps.Core import Coordinate
        from mapzen.util import is_valid
        invalid_coords = (
            (-1, 0, 0),
            (1, -1, 0),
            (1, 0, -1),
        )
        for (zoom, column, row) in invalid_coords:
            coord = Coordinate(zoom=zoom, column=column, row=row)
            self.failIf(is_valid(coord), coord)

    def test_vals_not_in_range(self):
        from ModestMaps.Core import Coordinate
        from mapzen.util import is_valid
        invalid_coords = (
            (0, 1, 0),
            (2, 0, 4),
            (1, 2, 2),
        )
        for (zoom, column, row) in invalid_coords:
            coord = Coordinate(zoom=zoom, column=column, row=row)
            self.failIf(is_valid(coord), coord)

    def test_valid_coords(self):
        from ModestMaps.Core import Coordinate
        from mapzen.util import is_valid
        valid_coords = (
            (0, 0, 0),
            (2, 1, 1),
            (3, 7, 7),
            (1, 0, 1),
        )
        for (zoom, column, row) in valid_coords:
            coord = Coordinate(zoom=zoom, column=column, row=row)
            self.failUnless(is_valid(coord), coord)
