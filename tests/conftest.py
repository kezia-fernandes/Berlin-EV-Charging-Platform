"""Shared test fixtures for all contexts"""
import pytest
from contexts.discovery.infrastructure.repositories.in_memory_station_repository import InMemoryStationRepository
from contexts.reporting.infrastructure.repositories.in_memory_report_repository import InMemoryReportRepository
from contexts.discovery.domain.entities.operational_station import OperationalStation
from contexts.shared_kernel.common.station_id import StationId


@pytest.fixture
def station_repository():
    """Provide a clean station repository for tests"""
    return InMemoryStationRepository()


@pytest.fixture
def report_repository():
    """Provide a clean report repository for tests"""
    return InMemoryReportRepository()


@pytest.fixture
def sample_station(station_repository):
    """Provide a sample operational station"""
    station = OperationalStation(
        station_id=StationId("TEST-STATION-001"),
        name="Test Charging Station",
        postal_code="10115"
    )
    station_repository.save(station)
    return station
