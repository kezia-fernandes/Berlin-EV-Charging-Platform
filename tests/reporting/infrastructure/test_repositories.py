import pytest
from uuid import uuid4
from contexts.reporting.domain.entities.malfunction_report import MalfunctionReport
from contexts.shared_kernel.common.station_id import StationId
from contexts.reporting.domain.value_objects.report_description import ReportDescription
from contexts.reporting.domain.enums.malfunction_type import MalfunctionType
from contexts.reporting.infrastructure.repositories.in_memory_report_repository import InMemoryReportRepository


class TestInMemoryReportRepository:
    """Test in-memory implementation of report repository"""
    
    @pytest.fixture
    def repository(self):
        """Create a fresh repository for each test"""
        return InMemoryReportRepository()
    
    @pytest.fixture
    def sample_report(self):
        """Create a sample report for testing"""
        return MalfunctionReport(
            report_id=uuid4(),
            station_id=StationId("STATION-001"),
            malfunction_type=MalfunctionType.NOT_CHARGING,
            description=ReportDescription("Test malfunction report")
        )
    
    def test_save_and_find_report(self, repository, sample_report):
        """Test saving and retrieving a report"""
        repository.save(sample_report)
        found = repository.find_by_id(sample_report.report_id)
        
        assert found is not None
        assert found.report_id == sample_report.report_id
    
    def test_find_reports_by_station(self, repository):
        """Test finding all reports for a specific station"""
        station_id = StationId("STATION-001")
        report1 = MalfunctionReport(
            report_id=uuid4(),
            station_id=station_id,
            malfunction_type=MalfunctionType.NOT_CHARGING,
            description=ReportDescription("First report for testing")
        )
        report2 = MalfunctionReport(
            report_id=uuid4(),
            station_id=station_id,
            malfunction_type=MalfunctionType.PAYMENT_FAILURE,
            description=ReportDescription("Second report for testing")
        )
        
        repository.save(report1)
        repository.save(report2)
        
        station_reports = repository.find_by_station(station_id)
        
        assert len(station_reports) == 2