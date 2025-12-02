"""
Flask web application for Event ICP Matcher.
"""
import os
import json
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv

from linkup_client import LinkupClient
from icp_matcher_openai import ICPMatcher

load_dotenv()

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

# Initialize clients
linkup_client = None
icp_matcher = None

try:
    linkup_client = LinkupClient()
    icp_matcher = ICPMatcher()
except Exception as e:
    print(f"Warning: Could not initialize clients: {e}")
    print("Make sure API keys are set in .env file")

# Hardcoded speakers for AI Summit NY to skip Linkup scraping
AI_SUMMIT_NY_SPEAKERS = [
    {"name": "Aarohi Tripathi", "title": "Senior Data Engineer", "company": "Technology in Healthcare Services"},
    {"name": "Aaron Rajan", "title": "Chief Digital Information Officer & Global VP", "company": "Unilever"},
    {"name": "Abhishek Sinha", "title": "Senior Director - Head of COE (AI & Visualization)", "company": "Sage Therapeutics"},
    {"name": "Aditya Mulik", "title": "Software Engineer", "company": "Walmart Global Tech"},
    {"name": "Adrian Crockett", "title": "General Partner & Head of EJ Labs", "company": "Edward Jones"},
    {"name": "Aeshna Kapoor", "title": "Data Scientist", "company": "Technology in Financial Services"},
    {"name": "Agus Sudjianto", "title": "Executive in Residence, Center for Trustworthy AI", "company": "University of North Carolina at Charlotte"},
    {"name": "Alessio Alionço", "title": "CEO/Founder", "company": "Pipefy"},
    {"name": "Alex Tsankov", "title": "MLOps Engineer", "company": "Bloomberg"},
    {"name": "Alexandre Girault", "title": "Head of AI/Innovation & Head of Data North America", "company": "Lacoste"},
    {"name": "Ali Mahmoud", "title": "Principal", "company": "Glasswing Ventures"},
    {"name": "Aliza Carpio", "title": "Senior Director, Technical Product Management", "company": "JLL"},
    {"name": "Amanda Martin", "title": "Senior Developer Advocate", "company": "Apollo GraphQL"},
    {"name": "Amit Chita", "title": "Field CTO", "company": "Mend.io"},
    {"name": "Amy Auton-Smith", "title": "NY Technology Investment Lead", "company": "British Consulate General NY"},
    {"name": "Ananya Upadhyay", "title": "AI Developer", "company": "United Rentals, Inc."},
    {"name": "Andrea Hippeau", "title": "Partner", "company": "Lerer Hippeau"},
    {"name": "Andreas Welsch", "title": "Founder & Chief AI Strategist", "company": "Intelligence Briefing"},
    {"name": "Andres Andreu", "title": "Chief Executive Officer", "company": "Constella Intelligence"},
    {"name": "Andrew Bostjancic", "title": "Senior Business Development Manager", "company": "Taylor & Francis"},
    {"name": "Andrew Culhane", "title": "Chief Commercial Officer", "company": "Torc Robotics"},
    {"name": "Andy Maskin", "title": "Director, AI Creative Technology", "company": "Publicis Sapient"},
    {"name": "Andy Pidcock", "title": "Head of Post-Production", "company": "Malka a part of Gen Digital"},
    {"name": "Angella Tape", "title": "SVP Group Strategy Director", "company": "Havas"},
    {"name": "Anne Josephine Flanagan", "title": "Co-Founder and CSO", "company": "Boyd Strategy Group"},
    {"name": "Anne-Claire Baschet", "title": "Chief Data & AI Officer", "company": "Mirakl"},
    {"name": "Anshu Sharma", "title": "Co-founder and CEO", "company": "Skyflow"},
    {"name": "Anthony Scarola", "title": "CISO", "company": "Apple Bank"},
    {"name": "Antonio Ortiz Barranon", "title": "Professor", "company": "Tecnologico de Monterrey"},
    {"name": "Anuradha Maradapu", "title": "Manager, Data Governance Office", "company": "American Airlines"},
    {"name": "Anusha Dandapani", "title": "Chief, AI Hub", "company": "United Nations International Computing Centre (UNICC)"},
    {"name": "Apostol Vassilev", "title": "Research Team Supervisor", "company": "National Institute of Standards and Technology (NIST)"},
    {"name": "Arjun Ramakrishnan", "title": "Principal Security Architect - AI Security", "company": "Mastercard"},
    {"name": "Arpit Narain", "title": "Global Head of Financial Solutions", "company": "Mathworks"},
    {"name": "Arthur O'Connor", "title": "Academic Director", "company": "CUNY"},
    {"name": "Aruna Rawat", "title": "CISO", "company": "Pureinsurance- A Tokio Marine Company"},
    {"name": "Arvind Balasundaram", "title": "Executive Director, Commercial Insights & Analytics", "company": "Regeneron Pharmaceuticals"},
    {"name": "Asha Saxena", "title": "CEO & Founder", "company": "World Leaders in Data & AI (WLDA)"},
    {"name": "Ashish Gupta", "title": "Senior Vice President and Head of Data & AI", "company": "Incedo"},
    {"name": "Ashlyn Lackey", "title": "Director, Emerging Technology", "company": "Prudential"},
    {"name": "Audi Rowe", "title": "Americas Consulting Transformation Leader", "company": "EY"},
    {"name": "Axel Threlfall", "title": "Editor at Large", "company": "Reuters"},
    {"name": "Aydin Mirzaee", "title": "CEO", "company": "Fellow.ai"},
    {"name": "Barry McCardel", "title": "Founder and CEO", "company": "Hex"},
    {"name": "Benjamin Kummer", "title": "Director of Clinical Informatics in Neurology", "company": "Icahn School of Medicine at Mount Sinai"},
    {"name": "Benjamin Sherman", "title": "Security Expert", "company": "Fortinet"},
    {"name": "Beth Porter", "title": "Head of Studio Operations", "company": "C10 Labs"},
    {"name": "Beth Roth", "title": "Senior Manager, Product Design", "company": "Capital One"},
    {"name": "Bhavesh Mehta", "title": "Senior Manager", "company": "Uber"},
    {"name": "Bhumika Shah", "title": "Data Solution Engineer, PhD Scholar", "company": "University of the Cumberlands"},
]

# URL patterns that use hardcoded data
HARDCODED_EVENT_URLS = {
    "newyork.theaisummit.com": AI_SUMMIT_NY_SPEAKERS,
    "theaisummit.com/conference-speakers": AI_SUMMIT_NY_SPEAKERS,
}


def convert_speakers_to_table(speakers: list) -> str:
    """Convert enriched speakers list to markdown table for ICP matching."""
    lines = ["| Name | Role/Title | Company | Background |"]
    lines.append("|------|-----------|---------|------------|")

    for s in speakers:
        name = s.get("name", "N/A")
        title = s.get("title", "N/A")
        company = s.get("company", "N/A")

        # Extract enrichment info from search results
        enrichment_text = ""
        enrichment_results = s.get("enrichment", [])
        if enrichment_results:
            # Combine snippets/content from search results
            snippets = []
            for result in enrichment_results[:3]:  # Take top 3 results
                if isinstance(result, dict):
                    snippet = result.get("content") or result.get("snippet") or result.get("description", "")
                    if snippet:
                        # Truncate long snippets
                        snippet = snippet[:300] + "..." if len(snippet) > 300 else snippet
                        snippets.append(snippet)
            enrichment_text = " | ".join(snippets) if snippets else ""

        # Also include bio if available from structured extraction
        bio = s.get("bio", "")
        if bio and not enrichment_text:
            enrichment_text = bio[:300] + "..." if len(bio) > 300 else bio

        # Clean up for markdown table (escape pipes)
        enrichment_text = enrichment_text.replace("|", "-").replace("\n", " ")

        lines.append(f"| {name} | {title} | {company} | {enrichment_text} |")

    return "\n".join(lines)


@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')


@app.route('/api/analyze', methods=['POST'])
def analyze_event():
    """
    API endpoint to analyze an event using the new 4-step workflow.

    Expected JSON body:
    {
        "event_url": "https://...",  (required)
        "company_url": "https://...",  (required)
        "company_name": "Company"  (optional, defaults to "your company")
    }
    """
    if not linkup_client or not icp_matcher:
        return jsonify({
            "error": "API clients not initialized. Please check your API keys in .env file."
        }), 500

    try:
        data = request.get_json()

        # Validate required fields
        if not data.get('event_url'):
            return jsonify({"error": "event_url is required"}), 400

        if not data.get('company_url'):
            return jsonify({"error": "company_url is required"}), 400

        event_url = data['event_url']
        company_url = data['company_url']
        company_name = data.get('company_name', 'your company')

        # Step 1: Extract speakers from event URL
        # Check for hardcoded URLs first to skip Linkup API call
        speakers = None
        attendee_sources = []
        use_hardcoded = False

        for url_pattern, hardcoded_speakers in HARDCODED_EVENT_URLS.items():
            if url_pattern in event_url:
                print(f"Step 1: Using hardcoded speakers for {url_pattern} (skipping Linkup)")
                speakers = hardcoded_speakers
                use_hardcoded = True
                break

        if not use_hardcoded:
            # Use Linkup API to extract speakers
            print(f"Step 1: Extracting speakers from {event_url}...")
            try:
                speakers_response = linkup_client.extract_speakers_structured(event_url)

                # Handle structured output response - Linkup returns speakers directly at root level
                # Try multiple possible response formats
                if "speakers" in speakers_response:
                    speakers = speakers_response.get("speakers", [])
                elif "structuredOutput" in speakers_response:
                    structured_output = speakers_response.get("structuredOutput", {})
                    if isinstance(structured_output, str):
                        import json as json_module
                        try:
                            structured_output = json_module.loads(structured_output)
                        except:
                            structured_output = {}
                    speakers = structured_output.get("speakers", [])
                elif "structured_output" in speakers_response:
                    structured_output = speakers_response.get("structured_output", {})
                    if isinstance(structured_output, str):
                        import json as json_module
                        try:
                            structured_output = json_module.loads(structured_output)
                        except:
                            structured_output = {}
                    speakers = structured_output.get("speakers", [])
                else:
                    speakers = []
                attendee_sources = speakers_response.get("sources", [])
            except Exception as e:
                print(f"Error extracting speakers: {e}")
                return jsonify({
                    "error": f"Failed to extract speakers from event URL: {str(e)}"
                }), 500

        if not speakers:
            return jsonify({
                "error": "No speakers found on the event page. The page may be private, dynamically loaded, or not contain speaker information."
            }), 400

        # Limit speakers to prevent timeout
        # Vercel free tier has 10-second timeout, so we need to keep speaker count low
        # Even Pro tier (300s) can struggle with too many speakers due to OpenAI API latency
        MAX_SPEAKERS_DYNAMIC = 8  # For dynamically scraped events
        MAX_SPEAKERS_HARDCODED = 10  # For hardcoded events (reduced for Vercel compatibility)
        MAX_SPEAKERS = MAX_SPEAKERS_HARDCODED if use_hardcoded else MAX_SPEAKERS_DYNAMIC

        total_found = len(speakers)
        if len(speakers) > MAX_SPEAKERS:
            print(f"Limiting from {len(speakers)} to {MAX_SPEAKERS} speakers to prevent timeout")
            speakers = speakers[:MAX_SPEAKERS]

        attendee_data = f"Extracted {total_found} speakers from {event_url}" + (f" (processing top {MAX_SPEAKERS})" if total_found > MAX_SPEAKERS else "")
        print(f"Found {total_found} speakers, processing {len(speakers)}")

        # Step 2: Enrich each speaker with LinkedIn + company info
        # Skip enrichment for speed - use bio from structured extraction instead
        print(f"Step 2: Processing {len(speakers)} speakers...")
        enriched_speakers = []
        for i, speaker in enumerate(speakers):
            speaker_name = speaker.get("name", "Unknown")
            speaker_title = speaker.get("title", "N/A")
            speaker_company = speaker.get("company", "N/A")

            print(f"  Processing {i+1}/{len(speakers)}: {speaker_name} at {speaker_company}")

            # Use bio from structured extraction instead of making additional API calls
            # This dramatically speeds up the workflow
            enriched_speakers.append({
                **speaker,
                "enrichment": []  # Skip enrichment API calls for speed
            })

        # Convert enriched speakers to markdown table for ICP matcher
        enriched_attendees = convert_speakers_to_table(enriched_speakers)
        enrichment_sources = []

        # Step 3: Get user company ICP from their website
        print(f"Step 3: Analyzing ICP for {company_name} from {company_url}...")
        try:
            icp_response = linkup_client.get_company_icp_from_url(
                company_url=company_url,
                company_name=company_name
            )
            user_icp = icp_response.get("answer", "")
            icp_sources = icp_response.get("sources", [])

            if not user_icp:
                return jsonify({
                    "error": "Could not analyze ICP from company URL. Please verify the URL is correct."
                }), 400
        except Exception as e:
            return jsonify({
                "error": f"Failed to analyze company ICP: {str(e)}"
            }), 500

        # Step 4: Match attendee companies to user's ICP using OpenAI
        print("Step 4: Matching attendee companies to ICP...")
        try:
            match_result = icp_matcher.match_companies_to_icp(
                user_icp=user_icp,
                enriched_attendees=enriched_attendees,
                company_name=company_name
            )

            if "error" in match_result:
                return jsonify({
                    "error": f"ICP matching failed: {match_result['error']}"
                }), 500
        except Exception as e:
            return jsonify({
                "error": f"Failed to match companies to ICP: {str(e)}"
            }), 500

        # Compile results
        results = {
            "metadata": {
                "event_url": event_url,
                "company_url": company_url,
                "company_name": company_name,
                "analysis_date": datetime.now().isoformat(),
                "workflow_version": "v2_4step"
            },
            "step1_attendees": {
                "data": attendee_data,
                "sources": attendee_sources
            },
            "step2_enriched": {
                "data": enriched_attendees,
                "sources": enrichment_sources
            },
            "step3_icp": {
                "data": user_icp,
                "sources": icp_sources
            },
            "step4_matches": match_result
        }

        return jsonify(results), 200

    except Exception as e:
        print(f"Error in analyze_event: {e}")
        return jsonify({
            "error": f"An error occurred: {str(e)}"
        }), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "linkup_configured": linkup_client is not None,
        "openai_configured": icp_matcher is not None
    }), 200


@app.route('/static/<path:path>')
def send_static(path):
    """Serve static files."""
    return send_from_directory('static', path)


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5001))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'

    print("\n" + "="*70)
    print("Event ICP Matcher - Web Interface")
    print("="*70)
    print(f"\n🚀 Starting server on http://localhost:{port}")
    print(f"📊 API endpoint: http://localhost:{port}/api/analyze")
    print(f"💚 Health check: http://localhost:{port}/api/health")
    print("\nPress Ctrl+C to stop the server\n")

    app.run(host='0.0.0.0', port=port, debug=debug)
