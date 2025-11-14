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

        # USING MOCK DATA FOR DEMO - Cerebral Valley 2025 Speakers
        print(f"Using MOCK enriched data for Cerebral Valley speakers...")

        attendee_data = "Cerebral Valley 2025 Speakers and Discussion Leaders"
        attendee_sources = []

        enriched_attendees = """| Name | Role/Title | Affiliation/Company | Company Description |
|------|-----------|---------------------|---------------------|
| Amjad Masad | Founder & CEO | Replit | AI-powered cloud development platform enabling users to build apps and websites through natural language. Replit Agent automates software development with millions of users worldwide. |
| Mike Krieger | Chief Product Officer | Anthropic | AI safety and research company that develops Claude, a family of LLMs designed with safety, helpfulness, and honesty as core principles. Valued at $183B. |
| Jimmy Ba | Co-founder | xAI | Elon Musk's AI company focused on developing advanced AI systems to understand the universe. Building Grok AI assistant. |
| Guillermo Rauch | Founder & CEO | Vercel | Cloud platform for frontend developers, creator of Next.js. Provides edge network, serverless functions, and Git-integrated deployments for modern web apps. |
| Winston Weinberg | Founder & CEO | Harvey | AI-powered legal platform built on GPT-4 for law firms and corporations. Valued at $3B with 235 clients across 42 countries. Helps with legal research, drafting, and diligence. |
| Elad Gil | Founder | Gil & Co. | Venture capital investor and advisor to major tech companies including Airbnb, Coinbase, Stripe, Square, and others. |
| Ilya Fushman | Partner | Kleiner Perkins | Leading venture capital firm that has invested in companies like Amazon, Google, and Genentech. Focus on enterprise, consumer, and healthcare tech. |
| Andy Konwinski | Co-founder | Laude | AI-powered conversation intelligence platform for sales teams. Helps analyze and improve sales calls and meetings. |
| Cristina Cordova | COO | Linear | Modern issue tracking and project management tool for software teams. Known for exceptional design and performance. Used by thousands of companies. |
| Mati Staniszewski | Founder & CEO | ElevenLabs | Leading AI voice generation company with 5,000+ voices in 70+ languages. Creates lifelike speech for content creators, businesses, and developers. |
| Tuhin Srivastava | Founder & CEO | Baseten | ML infrastructure platform that helps companies deploy and scale machine learning models in production. Serverless ML deployment. |
| Eoghan McCabe | Founder & CEO | Intercom | Customer messaging platform with AI-powered chatbots and support tools. Serves 25,000+ businesses with conversational relationship platform. |
| Christina Cacioppo | Founder & CEO | Vanta | Security compliance automation platform. Helps companies get SOC 2, ISO 27001, HIPAA, and other certifications. Over 8,000 customers. |
| Aaron Levie | Founder & CEO | Box | Enterprise cloud content management and file sharing platform. Publicly traded (NYSE: BOX) with millions of users across 100,000+ organizations. |
| Daniel Lurie | Mayor | City and County of San Francisco | Mayor of San Francisco, focused on technology, innovation, and civic improvement in the Bay Area. |
| Parag Agrawal | Founder & CEO | Parallel Web Systems | Former Twitter CEO building AI-powered software development tools. Focused on parallel computing and distributed systems. |
| Gabriel Hubert | Founder & CEO | Dust | AI assistant platform for teams. Helps companies build custom AI assistants that connect to their data and workflows. |
| Anna Patterson | Founder & CEO | Ceramic.ai | AI-powered data management and knowledge graph platform. Former Google engineer who built key parts of search infrastructure. |
| Kirsten Green | Founder & Managing Partner | Forerunner Ventures | Leading consumer-focused VC firm. Early investor in Warby Parker, Glossier, Jet.com, Dollar Shave Club, and Chime. |
| Eleonore Crespo | Founder & CEO | Pigment | Business planning platform that helps CFOs and finance teams with forecasting, modeling, and strategic planning. Over 400 enterprise customers. |
| Tudor Achim | Founder & CEO | Harmonic | AI-powered search and knowledge management platform for teams. Helps companies organize and find information across all their tools. |
| Julie Bornstein | Founder & CEO | Daydream | AI-powered fashion and shopping platform. Former Stitch Fix COO and Nordstrom executive building personalized shopping experiences. |
| Kevin Novak | Founder & Managing Partner | Rackhouse Venture Capital | Early-stage venture capital firm focused on B2B SaaS, infrastructure, and developer tools. |
| Ophelia Brown | Managing Partner | Blossom Capital | European VC firm focused on B2B software. Invested in companies like UiPath, Contentful, and Ledger. |
| Marc Boroditsky | CRO | Nebius | Cloud infrastructure company spun out of Yandex. Provides GPU cloud and AI infrastructure for model training and inference. |
| Jai Das | Co-founder, President & Partner | Sapphire Ventures | Growth-stage venture capital firm with $10B+ under management. Invested in LinkedIn, Box, AppDynamics, and others. |
| Astasia Myers | General Partner | Felicis | VC firm focused on early-stage startups. Portfolio includes Shopify, Canva, Notion, and Plaid. |
| Stefan Weitz | Co-founder & CEO | HumanX | Event series and community focused on human-centered AI and technology. Brings together leaders in AI, policy, and business. |
| Howie Xu | Chief AI & Innovation Officer | Gen | Digital safety company (formerly Norton and Avast). Building AI-powered cybersecurity and privacy tools for consumers. |
| Sarah Wooders | Founder & CTO | Letta | AI memory management platform. Helps AI agents maintain context and memory across conversations. Built by former Berkeley AI researchers. |
| Brooke Hopkins | Founder & CEO | Coval | AI evaluation and testing platform for LLM applications. Helps companies ensure their AI systems are reliable and safe before deployment. |
| Ethan Lutske | Partner | Wilson Sonsini | Top Silicon Valley law firm specializing in technology, startups, and venture capital. Represented Google, Apple, Tesla in major transactions. |
| Keith Figlioli | Managing Partner | LRVHealth | Healthcare-focused venture capital firm investing in digital health, healthcare services, and life sciences companies. |
| Jake Saper | General Partner | Emergence Capital | Enterprise SaaS-focused VC firm. Early investors in Salesforce, Zoom, Box, and other major SaaS companies. |
| Roy Bahat | Head | Bloomberg Beta | Venture capital arm of Bloomberg LP. Focuses on the future of work, machine intelligence, and data-driven companies. |
"""
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
