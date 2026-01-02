#!/bin/bash
# Complete script to populate ALL reporting context files
# Run from: /mnt/d/Advanced_Software/Berlin-EV-Charging-Platform

cd /mnt/d/Advanced_Software/Berlin-EV-Charging-Platform

echo "🚀 Populating Complete Reporting Context..."

# ============================================================================
# COMPLETE THE MALFUNCTION SERVICE TEST
# ============================================================================

cat > contexts/reporting/tests/domain/test_malfunction_service.py << 'EOF'
import pytest
from uuid import uuid4
from contexts.reporting.domain.services.malfunction_report_service import MalfunctionReportService
from contexts.reporting.domain.entities.operational_station import OperationalStation
from contexts.reporting.domain.value_objects.station_id import StationId
from contexts.reporting.domain.enums.malfunction_type import MalfunctionType
from contexts.reporting.domain.enums.station_status import StationStatus
from contexts.reporting.infrastructure.repositories.in_memory_station_repository import (
    InMemoryStationRepository
)
from contexts.reporting.infrastructure.repositories.in_memory_report_repository import (
    InMemoryReportRepository
)


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
    
    def test_submit_report_with_invalid_description_raises_error(self, service):
        """Test that invalid description raises validation error"""
        with pytest.raises(ValueError, match="too short"):
            service.submit_malfunction_report(
                station_id="STATION-001",
                malfunction_type=MalfunctionType.NOT_CHARGING,
                description="Bad",
                reported_by=None
            )
    
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
    
    def test_process_report_for_nonexistent_station_fails(self, service):
        """Test that processing report for non-existent station fails validation"""
        report_id = service.submit_malfunction_report(
            station_id="NONEXISTENT",
            malfunction_type=MalfunctionType.NOT_CHARGING,
            description="Station does not exist in system"
        )
        
        result = service.process_malfunction_report(report_id)
        
        assert result.success is False
        assert "does not exist" in result.errors[0]
        assert result.ticket_id is None
    
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
EOF

# ============================================================================
# INFRASTRUCTURE TESTS
# ============================================================================

cat > contexts/reporting/tests/infrastructure/test_repositories.py << 'EOF'
import pytest
from uuid import uuid4
from contexts.reporting.domain.entities.operational_station import OperationalStation
from contexts.reporting.domain.entities.malfunction_report import MalfunctionReport
from contexts.reporting.domain.value_objects.station_id import StationId
from contexts.reporting.domain.value_objects.report_description import ReportDescription
from contexts.reporting.domain.enums.malfunction_type import MalfunctionType
from contexts.reporting.infrastructure.repositories.in_memory_station_repository import (
    InMemoryStationRepository
)
from contexts.reporting.infrastructure.repositories.in_memory_report_repository import (
    InMemoryReportRepository
)


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
            description=ReportDescription("First report")
        )
        report2 = MalfunctionReport(
            report_id=uuid4(),
            station_id=station_id,
            malfunction_type=MalfunctionType.PAYMENT_FAILURE,
            description=ReportDescription("Second report")
        )
        
        repository.save(report1)
        repository.save(report2)
        
        station_reports = repository.find_by_station(station_id)
        
        assert len(station_reports) == 2
EOF

# ============================================================================
# UPDATE TEST_ENUMS.PY (FIX THE ENUM VALUE)
# ============================================================================

cat > contexts/reporting/tests/domain/test_enums.py << 'EOF'
import pytest
from contexts.reporting.domain.enums.malfunction_type import MalfunctionType
from contexts.reporting.domain.enums.report_status import ReportStatus


def test_malfunction_type_enum():
    """Test that enum values work"""
    assert MalfunctionType.NOT_CHARGING.value == "not_charging"


def test_report_status_enum():
    """Test status enum"""
    assert ReportStatus.SUBMITTED.value == "submitted"
EOF

echo "✅ All Reporting Context files created successfully!"
echo ""
echo "📊 Summary:"
echo "  ✓ Domain Layer: Value Objects, Enums, Entities, Repositories, Services"
echo "  ✓ Infrastructure Layer: In-Memory Repositories"
echo "  ✓ Tests: 5 complete test files"
echo ""
echo "🧪 Now run: pytest contexts/reporting/tests -v"
