import pytest
from contexts.reporting.domain.services.malfunction_report_service import MalfunctionReportService
from contexts.discovery.domain.entities.operational_station import OperationalStation
from contexts.shared_kernel.common.station_id import StationId
from contexts.reporting.domain.enums.malfunction_type import MalfunctionType
from contexts.discovery.domain.value_objects.station_status import StationStatus
from contexts.discovery.infrastructure.repositories.in_memory_station_repository import InMemoryStationRepository
from contexts.reporting.infrastructure.repositories.in_memory_report_repository import InMemoryReportRepository


class TestMalfunctionReportService:
    """Integration tests for the complete malfunction reporting workflow"""
    
    @pytest.fixture
    def service(self):
        """Create service with in-memory repositories"""
        station_repo = InMemoryStationRepository()
        report_repo = InMemoryReportRepository()
        
        # Pre-populate with test station
        test_station = OperationalStation(
            station_id=StationId("STATION-001"),
            name="Test Charging Station",
            postal_code="10178",
            address="Alexanderplatz 1"
        )
        station_repo.save(test_station)
        
        return MalfunctionReportService(
            report_repository=report_repo,
            station_repository=station_repo
        )
    
    def test_submit_malfunction_report(self, service):
        """Test submitting a malfunction report"""
        report_id = service.submit_malfunction_report(
            station_id="STATION-001",
            malfunction_type=MalfunctionType.NOT_CHARGING,
            description="Vehicle not charging properly at this station",
            reported_by="user@example.com"
        )
        
        assert report_id is not None
        
        # Verify report was saved
        report = service._report_repository.find_by_id(report_id)
        assert report is not None
        assert report.station_id.value == "STATION-001"
    
    def test_process_valid_report_creates_ticket_and_marks_station_defective(self, service):
        """Test complete workflow: submit -> process -> ticket created -> station defective"""
        # Submit report
        report_id = service.submit_malfunction_report(
            station_id="STATION-001",
            malfunction_type=MalfunctionType.PAYMENT_FAILURE,
            description="Payment terminal completely unresponsive"
        )
        
        # Process the report
        result = service.process_malfunction_report(report_id)
        
        assert result.success is True
        assert result.ticket_id is not None
        assert result.errors == []
        
        # Verify station is marked defective
        station = service._station_repository.find_by_id(StationId("STATION-001"))
        assert station.status == StationStatus.DEFECTIVE
        
        # Verify report has ticket
        report = service._report_repository.find_by_id(report_id)
        assert report.ticket_id is not None
    
    def test_resolve_malfunction_restores_station(self, service):
        """Test resolving malfunction restores station to available"""
        # Submit and process report
        report_id = service.submit_malfunction_report(
            station_id="STATION-001",
            malfunction_type=MalfunctionType.CONNECTOR_ISSUE,
            description="Connector cable is damaged and needs replacement"
        )
        
        result = service.process_malfunction_report(report_id)
        ticket_id = result.ticket_id
        
        # Resolve the malfunction
        service.resolve_malfunction(
            ticket_id=ticket_id,
            operator_notes="Replaced damaged connector cable. Station tested and working."
        )
        
        # Station should be available again
        station = service._station_repository.find_by_id(StationId("STATION-001"))
        assert station.status == StationStatus.AVAILABLE