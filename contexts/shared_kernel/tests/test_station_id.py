import pytest
from contexts.shared_kernel.common.station_id import StationId


def test_create_valid_station_id():
    """Test creating a valid station ID"""
    station_id = StationId("STATION-001")
    assert station_id.value == "STATION-001"


def test_empty_station_id_raises_error():
    """Test that empty station ID is rejected"""
    with pytest.raises(ValueError, match="cannot be empty"):
        StationId("")


def test_whitespace_only_station_id_raises_error():
    """Test that whitespace-only ID is rejected"""
    with pytest.raises(ValueError, match="cannot be empty"):
        StationId("   ")


def test_station_id_too_long_raises_error():
    """Test maximum length validation"""
    with pytest.raises(ValueError, match="too long"):
        StationId("A" * 51)


def test_station_id_is_immutable():
    """Test that station ID cannot be changed after creation"""
    station_id = StationId("STATION-001")
    
    with pytest.raises(Exception):  # frozen dataclass raises error
        station_id.value = "STATION-002"