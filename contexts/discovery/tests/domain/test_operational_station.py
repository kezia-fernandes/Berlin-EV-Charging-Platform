import pytest
from contexts.discovery.domain.entities.operational_station import OperationalStation
from contexts.shared_kernel.common.station_id import StationId
from contexts.discovery.domain.value_objects.station_status import StationStatus


class TestOperationalStation:
    """Test suite for OperationalStation entity"""
    
    def test_create_operational_station(self):
        """Test creating a basic operational station"""
        station_id = StationId("STATION-001")
        name = "Alexanderplatz Charging Hub"
        postal_code = "10178"
        
        station = OperationalStation(
            station_id=station_id,
            name=name,
            postal_code=postal_code
        )
        
        assert station.station_id == station_id
        assert station.name == name
        assert station.postal_code == postal_code
        assert station.status == StationStatus.AVAILABLE
        assert station.is_operational is True
    
    def test_mark_station_as_defective(self):
        """Test marking an available station as defective"""
        station = OperationalStation(
            station_id=StationId("STATION-001"),
            name="Test Station",
            postal_code="10178"
        )
        
        station.mark_as_defective()
        
        assert station.status == StationStatus.DEFECTIVE
        assert station.is_operational is False
    
    def test_restore_defective_station_to_available(self):
        """Test restoring a defective station to available"""
        station = OperationalStation(
            station_id=StationId("STATION-001"),
            name="Test Station",
            postal_code="10178"
        )
        station.mark_as_defective()
        
        station.mark_as_available()
        
        assert station.status == StationStatus.AVAILABLE
        assert station.is_operational is True