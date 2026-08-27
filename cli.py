"""
CLI Tool for AI Meeting Intelligence.
Author: Muhammad Awais (AI Meeting Intelligence)

Usage:
    python cli.py --input tests/fixtures/sample_taskeen_transcript.json --provider mock --output report.json
"""

import argparse
import json
import sys
from pathlib import Path
from dotenv import load_dotenv

# Ensure local src is in sys.path
sys.path.insert(0, str(Path(__file__).parent))

from src.ai_intelligence.service import MeetingIntelligenceService


def main():
    load_dotenv()

    parser = argparse.ArgumentParser(
        description="AI Meeting Intelligence - Analyze meeting transcripts and extract structured insights."
    )
    parser.add_argument(
        "--input", "-i",
        required=True,
        help="Path to input transcript JSON file matching Taskeen's format"
    )
    parser.add_argument(
        "--provider", "-p",
        default="mock",
        choices=["mock", "gemini", "openai"],
        help="LLM provider to use (default: mock)"
    )
    parser.add_argument(
        "--model", "-m",
        default=None,
        help="Model name override (e.g., gemini-1.5-flash or gpt-4o-mini)"
    )
    parser.add_argument(
        "--summary-type", "-s",
        default="both",
        choices=["short", "detailed", "both"],
        help="Summary depth requested (default: both)"
    )
    parser.add_argument(
        "--output", "-o",
        default=None,
        help="Path to save output JSON report (if omitted, prints summary to terminal)"
    )

    args = parser.parse_args()

    input_file = Path(args.input)
    if not input_file.exists():
        print(f"Error: Input file '{args.input}' not found.", file=sys.stderr)
        sys.exit(1)

    with open(input_file, "r", encoding="utf-8") as f:
        transcript_data = json.load(f)

    if args.summary_type:
        transcript_data["summary_type"] = args.summary_type

    print(f"[*] Initializing AI Meeting Intelligence Service (Provider: {args.provider})...")
    service = MeetingIntelligenceService(
        provider_type=args.provider,
        model_name=args.model
    )

    print(f"[*] Analyzing '{input_file.name}' ({len(transcript_data.get('segments', []))} segments)...")
    report = service.analyze_meeting_sync(transcript_data)

    print("\n" + "=" * 60)
    print(f"  AI MEETING INTELLIGENCE REPORT: {report.title}")
    print("=" * 60)
    print(f"\n[Executive Summary]\n{report.summary.executive_summary}\n")

    print(f"[Participants ({len(report.participants)})]")
    for p in report.participants:
        name_str = f" ({p.detected_name})" if p.detected_name else ""
        print(f" - {p.speaker_id}{name_str}: {p.spoken_seconds}s ({p.contribution_percentage}% contribution, {p.turn_count} turns)")

    print(f"\n[Decisions Made ({len(report.decisions)})]")
    for d in report.decisions:
        ts = f" [{d.timestamp.formatted}]" if d.timestamp else ""
        print(f" - {d.decision}{ts}")
        if d.rationale:
            print(f"   Rationale: {d.rationale}")

    print(f"\n[Action Items ({len(report.action_items)})]")
    for a in report.action_items:
        ts = f" [{a.timestamp.formatted}]" if a.timestamp else ""
        dl = f" | Deadline: {a.deadline_raw} -> {a.deadline_normalized}" if a.deadline_raw else ""
        print(f" - [{a.priority.upper()}] {a.task} (Owner: {a.assigned_to}{dl}){ts}")

    print(f"\n[Sentiment Analysis]")
    print(f" - Overall: {report.sentiment.overall_sentiment.value.upper()} (Score: {report.sentiment.score:+0.2f})")
    print(f" - Tone: {report.sentiment.tone_summary}")

    print(f"\n[Processing Metadata]")
    print(f" - Duration: {report.metadata.total_duration_seconds}s | Model: {report.metadata.model_name} | Elapsed: {report.metadata.processing_time_seconds}s")
    print("=" * 60)

    if args.output:
        out_path = Path(args.output)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(report.model_dump_json(indent=2))
        print(f"\n[+] Full structured JSON report saved to: {out_path.resolve()}\n")


if __name__ == "__main__":
    main()
