"""Tests for SearchStationsUseCase"""
import pytest
from contexts.discovery.application.use_cases.search_stations_use_case import SearchStationsUseCase
from contexts.discovery.domain.entities.operational_station import OperationalStation
from contexts.discovery.infrastructure.repositories.in_memory_station_repository import InMemoryStationRepository
from contexts.shared_kernel.common.station_id import StationId


@pytest.fixture
def use_case():
    """Setup use case with test data"""
    repo = InMemoryStationRepository()
    
    stations = [
        OperationalStation(
            station_id=StationId("STATION-001"),
            name="Alexanderplatz Station",
            postal_code="10178"
        ),
        OperationalStation(
            station_id=StationId("STATION-002"),
            name="Mitte Station",
            postal_code="10178"
        ),
        OperationalStation(
            station_id=StationId("STATION-003"),
            name="Kreuzberg Station",
            postal_code="10785"
        ),
    ]
    
    for station in stations:
        repo.save(station)
    
    return SearchStationsUseCase(repo)


class TestSearchStationsUseCase:
    """Test suite for SearchStationsUseCase"""
    
    # ==================== HAPPY PATH ====================
    
    def test_search_by_valid_postal_code(self, use_case):
        """Happy Path: Search by valid postal code"""
        stations = use_case.execute_by_postal_code("10178")
        assert len(stations) == 2
        assert all(s.postal_code == "10178" for s in stations)
    
    def test_search_by_another_valid_postal_code(self, use_case):
        """Happy Path: Search by another postal code"""
        stations = use_case.execute_by_postal_code("10785")
        assert len(stations) == 1
        assert stations[0].name == "Kreuzberg Station"
    
    def test_get_all_stations(self, use_case):
        """Happy Path: Get all stations"""
        stations = use_case.execute_all()
        assert len(stations) == 3
    
    def test_search_by_valid_id(self, use_case):
        """Happy Path: Search by ID"""
        station = use_case.execute_by_id("STATION-001")
        assert station is not None
        assert station.station_id.value == "STATION-001"
    
    # ==================== ERROR SCENARIOS ====================
    
    def test_empty_postal_code_raises_error(self, use_case):
        """Error Scenario: Empty postal code"""
        with pytest.raises(ValueError, match="cannot be empty"):
            use_case.execute_by_postal_code("")
    
    def test_whitespace_postal_code_raises_error(self, use_case):
        """Error Scenario: Whitespace postal code"""
        with pytest.raises(ValueError, match="cannot be empty"):
            use_case.execute_by_postal_code("   ")
    
    def test_invalid_postal_code_format(self, use_case):
        """Error Scenario: Non-numeric postal code"""
        with pytest.raises(ValueError, match="must be numeric only"):
            use_case.execute_by_postal_code("ABCDE")
    
    def test_search_by_nonexistent_id_raises_error(self, use_case):
        """Error Scenario: Nonexistent station ID"""
        with pytest.raises(ValueError, match="not found"):
            use_case.execute_by_id("NONEXISTENT")
    
    # ==================== EDGE CASES ====================
    
    def test_postal_code_too_short(self, use_case):
        """Edge Case: Postal code too short"""
        with pytest.raises(ValueError, match="exactly 5 digits"):
            use_case.execute_by_postal_code("123")
    
    def test_postal_code_too_long(self, use_case):
        """Edge Case: Postal code too long"""
        with pytest.raises(ValueError, match="exactly 5 digits"):
            use_case.execute_by_postal_code("123456")
    
    def test_search_by_postal_code_no_results(self, use_case):
        """Edge Case: Valid postal code but no stations"""
        stations = use_case.execute_by_postal_code("10999")
        assert len(stations) == 0
    
    # ==================== DOMAIN RULES ====================
    
    def test_non_berlin_postal_code_raises_error(self, use_case):
        """Domain Rule: Must be Berlin postal code"""
        with pytest.raises(ValueError, match="Berlin postal code"):
            use_case.execute_by_postal_code("20095")  # Hamburg
    
    def test_get_all_from_empty_repository(self):
        """Domain Rule: Empty repository returns empty list"""
        empty_repo = InMemoryStationRepository()
        use_case = SearchStationsUseCase(empty_repo)
        stations = use_case.execute_all()
        assert len(stations) == 0