import pytest
from uuid import uuid4

from contexts.reporting.application.use_cases.resolve_malfunction_use_case import ResolveMalfunctionUseCase
from contexts.reporting.application.dtos.resolve_report_dto import ResolveReportRequest
from contexts.reporting.domain.services.malfunction_report_service import MalfunctionReportService
from contexts.reporting.domain.entities.malfunction_report import MalfunctionReport
from contexts.reporting.domain.enums.malfunction_type import MalfunctionType
from contexts.reporting.domain.enums.report_status import ReportStatus
from contexts.reporting.domain.value_objects.report_description import ReportDescription
from contexts.reporting.infrastructure.repositories.in_memory_report_repository import InMemoryReportRepository
from contexts.discovery.infrastructure.repositories.in_memory_station_repository import InMemoryStationRepository
from contexts.discovery.domain.entities.operational_station import OperationalStation
from contexts.shared_kernel.common.station_id import StationId


class TestResolveMalfunctionUseCase:
    """Test suite for ResolveMalfunctionUseCase following TDD principles"""
    
    @pytest.fixture
    def setup(self):
     """Setup repositories, service, and a valid ticket"""
     station_repo = InMemoryStationRepository()
     report_repo = InMemoryReportRepository()
    
     # Create station (available initially)
     station = OperationalStation(
        station_id=StationId("STATION-001"),
        name="Test Station",
        postal_code="10178"
     )
     station_repo.save(station)
    
     service = MalfunctionReportService(report_repo, station_repo)
    
     # Use the service to create a proper report with ticket
     report_id = service.submit_malfunction_report(
        station_id="STATION-001",
        malfunction_type=MalfunctionType.NOT_CHARGING,
        description="Test malfunction report"
     )
    
     # Process it to create the ticket
     result = service.process_malfunction_report(report_id)
    
     use_case = ResolveMalfunctionUseCase(service)
    
     return use_case, station_repo, report_repo, str(result.ticket_id)
    
    # ==================== HAPPY PATH ====================
    
    def test_resolve_valid_malfunction_happy_path(self, setup):
        """Happy Path: Resolve a valid malfunction report"""
        use_case, _, _, ticket_id = setup
        
        request = ResolveReportRequest(ticket_id=ticket_id)
        response = use_case.execute(request)
        
        assert response.success is True
        assert response.ticket_id == ticket_id
        assert response.station_id == "STATION-001"
        assert "resolved" in response.message.lower()
    
    def test_resolve_with_operator_notes(self, setup):
        """Happy Path: Resolve with operator notes"""
        use_case, _, _, ticket_id = setup
        
        request = ResolveReportRequest(
            ticket_id=ticket_id,
            operator_notes="Replaced faulty connector. Tested successfully."
        )
        
        response = use_case.execute(request)
        
        assert response.success is True
    
    # ==================== ERROR SCENARIOS ====================
    
    def test_resolve_with_nonexistent_ticket_id(self, setup):
        """Error Scenario: Nonexistent ticket ID"""
        use_case, _, _, _ = setup
        
        fake_ticket_id = str(uuid4())
        request = ResolveReportRequest(ticket_id=fake_ticket_id)
        response = use_case.execute(request)
        
        assert response.success is False
        assert response.station_id is None
        assert "no report found" in response.message.lower()
    
    def test_resolve_with_empty_ticket_id(self, setup):
        """Error Scenario: Empty ticket ID"""
        use_case, _, _, _ = setup
        
        with pytest.raises(ValueError, match="Ticket ID cannot be empty"):
            ResolveReportRequest(ticket_id="")
    
    def test_resolve_with_invalid_uuid_format(self, setup):
        """Error Scenario: Invalid UUID format"""
        use_case, _, _, _ = setup
        
        request = ResolveReportRequest(ticket_id="not-a-valid-uuid")
        response = use_case.execute(request)
        
        assert response.success is False
    
    # ==================== DOMAIN RULES ====================
    
    def test_station_restored_after_resolution(self, setup):
        """Domain Rule: Station must be restored to available after resolution"""
        use_case, station_repo, _, ticket_id = setup
        
        # Verify station is defective before
        station_before = station_repo.find_by_id(StationId("STATION-001"))
        assert station_before.is_operational is False
        
        # Resolve
        request = ResolveReportRequest(ticket_id=ticket_id)
        response = use_case.execute(request)
        
        assert response.success is True
        
        # Verify station is available after
        station_after = station_repo.find_by_id(StationId("STATION-001"))
        assert station_after.is_operational is True
    
    def test_report_status_updated_after_resolution(self, setup):
        """Domain Rule: Report status must be RESOLVED after resolution"""
        use_case, _, report_repo, ticket_id = setup
        
        # Resolve
        request = ResolveReportRequest(ticket_id=ticket_id)
        response = use_case.execute(request)
        
        assert response.success is True
        
        # Verify report status
        all_reports = report_repo.find_all()
        resolved_report = next(
            (r for r in all_reports if str(r.ticket_id) == ticket_id),
            None
        )
        
        assert resolved_report is not None
        assert resolved_report.status == ReportStatus.RESOLVED