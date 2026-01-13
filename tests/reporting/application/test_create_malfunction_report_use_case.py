"""Tests for CreateMalfunctionReportUseCase"""
import pytest
from contexts.reporting.application.use_cases.create_malfunction_report_use_case import CreateMalfunctionReportUseCase
from contexts.reporting.application.dtos.create_report_dto import CreateReportRequest
from contexts.reporting.domain.enums.malfunction_type import MalfunctionType
from contexts.reporting.domain.services.malfunction_report_service import MalfunctionReportService
from contexts.reporting.infrastructure.repositories.in_memory_report_repository import InMemoryReportRepository
from contexts.discovery.infrastructure.repositories.in_memory_station_repository import InMemoryStationRepository
from contexts.discovery.domain.entities.operational_station import OperationalStation
from contexts.shared_kernel.common.station_id import StationId


class TestCreateMalfunctionReportUseCase:
    """Test suite for CreateMalfunctionReportUseCase following TDD principles"""
    
    @pytest.fixture
    def setup(self):
        """Setup repositories and use case"""
        station_repo = InMemoryStationRepository()
        report_repo = InMemoryReportRepository()
        
        # Add test station
        station = OperationalStation(
            station_id=StationId("STATION-001"),
            name="Test Station",
            postal_code="10178"
        )
        station_repo.save(station)
        
        service = MalfunctionReportService(report_repo, station_repo)
        use_case = CreateMalfunctionReportUseCase(service)
        
        return use_case, station_repo, report_repo
    
    # ==================== HAPPY PATH ====================
    
    def test_create_valid_report_happy_path(self, setup):
        """Happy Path: Create a valid malfunction report"""
        use_case, _, _ = setup
        
        request = CreateReportRequest(
            station_id="STATION-001",
            malfunction_type=MalfunctionType.NOT_CHARGING,
            description="The charging station does not deliver power to my vehicle."
        )
        
        response = use_case.execute(request)
        
        assert response.success is True
        assert response.ticket_id is not None
        assert len(response.errors) == 0
        assert not response.has_errors
    
    def test_create_report_with_reporter_email(self, setup):
        """Happy Path: Create report with reporter email"""
        use_case, _, _ = setup
        
        request = CreateReportRequest(
            station_id="STATION-001",
            malfunction_type=MalfunctionType.PAYMENT_FAILURE,
            description="Payment system not responding to card swipe.",
            reported_by="user@example.com"
        )
        
        response = use_case.execute(request)
        
        assert response.success is True
        assert response.ticket_id is not None
    
    # ==================== ERROR SCENARIOS ====================
    
    def test_create_report_for_nonexistent_station(self, setup):
        """Error Scenario: Report for station that doesn't exist"""
        use_case, _, _ = setup
        
        request = CreateReportRequest(
            station_id="NONEXISTENT",
            malfunction_type=MalfunctionType.NOT_CHARGING,
            description="Test report for missing station"
        )
        
        response = use_case.execute(request)
        
        assert response.success is False
        assert response.ticket_id is None
        assert len(response.errors) > 0
        assert response.has_errors
    
    def test_create_report_with_empty_station_id(self, setup):
        """Error Scenario: Empty station ID should be rejected"""
        use_case, _, _ = setup
        
        with pytest.raises(ValueError, match="Station ID cannot be empty"):
            CreateReportRequest(
                station_id="",
                malfunction_type=MalfunctionType.NOT_CHARGING,
                description="Test"
            )
    
    def test_create_report_with_empty_description(self, setup):
        """Error Scenario: Empty description should be rejected"""
        use_case, _, _ = setup
        
        with pytest.raises(ValueError, match="Description cannot be empty"):
            CreateReportRequest(
                station_id="STATION-001",
                malfunction_type=MalfunctionType.NOT_CHARGING,
                description=""
            )
    
    # ==================== EDGE CASES ====================
    
    def test_create_report_for_already_defective_station(self, setup):
        """Edge Case: Creating report for already defective station"""
        use_case, station_repo, _ = setup
        
        # Mark station as defective first
        station = station_repo.find_by_id(StationId("STATION-001"))
        station.mark_as_defective()
        station_repo.save(station)
        
        # Try to create report
        request = CreateReportRequest(
            station_id="STATION-001",
            malfunction_type=MalfunctionType.NOT_CHARGING,
            description="Reporting already defective station"
        )
        
        response = use_case.execute(request)
        
        assert response.success is False
        assert any("already marked as defective" in error.lower() for error in response.errors)
    
    # ==================== DOMAIN RULES ====================
    
    def test_station_marked_defective_after_report(self, setup):
        """Domain Rule: Station must be marked defective after successful report"""
        use_case, station_repo, _ = setup
        
        # Verify station is operational before
        station_before = station_repo.find_by_id(StationId("STATION-001"))
        assert station_before.is_operational is True
        
        # Create report
        request = CreateReportRequest(
            station_id="STATION-001",
            malfunction_type=MalfunctionType.PAYMENT_FAILURE,
            description="Payment terminal shows error"
        )
        
        response = use_case.execute(request)
        assert response.success is True
        
        # Verify station is now defective
        station_after = station_repo.find_by_id(StationId("STATION-001"))
        assert station_after.is_operational is False
    
    def test_ticket_id_generated_for_valid_report(self, setup):
        """Domain Rule: Valid report must generate a ticket ID"""
        use_case, _, _ = setup
        
        request = CreateReportRequest(
            station_id="STATION-001",
            malfunction_type=MalfunctionType.CONNECTOR_ISSUE,
            description="Connector cable is damaged"
        )
        
        response = use_case.execute(request)
        
        assert response.success is True
        assert response.ticket_id is not None
        assert len(response.ticket_id) > 0