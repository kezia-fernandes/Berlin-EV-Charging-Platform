import pytest
from uuid import uuid4
from contexts.reporting.domain.entities.malfunction_report import MalfunctionReport
from contexts.shared_kernel.common.station_id import StationId
from contexts.reporting.domain.value_objects.report_description import ReportDescription
from contexts.reporting.domain.enums.malfunction_type import MalfunctionType
from contexts.reporting.domain.enums.report_status import ReportStatus


def test_create_malfunction_report():
    """Test creating a basic malfunction report"""
    report_id = uuid4()
    station_id = StationId("STATION-001")
    description = ReportDescription("Payment terminal not working properly")
    
    report = MalfunctionReport(
        report_id=report_id,
        station_id=station_id,
        malfunction_type=MalfunctionType.PAYMENT_FAILURE,
        description=description
    )
    
    assert report.report_id == report_id
    assert report.station_id == station_id
    assert report.status == ReportStatus.SUBMITTED
    assert report.ticket_id is None


def test_validate_report_with_existing_station():
    """Test validating a report when station exists"""
    report = MalfunctionReport(
        report_id=uuid4(),
        station_id=StationId("STATION-001"),
        malfunction_type=MalfunctionType.NOT_CHARGING,
        description=ReportDescription("Vehicle not charging at all")
    )
    
    is_valid = report.validate(station_exists=True, station_is_operational=True)
    
    assert is_valid is True
    assert report.status == ReportStatus.VALIDATED