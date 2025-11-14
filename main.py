"""
Event ICP Matcher - Main Application

This application uses Linkup API to find event attendees and Claude AI to determine
if they match your company's Ideal Customer Profile.
"""
import os
import json
import argparse
from datetime import datetime
from typing import Optional
from dotenv import load_dotenv

from linkup_client import LinkupClient
from icp_matcher import ICPMatcher

load_dotenv()


class EventICPMatcher:
    """Main application orchestrating event attendee analysis."""

    def __init__(
        self,
        linkup_api_key: Optional[str] = None,
        anthropic_api_key: Optional[str] = None
    ):
        """
        Initialize the Event ICP Matcher.

        Args:
            linkup_api_key: Linkup API key (optional, will use env variable if not provided).
            anthropic_api_key: Anthropic API key (optional, will use env variable if not provided).
        """
        self.linkup = LinkupClient(api_key=linkup_api_key)
        self.icp_matcher = ICPMatcher(api_key=anthropic_api_key)

    def analyze_event(
        self,
        event_name: str,
        event_url: Optional[str] = None,
        company_name: str = "Linkup",
        company_domain: str = "linkup.so",
        use_company_research: bool = True,
        output_file: Optional[str] = None
    ) -> dict:
        """
        Analyze event attendees and match them against company ICP.

        Args:
            event_name: Name of the event to analyze.
            event_url: URL of the event page.
            company_name: Your company name.
            company_domain: Your company domain.
            use_company_research: Whether to research company ICP using Linkup (recommended).
            output_file: Optional file path to save results.

        Returns:
            Dictionary containing the full analysis results.
        """
        print(f"\n{'='*70}")
        print(f"Event ICP Matcher - Analyzing: {event_name}")
        print(f"{'='*70}\n")

        # Step 1: Get company information and ICP
        print(f"[Step 1/3] Researching {company_name}'s ICP...")
        if use_company_research:
            try:
                company_response = self.linkup.get_company_info(
                    company_name=company_name,
                    company_domain=company_domain
                )
                company_info = company_response.get("answer", "")
                print(f"✓ Company research completed ({len(company_info)} characters)")
            except Exception as e:
                print(f"⚠ Warning: Could not fetch company info from Linkup: {e}")
                print("  Falling back to Claude's knowledge...")
                company_info = self.icp_matcher.quick_company_icp_analysis(
                    company_name=company_name,
                    company_domain=company_domain
                )
        else:
            company_info = self.icp_matcher.quick_company_icp_analysis(
                company_name=company_name,
                company_domain=company_domain
            )
            print(f"✓ Company ICP generated using Claude")

        # Step 2: Find event attendees
        print(f"\n[Step 2/3] Searching for attendees of '{event_name}'...")
        try:
            attendee_response = self.linkup.search_event_attendees(
                event_name=event_name,
                event_url=event_url
            )
            attendee_info = attendee_response.get("answer", "")
            attendee_sources = attendee_response.get("sources", [])
            print(f"✓ Found attendee information ({len(attendee_info)} characters)")
            print(f"  Sources used: {len(attendee_sources)}")
        except Exception as e:
            print(f"✗ Error: Could not fetch event attendees: {e}")
            return {
                "error": "Failed to fetch event attendees",
                "details": str(e)
            }

        # Step 3: Analyze ICP matches using Claude
        print(f"\n[Step 3/3] Analyzing ICP matches with Claude AI...")
        analysis_result = self.icp_matcher.analyze_icp_match(
            company_info=company_info,
            attendee_info=attendee_info,
            company_name=company_name
        )

        if "error" in analysis_result:
            print(f"✗ Error during analysis: {analysis_result['error']}")
            return analysis_result

        print(f"✓ Analysis completed successfully\n")

        # Compile full results
        results = {
            "metadata": {
                "event_name": event_name,
                "event_url": event_url,
                "company_name": company_name,
                "company_domain": company_domain,
                "analysis_date": datetime.now().isoformat(),
            },
            "company_icp": company_info,
            "attendee_research": attendee_info,
            "sources": attendee_sources,
            "icp_analysis": analysis_result
        }

        # Display summary
        self._display_summary(analysis_result)

        # Save to file if requested
        if output_file:
            self._save_results(results, output_file)
            print(f"\n✓ Full results saved to: {output_file}")

        return results

    def _display_summary(self, analysis: dict):
        """Display a formatted summary of the analysis."""
        print(f"\n{'='*70}")
        print("ANALYSIS SUMMARY")
        print(f"{'='*70}\n")

        if "summary" in analysis:
            summary = analysis["summary"]
            print(f"Total Attendees Analyzed: {summary.get('total_attendees_analyzed', 0)}")
            print(f"  • High Priority Matches: {summary.get('high_priority_matches', 0)}")
            print(f"  • Medium Priority Matches: {summary.get('medium_priority_matches', 0)}")
            print(f"  • Low Priority Matches: {summary.get('low_priority_matches', 0)}")
            print(f"  • Not a Fit: {summary.get('not_a_fit', 0)}")

        if "overall_event_assessment" in analysis:
            print(f"\nOverall Assessment:")
            print(f"  {analysis['overall_event_assessment']}")

        if "attendees" in analysis and len(analysis["attendees"]) > 0:
            print(f"\n{'='*70}")
            print("TOP PRIORITY MATCHES")
            print(f"{'='*70}\n")

            # Sort by ICP match score
            attendees = sorted(
                analysis["attendees"],
                key=lambda x: x.get("icp_match_score", 0),
                reverse=True
            )

            for i, attendee in enumerate(attendees[:5], 1):  # Show top 5
                print(f"{i}. {attendee.get('name', 'Unknown')} - {attendee.get('role', 'Unknown role')}")
                print(f"   Company: {attendee.get('company', 'Unknown')}")
                print(f"   ICP Score: {attendee.get('icp_match_score', 0)}/10 ({attendee.get('opportunity_type', 'Unknown')})")
                print(f"   Action: {attendee.get('recommended_action', 'N/A')}")

                talking_points = attendee.get('key_talking_points', [])
                if talking_points:
                    print(f"   Key Points: {', '.join(talking_points[:2])}")
                print()

        if "recommendations" in analysis:
            print(f"{'='*70}")
            print("RECOMMENDATIONS")
            print(f"{'='*70}\n")
            for i, rec in enumerate(analysis["recommendations"], 1):
                print(f"{i}. {rec}")

        print(f"\n{'='*70}\n")

    def _save_results(self, results: dict, output_file: str):
        """Save results to a JSON file."""
        os.makedirs(os.path.dirname(output_file) or ".", exist_ok=True)
        with open(output_file, "w") as f:
            json.dump(results, f, indent=2)


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Analyze event attendees and match them against your company's ICP using Linkup and Claude AI."
    )
    parser.add_argument(
        "event_name",
        type=str,
        help="Name of the event to analyze"
    )
    parser.add_argument(
        "--event-url",
        type=str,
        help="URL of the event page (recommended for better results)"
    )
    parser.add_argument(
        "--company-name",
        type=str,
        default=os.getenv("COMPANY_NAME", "Linkup"),
        help="Your company name (default: Linkup or from COMPANY_NAME env variable)"
    )
    parser.add_argument(
        "--company-domain",
        type=str,
        default=os.getenv("COMPANY_DOMAIN", "linkup.so"),
        help="Your company domain (default: linkup.so or from COMPANY_DOMAIN env variable)"
    )
    parser.add_argument(
        "--no-company-research",
        action="store_true",
        help="Skip researching company ICP via Linkup and use Claude's knowledge instead"
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Output file path for saving results (JSON format)"
    )

    args = parser.parse_args()

    try:
        matcher = EventICPMatcher()
        results = matcher.analyze_event(
            event_name=args.event_name,
            event_url=args.event_url,
            company_name=args.company_name,
            company_domain=args.company_domain,
            use_company_research=not args.no_company_research,
            output_file=args.output
        )

        # Return appropriate exit code
        if "error" in results:
            return 1
        return 0

    except Exception as e:
        print(f"\n✗ Fatal error: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
