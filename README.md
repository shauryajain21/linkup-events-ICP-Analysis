# Event ICP Matcher

A powerful tool that uses **Linkup's API** to find people attending events and **Claude AI** to determine if they match your company's Ideal Customer Profile (ICP).

> 🌐 **New!** Now available with a beautiful web interface styled with Linkup's brand theme! See [Web App Guide](WEB_APP_GUIDE.md)

## Overview

This project helps sales and marketing teams:
- 🔍 **Discover** who's attending specific events using Linkup's deep search capabilities
- 🎯 **Analyze** each attendee against your company's ICP using Claude AI
- 📊 **Prioritize** outreach based on ICP match scores
- 💡 **Generate** personalized talking points for each high-priority lead

## Features

- 🌐 **Web Interface** - Beautiful Linkup-themed UI for easy analysis (NEW!)
- **Smart Event Research**: Uses Linkup's deep search to find attendees from multiple sources (LinkedIn, Twitter/X, event pages, etc.)
- **ICP Analysis**: Leverages Claude AI to analyze if attendees match your ideal customer profile
- **Prioritized Scoring**: Assigns match scores (1-10) and priority levels to each attendee
- **Actionable Insights**: Provides specific next steps and talking points for each prospect
- **Flexible Configuration**: Works with any company and event
- **Source Attribution**: Shows sources for all information found
- **CLI & API**: Use via command line or programmatically in Python

## Architecture

```
┌─────────────────┐
│   Event Info    │
│  (Name + URL)   │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│         Linkup API                      │
│  ┌─────────────┐    ┌────────────────┐ │
│  │   Company   │    │     Event      │ │
│  │  Research   │    │   Attendees    │ │
│  │   (ICP)     │    │    Search      │ │
│  └─────────────┘    └────────────────┘ │
└─────────────────────────────────────────┘
         │                    │
         └────────┬───────────┘
                  ▼
         ┌─────────────────┐
         │   Claude AI     │
         │  ICP Matching   │
         │   & Analysis    │
         └────────┬────────┘
                  ▼
         ┌─────────────────┐
         │  Prioritized    │
         │   Match List    │
         │ + Action Items  │
         └─────────────────┘
```

## Installation

### Prerequisites

- Python 3.8 or higher
- Linkup API key ([Get one here](https://linkup.so))
- Anthropic API key ([Get one here](https://console.anthropic.com))

### Setup

1. **Clone or download this project**

```bash
cd event-icp-matcher
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Configure environment variables**

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:

```bash
# Linkup API Configuration
LINKUP_API_KEY=your_linkup_api_key_here

# Anthropic API Configuration
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Company Configuration (optional)
COMPANY_NAME=Linkup
COMPANY_DOMAIN=linkup.so
```

## Usage

### Web Interface (Recommended)

The easiest way to use Event ICP Matcher is through the web interface:

```bash
# Start the web server
python app.py

# Open your browser to http://localhost:5001
```

Then fill out the form with your event details and click "Analyze Event"!

📖 **Full guide:** [Web App Guide](WEB_APP_GUIDE.md)

### Command Line Interface

Analyze attendees for an event from the terminal:

```bash
python main.py "AI Agents Hackathon NYC 2025"
```

### With Event URL (Recommended)

Providing the event URL improves accuracy:

```bash
python main.py "AI Agents Hackathon NYC 2025" \
  --event-url "https://lu.ma/ai-agents-hackathon-nyc"
```

### Custom Company

Analyze for a different company:

```bash
python main.py "SaaS Connect 2025" \
  --event-url "https://example.com/event" \
  --company-name "Acme Corp" \
  --company-domain "acme.com"
```

### Save Results to File

Save the full analysis to a JSON file:

```bash
python main.py "Tech Summit 2025" \
  --event-url "https://example.com/event" \
  --output "results/tech_summit_2025.json"
```

### All Options

```bash
python main.py --help
```

**Options:**
- `event_name` (required): Name of the event to analyze
- `--event-url`: URL of the event page (recommended for better results)
- `--company-name`: Your company name (default: from .env or "Linkup")
- `--company-domain`: Your company domain (default: from .env or "linkup.so")
- `--no-company-research`: Skip Linkup research for company ICP (uses Claude's knowledge)
- `--output`: Output file path for saving results (JSON format)

## Example Output

```
======================================================================
Event ICP Matcher - Analyzing: AI Agents Hackathon NYC 2025
======================================================================

[Step 1/3] Researching Linkup's ICP...
✓ Company research completed (1847 characters)

[Step 2/3] Searching for attendees of 'AI Agents Hackathon NYC 2025'...
✓ Found attendee information (3421 characters)
  Sources used: 8

[Step 3/3] Analyzing ICP matches with Claude AI...
✓ Analysis completed successfully

======================================================================
ANALYSIS SUMMARY
======================================================================

Total Attendees Analyzed: 12
  • High Priority Matches: 4
  • Medium Priority Matches: 5
  • Low Priority Matches: 2
  • Not a Fit: 1

Overall Assessment:
  This event has strong ICP alignment with multiple AI/ML engineers and
  technical decision-makers from target companies.

======================================================================
TOP PRIORITY MATCHES
======================================================================

1. Sarah Chen - Senior ML Engineer
   Company: DataCorp Inc
   ICP Score: 9/10 (High Priority)
   Action: Schedule demo call to discuss search API integration
   Key Points: Real-time data needs, API integration experience

2. Michael Rodriguez - VP of Engineering
   Company: TechStart AI
   ICP Score: 8/10 (High Priority)
   Action: Send product overview focused on deep search capabilities
   Key Points: Building AI agents, Need reliable data sources

...

======================================================================
RECOMMENDATIONS
======================================================================

1. Prioritize outreach to the 4 high-priority matches within 48 hours
2. Prepare technical demo materials for ML engineers
3. Follow up with medium-priority matches via LinkedIn

======================================================================
```

## How It Works

### 1. Company ICP Research (Linkup)

The tool uses Linkup to deeply research your company by analyzing:
- Homepage and about page
- Product pages
- Pricing page
- Blog content

Following Linkup's best practices, it extracts:
- Products and services
- Business model
- Target market and ICP
- Key value propositions
- Industries served
- Typical customer size (SMB, Mid-market, Enterprise)

### 2. Event Attendee Discovery (Linkup)

Using Linkup's deep search, the tool finds attendees from:
- Event registration pages
- Speaker lists and bios
- LinkedIn posts about the event
- Twitter/X announcements
- Event organizer announcements

The search focuses on:
- Names and professional backgrounds
- Current companies and roles
- LinkedIn profiles
- Professional details

### 3. ICP Matching & Analysis (Claude)

Claude AI analyzes each attendee and provides:

**For each person:**
- ICP Match Score (1-10)
- Match reasoning based on:
  - Company size and industry
  - Role and decision-making authority
  - Pain points alignment
  - Budget indicators
  - Geographic relevance
- Opportunity type (High/Medium/Low Priority or Not a Fit)
- Recommended action
- Key talking points for outreach
- Contact information

**Overall:**
- Summary statistics
- Event assessment
- Strategic recommendations

## Use Cases

### 1. Pre-Event Prospecting
Identify high-value attendees before the event to schedule meetings.

### 2. Post-Event Follow-Up
Prioritize who to follow up with after the event.

### 3. Event ROI Analysis
Determine if an event is worth attending based on attendee ICP fit.

### 4. Competitive Intelligence
Understand who your competitors are targeting at events.

### 5. Partnership Opportunities
Find potential partners or integration opportunities.

## Tips for Best Results

### Event Research
- ✅ **Always provide the event URL** for better accuracy
- ✅ Use the official event page, Eventbrite, Luma, or Partful links
- ✅ For large conferences, search for specific tracks or sessions
- ✅ Run searches close to the event date when attendee lists are finalized

### Company ICP
- ✅ Keep your company website updated with clear value propositions
- ✅ Include case studies and customer testimonials
- ✅ Maintain an active blog with customer-focused content
- ✅ Use `--no-company-research` flag for faster results if ICP is well-known

### Prompting Best Practices (from Linkup)
The tool follows Linkup's prompting guidelines:
- **Clear goals**: Specific objectives for each search
- **Defined scope**: Targeted domains and sources
- **Structured criteria**: Detailed information requirements
- **Response format**: Structured output for consistency

## Advanced Usage

### Python API

You can also use the tool programmatically:

```python
from main import EventICPMatcher

# Initialize
matcher = EventICPMatcher()

# Analyze event
results = matcher.analyze_event(
    event_name="AI Agents Hackathon NYC 2025",
    event_url="https://lu.ma/ai-agents-hackathon",
    company_name="Linkup",
    company_domain="linkup.so",
    output_file="results/analysis.json"
)

# Access results
print(f"High priority matches: {results['icp_analysis']['summary']['high_priority_matches']}")

for attendee in results['icp_analysis']['attendees']:
    if attendee['opportunity_type'] == 'High Priority':
        print(f"Reach out to: {attendee['name']} at {attendee['company']}")
```

### Custom ICP Analysis

Use just the ICP matcher component:

```python
from icp_matcher import ICPMatcher

matcher = ICPMatcher()

# Analyze with custom company info and attendee data
analysis = matcher.analyze_icp_match(
    company_info="Your detailed company ICP description...",
    attendee_info="Information about event attendees...",
    company_name="Your Company"
)
```

## Output Format

Results are saved in JSON format with this structure:

```json
{
  "metadata": {
    "event_name": "Event Name",
    "event_url": "https://...",
    "company_name": "Company",
    "company_domain": "domain.com",
    "analysis_date": "2025-01-11T10:30:00"
  },
  "company_icp": "Detailed ICP research...",
  "attendee_research": "Detailed attendee information...",
  "sources": [
    {
      "name": "Source name",
      "url": "https://...",
      "snippet": "..."
    }
  ],
  "icp_analysis": {
    "summary": {
      "total_attendees_analyzed": 10,
      "high_priority_matches": 3,
      "medium_priority_matches": 4,
      "low_priority_matches": 2,
      "not_a_fit": 1
    },
    "attendees": [...],
    "overall_event_assessment": "...",
    "recommendations": [...]
  }
}
```

## Project Structure

```
event-icp-matcher/
├── main.py                 # Main application and CLI
├── linkup_client.py        # Linkup API client
├── icp_matcher.py          # Claude AI ICP matching logic
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── .gitignore             # Git ignore rules
├── README.md              # This file
└── examples/
    └── example_usage.py   # Example scripts
```

## Troubleshooting

### "Linkup API key must be provided"
Make sure you've set `LINKUP_API_KEY` in your `.env` file.

### "Anthropic API key must be provided"
Make sure you've set `ANTHROPIC_API_KEY` in your `.env` file.

### "Could not fetch event attendees"
- Verify the event URL is correct
- Try using just the event name without URL
- Check that the event has public attendee information

### Low quality results
- Provide the event URL for better accuracy
- Make sure your company website has clear ICP signals
- Try analyzing closer to the event date when more info is available

## Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Improve documentation
- Add new ICP matching criteria

## License

MIT License - feel free to use this for commercial or personal projects.

## Credits

Built with:
- **[Linkup](https://linkup.so)** - Deep search API for online content
- **[Claude AI](https://anthropic.com)** - Advanced AI for ICP analysis
- **[Anthropic Python SDK](https://github.com/anthropics/anthropic-sdk-python)**

## Support

For issues or questions:
- Linkup API: https://docs.linkup.so
- Claude AI: https://docs.anthropic.com
- This project: [Create an issue](https://github.com/yourusername/event-icp-matcher/issues)
