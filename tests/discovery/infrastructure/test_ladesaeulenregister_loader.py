"""Tests for LadesaeulenregisterLoader"""
import pytest
from contexts.discovery.infrastructure.data.ladesaeulenregister_loader import LadesaeulenregisterLoader


class TestLadesaeulenregisterLoader:
    """Test suite for CSV data loader"""
    
    def test_load_berlin_stations(self):
        """Test loading Berlin stations from CSV"""
        loader = LadesaeulenregisterLoader()
        stations = loader.load_berlin_stations()
        
        # Should load at least some stations
        assert len(stations) > 0
        # All stations should have postal codes
        assert all(station.postal_code for station in stations)
    
    def test_stations_have_required_fields(self):
        """Test that loaded stations have all required fields"""
        loader = LadesaeulenregisterLoader()
        stations = loader.load_berlin_stations()
        
        # Check first station has required fields
        station = stations[0]
        assert station.station_id is not None
        assert station.name is not None
        assert station.postal_code is not None
        assert station.station_id.value.startswith("BERLIN-")
    
    def test_stations_have_berlin_prefix(self):
        """Test that all loaded stations have BERLIN prefix in ID"""
        loader = LadesaeulenregisterLoader()
        stations = loader.load_berlin_stations()
        
        # All station IDs should start with BERLIN-
        for station in stations:
            assert station.station_id.value.startswith('BERLIN-'), \
                f"Station {station.station_id.value} doesn't have BERLIN- prefix"
    
    def test_get_summary(self):
        """Test getting summary statistics"""
        loader = LadesaeulenregisterLoader()
        summary = loader.get_summary()
        
        assert 'total_berlin_stations' in summary
        assert 'unique_postal_codes' in summary
        assert 'stations_per_postal_code' in summary
        assert 'stations_with_coordinates' in summary
        assert 'coverage_percentage' in summary
        
        assert summary['total_berlin_stations'] > 0
        assert summary['unique_postal_codes'] > 0
        assert isinstance(summary['stations_per_postal_code'], dict)
    
    def test_no_duplicate_locations(self):
        """Test that there are no duplicate station locations"""
        loader = LadesaeulenregisterLoader()
        stations = loader.load_berlin_stations()
        
        # Create location keys (postal code + address)
        locations = []
        for station in stations:
            location_key = f"{station.postal_code}-{station.address}"
            locations.append(location_key)
        
        # Check: number of unique locations should equal total stations
        # (loader already filters duplicates, so this should always pass)
        unique_locations = set(locations)
        assert len(locations) == len(unique_locations), "Found duplicate station locations"
    
    def test_csv_file_exists(self):
        """Test that CSV file is found during initialization"""
        loader = LadesaeulenregisterLoader()
        assert loader.csv_path.exists()
    
    def test_stations_have_valid_postal_codes(self):
        """Test that all stations have 5-digit postal codes"""
        loader = LadesaeulenregisterLoader()
        stations = loader.load_berlin_stations()
        
        for station in stations:
            assert len(station.postal_code) == 5, \
                f"Station {station.station_id.value} has invalid postal code length: {station.postal_code}"
            assert station.postal_code.isdigit(), \
                f"Station {station.station_id.value} has non-numeric postal code: {station.postal_code}"
    
    def test_station_names_not_empty(self):
        """Test that all stations have names"""
        loader = LadesaeulenregisterLoader()
        stations = loader.load_berlin_stations()
        
        for station in stations:
            assert station.name, f"Station {station.station_id.value} has empty name"
            assert len(station.name) > 0
            assert len(station.name) <= 100  # Should be truncated if too long