#!/usr/bin/env python3
"""
Test Suite for Rubik's Cube Geospatial Mapper
Comprehensive tests for the 6-face geospatial computing system
"""

import unittest
import math
from rubiks_geospatial_mapper import (
    RubiksGeospatialMapper,
    DMSCoordinate,
    GeoVector
)


class TestDMSCoordinate(unittest.TestCase):
    """Test DMS coordinate representation"""
    
    def test_dms_to_string_north(self):
        """Test DMS string formatting for North"""
        dms = DMSCoordinate(45, 30, 15.5, 'N')
        self.assertEqual(dms.to_string(), "45°30'15.5\"N")
    
    def test_dms_to_string_south(self):
        """Test DMS string formatting for South"""
        dms = DMSCoordinate(67, 30, 0.0, 'S')
        self.assertEqual(dms.to_string(), "67°30'0.0\"S")
    
    def test_dms_to_string_east(self):
        """Test DMS string formatting for East"""
        dms = DMSCoordinate(90, 0, 0.0, 'E')
        self.assertEqual(dms.to_string(), "90°0'0.0\"E")
    
    def test_dms_to_string_west(self):
        """Test DMS string formatting for West"""
        dms = DMSCoordinate(135, 0, 0.0, 'W')
        self.assertEqual(dms.to_string(), "135°0'0.0\"W")


class TestRubiksGeospatialMapper(unittest.TestCase):
    """Test the main mapper functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.mapper = RubiksGeospatialMapper()
    
    def test_decimal_to_dms_positive_latitude(self):
        """Test decimal to DMS conversion for positive latitude"""
        dms = self.mapper.decimal_to_dms(45.5, is_latitude=True)
        self.assertEqual(dms.degrees, 45)
        self.assertEqual(dms.minutes, 30)
        self.assertAlmostEqual(dms.seconds, 0.0, places=1)
        self.assertEqual(dms.direction, 'N')
    
    def test_decimal_to_dms_negative_latitude(self):
        """Test decimal to DMS conversion for negative latitude"""
        dms = self.mapper.decimal_to_dms(-67.5, is_latitude=True)
        self.assertEqual(dms.degrees, 67)
        self.assertEqual(dms.minutes, 30)
        self.assertAlmostEqual(dms.seconds, 0.0, places=1)
        self.assertEqual(dms.direction, 'S')
    
    def test_decimal_to_dms_positive_longitude(self):
        """Test decimal to DMS conversion for positive longitude"""
        dms = self.mapper.decimal_to_dms(90.0, is_latitude=False)
        self.assertEqual(dms.degrees, 90)
        self.assertEqual(dms.minutes, 0)
        self.assertAlmostEqual(dms.seconds, 0.0, places=1)
        self.assertEqual(dms.direction, 'E')
    
    def test_decimal_to_dms_negative_longitude(self):
        """Test decimal to DMS conversion for negative longitude"""
        dms = self.mapper.decimal_to_dms(-135.0, is_latitude=False)
        self.assertEqual(dms.degrees, 135)
        self.assertEqual(dms.minutes, 0)
        self.assertAlmostEqual(dms.seconds, 0.0, places=1)
        self.assertEqual(dms.direction, 'W')
    
    def test_dms_to_decimal_north(self):
        """Test DMS to decimal conversion for North"""
        dms = DMSCoordinate(45, 30, 0.0, 'N')
        decimal = self.mapper.dms_to_decimal(dms)
        self.assertAlmostEqual(decimal, 45.5, places=6)
    
    def test_dms_to_decimal_south(self):
        """Test DMS to decimal conversion for South"""
        dms = DMSCoordinate(67, 30, 0.0, 'S')
        decimal = self.mapper.dms_to_decimal(dms)
        self.assertAlmostEqual(decimal, -67.5, places=6)
    
    def test_dms_to_decimal_east(self):
        """Test DMS to decimal conversion for East"""
        dms = DMSCoordinate(90, 0, 0.0, 'E')
        decimal = self.mapper.dms_to_decimal(dms)
        self.assertAlmostEqual(decimal, 90.0, places=6)
    
    def test_dms_to_decimal_west(self):
        """Test DMS to decimal conversion for West"""
        dms = DMSCoordinate(135, 0, 0.0, 'W')
        decimal = self.mapper.dms_to_decimal(dms)
        self.assertAlmostEqual(decimal, -135.0, places=6)
    
    def test_compute_3d_vector_north_pole(self):
        """Test 3D vector computation for North Pole"""
        x, y, z = self.mapper.compute_3d_vector(90, 0)
        self.assertAlmostEqual(x, 0.0, places=6)
        self.assertAlmostEqual(y, 0.0, places=6)
        self.assertAlmostEqual(z, 1.0, places=6)
    
    def test_compute_3d_vector_south_pole(self):
        """Test 3D vector computation for South Pole"""
        x, y, z = self.mapper.compute_3d_vector(-90, 0)
        self.assertAlmostEqual(x, 0.0, places=6)
        self.assertAlmostEqual(y, 0.0, places=6)
        self.assertAlmostEqual(z, -1.0, places=6)
    
    def test_compute_3d_vector_prime_meridian(self):
        """Test 3D vector computation for Prime Meridian"""
        x, y, z = self.mapper.compute_3d_vector(0, 0)
        self.assertAlmostEqual(x, 1.0, places=6)
        self.assertAlmostEqual(y, 0.0, places=6)
        self.assertAlmostEqual(z, 0.0, places=6)
    
    def test_compute_3d_vector_equator_east(self):
        """Test 3D vector computation for Equator East (90°)"""
        x, y, z = self.mapper.compute_3d_vector(0, 90)
        self.assertAlmostEqual(x, 0.0, places=6)
        self.assertAlmostEqual(y, 1.0, places=6)
        self.assertAlmostEqual(z, 0.0, places=6)
    
    def test_compute_3d_vector_equator_west(self):
        """Test 3D vector computation for Equator West (-90°)"""
        x, y, z = self.mapper.compute_3d_vector(0, -90)
        self.assertAlmostEqual(x, 0.0, places=6)
        self.assertAlmostEqual(y, -1.0, places=6)
        self.assertAlmostEqual(z, 0.0, places=6)
    
    def test_compute_3d_vector_antimeridian(self):
        """Test 3D vector computation for Antimeridian (180°)"""
        x, y, z = self.mapper.compute_3d_vector(0, 180)
        self.assertAlmostEqual(x, -1.0, places=6)
        self.assertAlmostEqual(y, 0.0, places=6)
        self.assertAlmostEqual(z, 0.0, places=6)
    
    def test_compute_trig6_zero(self):
        """Test TRIG6 computation for 0 degrees"""
        trig6 = self.mapper.compute_trig6(0)
        self.assertAlmostEqual(trig6['sin'], 0.0, places=6)
        self.assertAlmostEqual(trig6['cos'], 1.0, places=6)
        self.assertAlmostEqual(trig6['tan'], 0.0, places=6)
    
    def test_compute_trig6_45(self):
        """Test TRIG6 computation for 45 degrees"""
        trig6 = self.mapper.compute_trig6(45)
        self.assertAlmostEqual(trig6['sin'], 0.707107, places=5)
        self.assertAlmostEqual(trig6['cos'], 0.707107, places=5)
        self.assertAlmostEqual(trig6['tan'], 1.0, places=5)
        self.assertAlmostEqual(trig6['csc'], 1.414214, places=5)
        self.assertAlmostEqual(trig6['sec'], 1.414214, places=5)
        self.assertAlmostEqual(trig6['cot'], 1.0, places=5)
    
    def test_compute_trig6_90(self):
        """Test TRIG6 computation for 90 degrees"""
        trig6 = self.mapper.compute_trig6(90)
        self.assertAlmostEqual(trig6['sin'], 1.0, places=6)
        self.assertAlmostEqual(trig6['cos'], 0.0, places=6)
        # tan(90) and sec(90) should be inf
        self.assertTrue(math.isinf(trig6['tan']))
        self.assertTrue(math.isinf(trig6['sec']))
    
    def test_cube_to_geovector_u5_north_pole(self):
        """Test U5 (North Pole - center of UP face)"""
        gv = self.mapper.cube_to_geovector('U', 1, 1)
        self.assertEqual(gv.face, 'U')
        self.assertEqual(gv.position, (1, 1))
        self.assertEqual(gv.sticker_id, 'U5')
        self.assertEqual(gv.position_type, 'center')
        self.assertAlmostEqual(gv.lat, 90.0, places=6)
        self.assertAlmostEqual(gv.long, 0.0, places=6)
        self.assertAlmostEqual(gv.vector_3d[2], 1.0, places=6)
    
    def test_cube_to_geovector_d5_south_pole(self):
        """Test D5 (South Pole - center of DOWN face)"""
        gv = self.mapper.cube_to_geovector('D', 1, 1)
        self.assertEqual(gv.face, 'D')
        self.assertEqual(gv.position, (1, 1))
        self.assertEqual(gv.sticker_id, 'D5')
        self.assertEqual(gv.position_type, 'center')
        self.assertAlmostEqual(gv.lat, -90.0, places=6)
        self.assertAlmostEqual(gv.long, 0.0, places=6)
        self.assertAlmostEqual(gv.vector_3d[2], -1.0, places=6)
    
    def test_cube_to_geovector_f5_prime_meridian(self):
        """Test F5 (Prime Meridian - center of FRONT face)"""
        gv = self.mapper.cube_to_geovector('F', 1, 1)
        self.assertEqual(gv.face, 'F')
        self.assertEqual(gv.position, (1, 1))
        self.assertEqual(gv.sticker_id, 'F5')
        self.assertEqual(gv.position_type, 'center')
        self.assertAlmostEqual(gv.lat, 0.0, places=6)
        self.assertAlmostEqual(gv.long, 0.0, places=6)
        self.assertAlmostEqual(gv.vector_3d[0], 1.0, places=6)
    
    def test_cube_to_geovector_b5_antimeridian(self):
        """Test B5 (Antimeridian - center of BACK face)"""
        gv = self.mapper.cube_to_geovector('B', 1, 1)
        self.assertEqual(gv.face, 'B')
        self.assertEqual(gv.position, (1, 1))
        self.assertEqual(gv.sticker_id, 'B5')
        self.assertEqual(gv.position_type, 'center')
        self.assertAlmostEqual(gv.lat, 0.0, places=6)
        self.assertAlmostEqual(gv.long, 180.0, places=6)
        self.assertAlmostEqual(gv.vector_3d[0], -1.0, places=6)
    
    def test_cube_to_geovector_l5_west(self):
        """Test L5 (West - center of LEFT face)"""
        gv = self.mapper.cube_to_geovector('L', 1, 1)
        self.assertEqual(gv.face, 'L')
        self.assertEqual(gv.position, (1, 1))
        self.assertEqual(gv.sticker_id, 'L5')
        self.assertEqual(gv.position_type, 'center')
        self.assertAlmostEqual(gv.lat, 0.0, places=6)
        self.assertAlmostEqual(gv.long, -90.0, places=6)
        self.assertAlmostEqual(gv.vector_3d[1], -1.0, places=6)
    
    def test_cube_to_geovector_r5_east(self):
        """Test R5 (East - center of RIGHT face)"""
        gv = self.mapper.cube_to_geovector('R', 1, 1)
        self.assertEqual(gv.face, 'R')
        self.assertEqual(gv.position, (1, 1))
        self.assertEqual(gv.sticker_id, 'R5')
        self.assertEqual(gv.position_type, 'center')
        self.assertAlmostEqual(gv.lat, 0.0, places=6)
        self.assertAlmostEqual(gv.long, 90.0, places=6)
        self.assertAlmostEqual(gv.vector_3d[1], 1.0, places=6)
    
    def test_cube_to_geovector_corner_positions(self):
        """Test corner position types"""
        corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
        for row, col in corners:
            gv = self.mapper.cube_to_geovector('U', row, col)
            self.assertEqual(gv.position_type, 'corner')
    
    def test_cube_to_geovector_edge_positions(self):
        """Test edge position types"""
        edges = [(0, 1), (1, 0), (1, 2), (2, 1)]
        for row, col in edges:
            gv = self.mapper.cube_to_geovector('U', row, col)
            self.assertEqual(gv.position_type, 'edge')
    
    def test_cube_to_geovector_center_position(self):
        """Test center position type"""
        gv = self.mapper.cube_to_geovector('U', 1, 1)
        self.assertEqual(gv.position_type, 'center')
    
    def test_cube_to_geovector_invalid_face(self):
        """Test invalid face raises ValueError"""
        with self.assertRaises(ValueError):
            self.mapper.cube_to_geovector('X', 0, 0)
    
    def test_cube_to_geovector_invalid_row(self):
        """Test invalid row raises ValueError"""
        with self.assertRaises(ValueError):
            self.mapper.cube_to_geovector('U', 3, 0)
    
    def test_cube_to_geovector_invalid_col(self):
        """Test invalid column raises ValueError"""
        with self.assertRaises(ValueError):
            self.mapper.cube_to_geovector('U', 0, -1)
    
    def test_generate_complete_matrix_count(self):
        """Test complete matrix generates 54 stickers"""
        matrix = self.mapper.generate_complete_matrix()
        self.assertEqual(len(matrix), 54)
    
    def test_generate_complete_matrix_faces(self):
        """Test complete matrix has all 6 faces"""
        matrix = self.mapper.generate_complete_matrix()
        faces = set(gv.face for gv in matrix)
        self.assertEqual(faces, {'U', 'D', 'F', 'B', 'L', 'R'})
    
    def test_generate_complete_matrix_stickers_per_face(self):
        """Test each face has 9 stickers"""
        matrix = self.mapper.generate_complete_matrix()
        for face in ['U', 'D', 'F', 'B', 'L', 'R']:
            face_stickers = [gv for gv in matrix if gv.face == face]
            self.assertEqual(len(face_stickers), 9)
    
    def test_get_face_matrix(self):
        """Test getting stickers for a specific face"""
        self.mapper.generate_complete_matrix()
        face_matrix = self.mapper.get_face_matrix('U')
        self.assertEqual(len(face_matrix), 9)
        self.assertTrue(all(gv.face == 'U' for gv in face_matrix))
    
    def test_export_to_dict_structure(self):
        """Test export to dictionary structure"""
        export = self.mapper.export_to_dict()
        self.assertEqual(export['total_stickers'], 54)
        self.assertEqual(export['faces'], 6)
        self.assertEqual(export['stickers_per_face'], 9)
        self.assertEqual(len(export['stickers']), 54)
    
    def test_export_to_dict_sticker_structure(self):
        """Test individual sticker structure in export"""
        export = self.mapper.export_to_dict()
        sticker = export['stickers'][0]
        
        # Check all required fields exist
        self.assertIn('id', sticker)
        self.assertIn('face', sticker)
        self.assertIn('position', sticker)
        self.assertIn('geolocation', sticker)
        self.assertIn('vector_3d', sticker)
        self.assertIn('angles', sticker)
        self.assertIn('trig6', sticker)
        
        # Check nested structures
        self.assertIn('row', sticker['position'])
        self.assertIn('col', sticker['position'])
        self.assertIn('type', sticker['position'])
        
        self.assertIn('lat_decimal', sticker['geolocation'])
        self.assertIn('long_decimal', sticker['geolocation'])
        self.assertIn('lat_dms', sticker['geolocation'])
        self.assertIn('long_dms', sticker['geolocation'])
        
        self.assertIn('x', sticker['vector_3d'])
        self.assertIn('y', sticker['vector_3d'])
        self.assertIn('z', sticker['vector_3d'])
        
        self.assertIn('theta', sticker['angles'])
        self.assertIn('phi', sticker['angles'])
        
        self.assertIn('sin', sticker['trig6'])
        self.assertIn('cos', sticker['trig6'])
        self.assertIn('tan', sticker['trig6'])
        self.assertIn('csc', sticker['trig6'])
        self.assertIn('sec', sticker['trig6'])
        self.assertIn('cot', sticker['trig6'])
    
    def test_unit_sphere_vectors(self):
        """Test that all vectors are on the unit sphere"""
        matrix = self.mapper.generate_complete_matrix()
        for gv in matrix:
            x, y, z = gv.vector_3d
            magnitude = math.sqrt(x**2 + y**2 + z**2)
            self.assertAlmostEqual(magnitude, 1.0, places=6)


class TestIntegration(unittest.TestCase):
    """Integration tests for the complete system"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.mapper = RubiksGeospatialMapper()
    
    def test_full_matrix_generation(self):
        """Test full matrix generation workflow"""
        matrix = self.mapper.generate_complete_matrix()
        
        # Verify count
        self.assertEqual(len(matrix), 54)
        
        # Verify all stickers have unique IDs
        ids = [gv.sticker_id for gv in matrix]
        self.assertEqual(len(ids), len(set(ids)))
        
        # Verify all stickers have valid coordinates
        for gv in matrix:
            self.assertTrue(-90 <= gv.lat <= 90)
            self.assertTrue(-180 <= gv.long <= 180)
    
    def test_export_and_reimport_consistency(self):
        """Test that export maintains data consistency"""
        matrix = self.mapper.generate_complete_matrix()
        export = self.mapper.export_to_dict()
        
        # Verify each exported sticker matches original
        for i, gv in enumerate(matrix):
            exported = export['stickers'][i]
            self.assertEqual(gv.sticker_id, exported['id'])
            self.assertEqual(gv.face, exported['face'])
            self.assertAlmostEqual(gv.lat, exported['geolocation']['lat_decimal'], places=6)
            self.assertAlmostEqual(gv.long, exported['geolocation']['long_decimal'], places=6)


def main():
    """Run all tests"""
    print("=" * 80)
    print("RUBIK'S CUBE GEOSPATIAL MAPPER - TEST SUITE")
    print("=" * 80)
    
    # Run tests
    unittest.main(verbosity=2)


if __name__ == "__main__":
    main()
