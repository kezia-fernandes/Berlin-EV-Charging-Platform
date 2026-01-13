from contexts.reporting.domain.enums.malfunction_type import MalfunctionType
from contexts.reporting.domain.enums.report_status import ReportStatus


def test_malfunction_type_enum():
    """Test that enum values work"""
    assert MalfunctionType.NOT_CHARGING.value == "not_charging"
    assert MalfunctionType.PAYMENT_FAILURE.value == "payment_failure"


def test_report_status_enum():
    """Test status enum"""
    assert ReportStatus.SUBMITTED.value == "submitted"
    assert ReportStatus.VALIDATED.value == "validated"