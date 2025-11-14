# Event ICP Matcher - Project Overview

## What This Project Does

The **Event ICP Matcher** is an intelligent prospecting tool that helps sales and marketing teams identify high-value leads at events by:

1. **Finding** people attending specific events using Linkup's deep search API
2. **Analyzing** each attendee against your Ideal Customer Profile (ICP) using Claude AI
3. **Prioritizing** prospects with match scores and recommended actions
4. **Providing** personalized talking points for outreach

## Key Value Propositions

### For Sales Teams
- 🎯 **Pre-qualify leads** before events to maximize ROI
- ⏱️ **Save time** by focusing on high-priority prospects
- 💡 **Get talking points** tailored to each prospect
- 📊 **Track event ROI** with ICP match analytics

### For Marketing Teams
- 📍 **Select better events** based on attendee ICP fit
- 🎪 **Plan booth strategy** around high-value attendees
- 📈 **Measure event quality** with quantitative ICP metrics
- 🤝 **Find partnerships** and integration opportunities

## Technical Innovation

### 1. Linkup API Integration
Uses Linkup's precise search engine following their best practices:

**Company ICP Research:**
```python
# Follows Linkup's prompt template for business intelligence
prompt = """
You are an expert business analyst. Describe {company}'s activities.
The company domain is {domain}. Analyze homepage, about, pricing, blog.

Include:
- Products and business model
- Target market and ICP
- Value propositions
- Customer pain points

Be sharp and business oriented.
"""
```

**Event Attendee Discovery:**
```python
# Deep search across multiple sources
- Event registration pages
- Speaker lists
- LinkedIn announcements
- Twitter/X posts
- Event organizer sites
```

### 2. Claude AI Analysis
Leverages Claude's advanced reasoning for nuanced ICP matching:

- Analyzes company size, industry, role fit
- Identifies pain points and buying signals
- Scores match quality (1-10 scale)
- Generates personalized outreach strategies
- Provides specific next actions

### 3. Intelligent Prioritization
Four-tier priority system:
- **High Priority**: Perfect ICP match - reach out immediately
- **Medium Priority**: Good potential - worth exploring
- **Low Priority**: Weak fit - low priority
- **Not a Fit**: Doesn't match ICP criteria

## How It Works - Step by Step

```
┌─────────────────────────────────────────────────────────────┐
│ INPUT: Event Name + URL + Company Info                      │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │   STEP 1: Research    │
         │   Company ICP         │
         │   (Linkup Deep Search)│
         └───────────┬───────────┘
                     │
                     ├─→ Analyze homepage
                     ├─→ Parse product pages
                     ├─→ Extract ICP signals
                     └─→ Identify target market
                     │
                     ▼
         ┌───────────────────────┐
         │   STEP 2: Find        │
         │   Event Attendees     │
         │   (Linkup Deep Search)│
         └───────────┬───────────┘
                     │
                     ├─→ Search event pages
                     ├─→ Find LinkedIn posts
                     ├─→ Check speaker lists
                     └─→ Scan social media
                     │
                     ▼
         ┌───────────────────────┐
         │   STEP 3: Analyze     │
         │   ICP Matches         │
         │   (Claude AI)         │
         └───────────┬───────────┘
                     │
                     ├─→ Score each attendee
                     ├─→ Generate reasoning
                     ├─→ Create action items
                     └─→ Suggest talking points
                     │
                     ▼
┌────────────────────────────────────────────────────────────┐
│ OUTPUT: Prioritized Lead List + Actions + Talking Points   │
└────────────────────────────────────────────────────────────┘
```

## Project Structure

```
event-icp-matcher/
│
├── main.py                    # Main application and CLI
│   ├── EventICPMatcher class
│   ├── CLI argument parsing
│   └── Result formatting and display
│
├── linkup_client.py           # Linkup API wrapper
│   ├── LinkupClient class
│   ├── search() - Generic search
│   ├── search_event_attendees() - Event-specific search
│   └── get_company_info() - Company ICP research
│
├── icp_matcher.py             # Claude AI integration
│   ├── ICPMatcher class
│   ├── analyze_icp_match() - Main analysis logic
│   └── quick_company_icp_analysis() - Fallback ICP
│
├── requirements.txt           # Python dependencies
├── .env.example              # Environment variables template
├── .gitignore                # Git ignore rules
│
├── README.md                 # Full documentation
├── QUICKSTART.md            # Quick start guide
├── PROJECT_OVERVIEW.md      # This file
│
└── examples/
    ├── example_usage.py     # Example scripts
    └── output/              # Example output files
```

## Core Technologies

| Technology | Purpose | Why We Use It |
|------------|---------|---------------|
| **Linkup API** | Deep search for company & event data | Precise, structured search optimized for AI; follows detailed prompts; provides source attribution |
| **Claude AI (Sonnet)** | ICP analysis and matching | Advanced reasoning; nuanced business analysis; structured JSON output; excellent at following complex instructions |
| **Python 3.8+** | Application language | Easy integration; great for data processing; extensive library support |
| **Anthropic SDK** | Claude API client | Official, well-maintained SDK |
| **Requests** | HTTP client for Linkup | Standard, reliable HTTP library |
| **python-dotenv** | Environment management | Secure API key handling |
| **Pydantic** | Data validation | Type safety for structured outputs |

## API Usage & Prompting Strategy

### Linkup Prompting Best Practices

Following Linkup's guide, we use the **4-component prompt anatomy**:

1. **Goal**: What we want to find
   ```
   "You are an expert business analyst researching attendees for event X"
   ```

2. **Scope**: Where to look
   ```
   "The event page is at [URL]. Focus on registration pages, speaker lists, LinkedIn posts"
   ```

3. **Criteria**: What information to extract
   ```
   "Find: names, roles, companies, LinkedIn profiles, professional backgrounds"
   ```

4. **Format**: How to return results
   ```
   "Return structured information with clear sources"
   ```

### Claude Prompting Strategy

For ICP analysis, we provide:

- **Context**: Company ICP and attendee data
- **Task**: Analyze each person for ICP fit
- **Criteria**: Specific factors to consider
- **Format**: JSON schema for structured output
- **Examples**: Clear scoring guidelines

## Example Use Case: Tech Conference

**Scenario**: You're attending "AI Summit 2025" and want to identify prospects.

**Input**:
```bash
python main.py "AI Summit 2025" \
  --event-url "https://aisummit.com/2025" \
  --company-name "Linkup" \
  --company-domain "linkup.so"
```

**Process**:
1. Linkup researches Linkup.so → Identifies ICP: AI/ML companies building agents
2. Linkup finds attendees → Discovers 50+ speakers/attendees with profiles
3. Claude analyzes each → Scores based on company size, role, AI focus

**Output**:
```
15 High Priority Matches:
- Dr. Sarah Chen, VP AI at DataCorp → Score: 9/10
  Action: Schedule demo on deep search for RAG systems
  Points: Mention structured output, cite reduction

- Michael Torres, CTO at StartupAI → Score: 8/10
  Action: Connect on LinkedIn, send API overview
  Points: Emphasize easy integration, developer experience
```

**Result**: Sales team has 15 qualified leads with personalized talking points before the event even starts!

## Configuration Options

### Environment Variables (.env)

```bash
# Required
LINKUP_API_KEY=sk_xxx                # From linkup.so
ANTHROPIC_API_KEY=sk-ant-xxx         # From console.anthropic.com

# Optional (can override via CLI)
COMPANY_NAME=Linkup
COMPANY_DOMAIN=linkup.so
```

### CLI Arguments

```bash
--event-url          # Event page URL (highly recommended)
--company-name       # Your company name
--company-domain     # Your website domain
--no-company-research  # Skip Linkup research, use Claude's knowledge
--output            # Save results to JSON file
```

## Output Schema

```json
{
  "metadata": {
    "event_name": "string",
    "event_url": "string",
    "company_name": "string",
    "analysis_date": "ISO-8601 timestamp"
  },
  "company_icp": "string (detailed ICP research)",
  "attendee_research": "string (attendee findings)",
  "sources": [
    {
      "name": "string",
      "url": "string",
      "snippet": "string"
    }
  ],
  "icp_analysis": {
    "summary": {
      "total_attendees_analyzed": "number",
      "high_priority_matches": "number",
      "medium_priority_matches": "number",
      "low_priority_matches": "number",
      "not_a_fit": "number"
    },
    "attendees": [
      {
        "name": "string",
        "role": "string",
        "company": "string",
        "icp_match_score": "number (1-10)",
        "match_reasoning": "string",
        "opportunity_type": "enum",
        "recommended_action": "string",
        "key_talking_points": ["string"],
        "contact_info": {
          "linkedin": "string",
          "email": "string",
          "twitter": "string"
        }
      }
    ],
    "overall_event_assessment": "string",
    "recommendations": ["string"]
  }
}
```

## Performance & Costs

### API Call Patterns

For a typical event analysis:

**Linkup API**:
- 1 deep search for company ICP (~5-10 seconds)
- 1 deep search for event attendees (~10-20 seconds)
- Total: ~15-30 seconds

**Claude API**:
- 1 analysis call with Sonnet (~3-5 seconds)
- Input tokens: ~2,000-5,000 (company + attendee data)
- Output tokens: ~1,000-3,000 (analysis results)

### Estimated Costs (per event analysis)

- Linkup: ~$0.10-0.50 per analysis (depending on depth and results)
- Claude: ~$0.05-0.15 per analysis (Sonnet pricing)
- **Total**: ~$0.15-0.65 per event

*Note: Costs are estimates based on typical usage. Actual costs vary based on data volume and search depth.*

## Future Enhancements

Potential features to add:

- [ ] **Multi-event batch processing**: Analyze multiple events in parallel
- [ ] **CRM integration**: Export to Salesforce, HubSpot
- [ ] **Email template generation**: Auto-generate personalized outreach emails
- [ ] **Calendar integration**: Schedule follow-ups automatically
- [ ] **Historical tracking**: Track engagement over time
- [ ] **Competitor tracking**: Identify which events competitors attend
- [ ] **Web interface**: Simple UI for non-technical users
- [ ] **Slack/Discord integration**: Get alerts for high-priority matches
- [ ] **LinkedIn auto-connect**: Automated connection requests (with user approval)
- [ ] **Custom scoring criteria**: User-defined ICP weights

## Getting Started

1. **Read**: [QUICKSTART.md](QUICKSTART.md) - 5-minute setup
2. **Try**: Run example analysis with default settings
3. **Customize**: Analyze for your own company
4. **Explore**: Check [examples/example_usage.py](examples/example_usage.py)
5. **Learn**: Read full [README.md](README.md) for advanced features

## Support & Resources

- **Linkup Docs**: https://docs.linkup.so
  - Prompting guide: https://docs.linkup.so/prompting
  - API reference: https://docs.linkup.so/api
- **Claude Docs**: https://docs.anthropic.com
  - Prompt engineering: https://docs.anthropic.com/claude/docs/prompt-engineering
- **Project Issues**: (Add your GitHub issues link)

## Credits

Built by [Your Name] using:
- Linkup API for deep search
- Claude AI for intelligent analysis
- Best practices from both platforms

---

**Ready to find your ideal customers at events? Let's get started!** 🚀
