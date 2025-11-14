"""
Example usage scripts for the Event ICP Matcher.

These examples demonstrate different ways to use the tool programmatically.
"""
import sys
import os

# Add parent directory to path to import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import EventICPMatcher
from linkup_client import LinkupClient
from icp_matcher import ICPMatcher


def example_1_basic_analysis():
    """
    Example 1: Basic event analysis with default settings (Linkup as company).
    """
    print("="*70)
    print("EXAMPLE 1: Basic Event Analysis")
    print("="*70 + "\n")

    matcher = EventICPMatcher()

    results = matcher.analyze_event(
        event_name="AI Agents Hackathon NYC 2025",
        event_url="https://partful.com/e/ai-agents-hackathon",
        output_file="examples/output/example1_results.json"
    )

    # Print high-priority matches
    if "icp_analysis" in results and "attendees" in results["icp_analysis"]:
        high_priority = [
            a for a in results["icp_analysis"]["attendees"]
            if a.get("opportunity_type") == "High Priority"
        ]
        print(f"\nFound {len(high_priority)} high-priority matches!")


def example_2_custom_company():
    """
    Example 2: Analyze event for a custom company.
    """
    print("\n" + "="*70)
    print("EXAMPLE 2: Custom Company Analysis")
    print("="*70 + "\n")

    matcher = EventICPMatcher()

    results = matcher.analyze_event(
        event_name="SaaS Founder Summit 2025",
        event_url="https://example.com/saas-summit",  # Replace with real URL
        company_name="Acme Analytics",
        company_domain="acme-analytics.com",  # Replace with real domain
        output_file="examples/output/example2_results.json"
    )

    return results


def example_3_multiple_events():
    """
    Example 3: Analyze multiple events and compare ICP fit.
    """
    print("\n" + "="*70)
    print("EXAMPLE 3: Multi-Event Comparison")
    print("="*70 + "\n")

    matcher = EventICPMatcher()

    events = [
        {
            "name": "TechCrunch Disrupt 2025",
            "url": "https://techcrunch.com/events/disrupt-2025/"
        },
        {
            "name": "Web Summit 2025",
            "url": "https://websummit.com"
        },
        {
            "name": "AI Engineering Summit",
            "url": None  # Can work without URL too
        }
    ]

    event_scores = []

    for event in events:
        print(f"\nAnalyzing: {event['name']}")
        print("-" * 70)

        results = matcher.analyze_event(
            event_name=event["name"],
            event_url=event["url"],
            company_name="Linkup",
            company_domain="linkup.so"
        )

        if "icp_analysis" in results and "summary" in results["icp_analysis"]:
            summary = results["icp_analysis"]["summary"]
            high_priority = summary.get("high_priority_matches", 0)
            total = summary.get("total_attendees_analyzed", 0)

            event_scores.append({
                "event": event["name"],
                "high_priority_count": high_priority,
                "total_attendees": total,
                "score": high_priority / max(total, 1)  # Avoid division by zero
            })

    # Sort events by ICP fit score
    event_scores.sort(key=lambda x: x["score"], reverse=True)

    print("\n" + "="*70)
    print("EVENT COMPARISON RESULTS")
    print("="*70 + "\n")

    for i, event in enumerate(event_scores, 1):
        print(f"{i}. {event['event']}")
        print(f"   High Priority Matches: {event['high_priority_count']}/{event['total_attendees']}")
        print(f"   ICP Fit Score: {event['score']:.1%}\n")


def example_4_custom_icp_analysis():
    """
    Example 4: Use just the ICP matcher with custom data.
    """
    print("\n" + "="*70)
    print("EXAMPLE 4: Custom ICP Analysis")
    print("="*70 + "\n")

    matcher = ICPMatcher()

    # Define your company's ICP
    company_icp = """
    Linkup is a deep search API that provides precise, structured data for AI applications.

    Ideal Customer Profile:
    - Companies building AI agents, chatbots, or LLM applications
    - Need reliable, real-time data to ground AI responses
    - Tech-forward companies (AI startups, SaaS companies, enterprises with AI initiatives)
    - Company size: Primarily Series A+ startups and mid-market companies
    - Decision makers: CTOs, VP Engineering, AI/ML team leads, Product Managers
    - Budget: $500+/month for API services

    Key Pain Points:
    - AI hallucination and unreliable outputs
    - Need for real-time, accurate data
    - Integration complexity with traditional search APIs
    - Structured output requirements

    Value Proposition:
    - Precise search optimized for AI/LLM use cases
    - Structured output with schema definition
    - Deep search for comprehensive results
    - Easy API integration
    """

    # Sample attendee data (you could get this from anywhere)
    attendee_data = """
    Event Attendees found:

    1. Jane Smith - CTO at AI Startup Inc
       - Building conversational AI platform
       - Looking for reliable data sources
       - LinkedIn: linkedin.com/in/janesmith

    2. Bob Johnson - Marketing Manager at Traditional Corp
       - Focus on digital advertising
       - Not involved in AI/ML projects

    3. Dr. Alice Chen - Director of AI Research at TechGiant
       - Leading team of 50 ML engineers
       - Working on enterprise AI assistants
       - Published papers on grounded generation
       - Twitter: @alicechen
    """

    # Analyze ICP match
    analysis = matcher.analyze_icp_match(
        company_info=company_icp,
        attendee_info=attendee_data,
        company_name="Linkup"
    )

    # Display results
    if "attendees" in analysis:
        print("\nICP Match Analysis:")
        for attendee in analysis["attendees"]:
            print(f"\n• {attendee['name']} ({attendee['company']})")
            print(f"  Score: {attendee['icp_match_score']}/10")
            print(f"  Priority: {attendee['opportunity_type']}")
            print(f"  Action: {attendee['recommended_action']}")


def example_5_linkup_client_only():
    """
    Example 5: Use Linkup client directly for custom searches.
    """
    print("\n" + "="*70)
    print("EXAMPLE 5: Direct Linkup Client Usage")
    print("="*70 + "\n")

    client = LinkupClient()

    # Search for company information
    print("Searching for Anthropic's ICP...")
    result = client.get_company_info(
        company_name="Anthropic",
        company_domain="anthropic.com"
    )

    print("\nCompany Info:")
    print(result.get("answer", "No answer found")[:500] + "...")

    print("\n\nSources used:")
    for i, source in enumerate(result.get("sources", [])[:3], 1):
        print(f"{i}. {source.get('name', 'Unknown')}")
        print(f"   URL: {source.get('url', 'N/A')}")

    # Search for event attendees
    print("\n" + "-"*70)
    print("Searching for TechCrunch Disrupt attendees...")
    attendees = client.search_event_attendees(
        event_name="TechCrunch Disrupt 2025",
        event_url="https://techcrunch.com/events/disrupt-2025/"
    )

    print("\nAttendee Info:")
    print(attendees.get("answer", "No answer found")[:500] + "...")


def example_6_structured_output():
    """
    Example 6: Using Linkup's structured output for custom schemas.
    """
    print("\n" + "="*70)
    print("EXAMPLE 6: Structured Output")
    print("="*70 + "\n")

    client = LinkupClient()

    # Define a custom schema for attendee data
    schema = {
        "type": "object",
        "properties": {
            "attendees": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "role": {"type": "string"},
                        "company": {"type": "string"},
                        "linkedin_url": {"type": "string"}
                    }
                }
            },
            "total_count": {"type": "number"}
        }
    }

    result = client.search(
        query="Find speakers at TechCrunch Disrupt 2025. List their names, roles, companies, and LinkedIn URLs.",
        depth="deep",
        output_type="structured",
        structured_output_schema=schema,
        include_sources=True
    )

    print("Structured attendee data:")
    print(result)


def main():
    """
    Run examples.

    Uncomment the examples you want to run.
    """
    # Create output directory
    os.makedirs("examples/output", exist_ok=True)

    # Run examples (uncomment the ones you want to try)

    # example_1_basic_analysis()
    # example_2_custom_company()
    # example_3_multiple_events()
    example_4_custom_icp_analysis()
    # example_5_linkup_client_only()
    # example_6_structured_output()

    print("\n" + "="*70)
    print("Examples completed!")
    print("="*70)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\nError running examples: {e}")
        print("\nMake sure you have set up your .env file with API keys!")
        sys.exit(1)
