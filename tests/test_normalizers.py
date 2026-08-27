"""
Unit tests for date and timestamp normalizers.
Author: Muhammad Awais (AI Meeting Intelligence)
"""

from src.ai_intelligence.normalizers import (
    format_seconds_to_timestamp,
    normalize_deadline,
    parse_reference_date
)


def test_format_seconds_to_timestamp():
    assert format_seconds_to_timestamp(0) == "00:00"
    assert format_seconds_to_timestamp(59) == "00:59"
    assert format_seconds_to_timestamp(135.2) == "02:15"
    assert format_seconds_to_timestamp(3600) == "01:00:00"
    assert format_seconds_to_timestamp(3725.8) == "01:02:06"


def test_normalize_deadline_relative_keywords():
    # Base reference date: Friday, August 28, 2026
    ref_date = "2026-08-28"

    assert normalize_deadline("today", ref_date) == "2026-08-28"
    assert normalize_deadline("tomorrow", ref_date) == "2026-08-29"
    assert normalize_deadline("day after tomorrow", ref_date) == "2026-08-30"


def test_normalize_deadline_weekdays():
    # 2026-08-28 is a Friday
    ref_date = "2026-08-28"

    # Next Monday should be 2026-08-31
    assert normalize_deadline("next Monday", ref_date) == "2026-08-31"

    # Friday (same day or next week)
    res_fri = normalize_deadline("by Friday", ref_date)
    assert res_fri is not None

    # Wednesday should be next Wednesday: 2026-09-02
    assert normalize_deadline("Wednesday", ref_date) == "2026-09-02"


def test_normalize_deadline_calendar_dates():
    ref_date = "2026-08-28"

    # Exact calendar date mentioned in PDF requirements: "September 10"
    assert normalize_deadline("September 10", ref_date) == "2026-09-10"
    assert normalize_deadline("Sept 10", ref_date) == "2026-09-10"


def test_normalize_deadline_end_of_month():
    ref_date = "2026-08-28"
    # August has 31 days
    assert normalize_deadline("end of this month", ref_date) == "2026-08-31"


def test_normalize_deadline_in_x_days():
    ref_date = "2026-08-28"
    assert normalize_deadline("in 2 days", ref_date) == "2026-08-30"
    assert normalize_deadline("in a week", ref_date) == "2026-09-04"
