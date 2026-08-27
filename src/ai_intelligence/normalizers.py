"""
Date and timestamp normalization utilities for AI Meeting Intelligence.
Author: Muhammad Awais (AI Meeting Intelligence)

Transforms:
- Timestamp seconds to human-readable strings (e.g. 135.2 -> "02:15")
- Natural language deadlines into ISO 8601 standardized dates (YYYY-MM-DD)
  Examples: "tomorrow", "Friday", "next Monday", "September 10", "end of this month"
"""

import calendar
import re
from datetime import datetime, date, timedelta
from typing import Optional, Tuple
from dateutil import parser as date_parser
from dateutil.relativedelta import relativedelta, MO, TU, WE, TH, FR, SA, SU

WEEKDAYS = {
    "monday": 0,
    "tuesday": 1,
    "wednesday": 2,
    "thursday": 3,
    "friday": 4,
    "saturday": 5,
    "sunday": 6,
}


def format_seconds_to_timestamp(seconds: float) -> str:
    """
    Format a floating-point seconds value into HH:MM:SS or MM:SS string.
    Example:
        135.2 -> "02:15"
        3725.0 -> "01:02:05"
    """
    if seconds is None or seconds < 0:
        return "00:00"
    
    total_seconds = int(round(seconds))
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    secs = total_seconds % 60

    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"


def format_duration_human(seconds: float) -> str:
    """
    Format seconds into a human-friendly duration string for dashboard cards.
    Examples:
        75.0 -> "1m 15s"
        1845.0 -> "30m 45s"
        3665.0 -> "1h 01m 05s"
    """
    if seconds is None or seconds < 0:
        return "0s"
    total_seconds = int(round(seconds))
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    secs = total_seconds % 60

    if hours > 0:
        return f"{hours}h {minutes:02d}m {secs:02d}s" if secs > 0 else f"{hours}h {minutes:02d}m"
    if minutes > 0:
        return f"{minutes}m {secs:02d}s"
    return f"{secs}s"


def parse_reference_date(ref_date_input: Optional[str] = None) -> date:
    """
    Parses an ISO date string or falls back to today's date.
    """
    if not ref_date_input:
        return date.today()
    try:
        if "T" in ref_date_input:
            return datetime.fromisoformat(ref_date_input.replace("Z", "+00:00")).date()
        return datetime.strptime(ref_date_input[:10], "%Y-%m-%d").date()
    except Exception:
        try:
            return date_parser.parse(ref_date_input).date()
        except Exception:
            return date.today()


def normalize_deadline(raw_text: Optional[str], reference_date_str: Optional[str] = None) -> Optional[str]:
    """
    Normalize natural language deadline expressions into standard 'YYYY-MM-DD' strings.
    Handles phrases mentioned in project requirements:
    - 'tomorrow', 'tomorrow morning', 'by tomorrow at 5pm'
    - 'today', 'tonight', 'tonight at 11 PM'
    - 'Friday', 'next Monday', 'next Monday morning', 'this Wednesday'
    - 'September 10', '10 September'
    - 'end of this month', 'end of next month'
    - 'end of this week', 'end of the week'
    - 'in 2 days', 'in 3 weeks'
    """
    if not raw_text or not isinstance(raw_text, str):
        return None

    cleaned = raw_text.strip().lower()
    cleaned = re.sub(r"^(by|on|at|before|due)\s+", "", cleaned).strip()

    # Strip trailing time designations (e.g. "at 11 pm", "at 5:00", "morning", "evening")
    cleaned_date = re.sub(r"\s+(at|by)\s+\d{1,2}(:\d{2})?\s*(am|pm)?.*$", "", cleaned).strip()
    cleaned_date = re.sub(r"\s+(morning|afternoon|evening|night|eod|cob|close of business)$", "", cleaned_date).strip()

    ref_date = parse_reference_date(reference_date_str)

    # 1. Direct Relative Keywords
    if cleaned_date in ("today", "tonight", "end of day", "eod"):
        return ref_date.isoformat()
    if cleaned_date in ("tomorrow", "tmrw"):
        return (ref_date + timedelta(days=1)).isoformat()
    if cleaned_date in ("day after tomorrow",):
        return (ref_date + timedelta(days=2)).isoformat()

    # 2. "In X days/weeks/months"
    in_pattern = re.match(r"in\s+(\d+|a|an|one|two|three|four|five)\s+(day|days|week|weeks|month|months)", cleaned_date)
    if in_pattern:
        num_word = in_pattern.group(1)
        unit = in_pattern.group(2)
        word_to_num = {"a": 1, "an": 1, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5}
        count = int(num_word) if num_word.isdigit() else word_to_num.get(num_word, 1)

        if "day" in unit:
            return (ref_date + timedelta(days=count)).isoformat()
        elif "week" in unit:
            return (ref_date + timedelta(weeks=count)).isoformat()
        elif "month" in unit:
            return (ref_date + relativedelta(months=count)).isoformat()

    # 3. "End of this month" / "End of next month"
    if "end of this month" in cleaned_date or "end of month" in cleaned_date:
        last_day = calendar.monthrange(ref_date.year, ref_date.month)[1]
        return date(ref_date.year, ref_date.month, last_day).isoformat()

    if "end of next month" in cleaned_date:
        next_month_date = ref_date + relativedelta(months=1)
        last_day = calendar.monthrange(next_month_date.year, next_month_date.month)[1]
        return date(next_month_date.year, next_month_date.month, last_day).isoformat()

    # "End of this week" / "End of the week" (target coming Friday or Sunday)
    if "end of this week" in cleaned_date or "end of the week" in cleaned_date or "end of week" in cleaned_date:
        current_day = ref_date.weekday()
        days_to_friday = (4 - current_day) if current_day <= 4 else (4 - current_day + 7)
        return (ref_date + timedelta(days=days_to_friday)).isoformat()

    # 4. Weekdays (e.g., "Friday", "next Monday", "this Friday")
    for day_name, day_index in WEEKDAYS.items():
        if day_name in cleaned_date:
            is_next = "next" in cleaned_date
            current_day_index = ref_date.weekday()

            if day_index > current_day_index:
                # Day hasn't occurred yet in the current calendar week
                days_ahead = day_index - current_day_index
                if is_next:
                    days_ahead += 7
            else:
                # Day already occurred or is today; earliest next occurrence is in the coming week
                days_ahead = (day_index - current_day_index) + 7

            return (ref_date + timedelta(days=days_ahead)).isoformat()

    # 5. Explicit Calendar Dates (e.g. "September 10", "10 September", "2026-09-01", "Sept 10th")
    try:
        parsed = date_parser.parse(cleaned_date, default=datetime(ref_date.year, 1, 1))
        # If no year was in the string and parsed date is in the past, roll forward 1 year
        if not re.search(r"\b(19|20)\d{2}\b", cleaned_date) and parsed.date() < ref_date:
            parsed = parsed.replace(year=ref_date.year + 1)
        return parsed.date().isoformat()
    except (ValueError, OverflowError):
        pass

    return None
