import pytest
from contexts.discovery.domain.entities.operational_station import OperationalStation
from contexts.shared_kernel.common.station_id import StationId
from contexts.discovery.infrastructure.repositories.in_memory_station_repository import InMemoryStationRepository


class TestInMemoryStationRepository:
    """Test in-memory implementation of station repository"""
    
    @pytest.fixture
    def repository(self):
        """Create a fresh repository for each test"""
        return InMemoryStationRepository()
    
    @pytest.fixture
    def sample_station(self):
        """Create a sample station for testing"""
        return OperationalStation(
            station_id=StationId("STATION-001"),
            name="Test Station",
            postal_code="10178"
        )
    
    def test_save_and_find_station(self, repository, sample_station):
        """Test saving and retrieving a station"""
        repository.save(sample_station)
        found = repository.find_by_id(sample_station.station_id)
        
        assert found is not None
        assert found.station_id == sample_station.station_id
        assert found.name == sample_station.name
    
    def test_find_nonexistent_station_returns_none(self, repository):
        """Test finding a station that doesn't exist"""
        found = repository.find_by_id(StationId("NONEXISTENT"))
        assert found is None
    
    def test_exists_returns_true_for_saved_station(self, repository, sample_station):
        """Test exists method returns True for saved station"""
        repository.save(sample_station)
        exists = repository.exists(sample_station.station_id)
        assert exists is True
    
    def test_find_by_postal_code(self, repository):
        """Test finding stations by postal code"""
        station1 = OperationalStation(
            station_id=StationId("STATION-001"),
            name="Station 1",
            postal_code="10178"
        )
        station2 = OperationalStation(
            station_id=StationId("STATION-002"),
            name="Station 2",
            postal_code="10178"
        )
        station3 = OperationalStation(
            station_id=StationId("STATION-003"),
            name="Station 3",
            postal_code="10785"
        )
        
        repository.save(station1)
        repository.save(station2)
        repository.save(station3)
        
        stations_10178 = repository.find_by_postal_code("10178")
        
        assert len(stations_10178) == 2
        assert all(s.postal_code == "10178" for s in stations_10178)