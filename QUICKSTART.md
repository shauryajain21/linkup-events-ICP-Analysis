# Quick Start Guide

Get started with Event ICP Matcher in 5 minutes!

## 1. Install Dependencies

```bash
cd event-icp-matcher
pip install -r requirements.txt
```

## 2. Set Up API Keys

Create a `.env` file:

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:

```bash
LINKUP_API_KEY=your_linkup_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
```

**Get API Keys:**
- Linkup: https://linkup.so (sign up for free)
- Anthropic: https://console.anthropic.com

## 3. Run Your First Analysis

```bash
python main.py "AI Agents Hackathon NYC 2025" \
  --event-url "https://partful.com/e/ai-agents-hackathon"
```

## 4. View Results

The tool will:
1. ✅ Research Linkup's ICP (default company)
2. ✅ Find event attendees using deep search
3. ✅ Analyze each attendee for ICP match
4. ✅ Show prioritized results with action items

## Example Output

```
======================================================================
ANALYSIS SUMMARY
======================================================================

Total Attendees Analyzed: 12
  • High Priority Matches: 4
  • Medium Priority Matches: 5
  • Low Priority Matches: 2
  • Not a Fit: 1

======================================================================
TOP PRIORITY MATCHES
======================================================================

1. Sarah Chen - Senior ML Engineer
   Company: DataCorp Inc
   ICP Score: 9/10 (High Priority)
   Action: Schedule demo call
   Key Points: Real-time data needs, API integration
```

## Next Steps

### Analyze for Your Company

```bash
python main.py "Your Event Name" \
  --event-url "https://event-url.com" \
  --company-name "Your Company" \
  --company-domain "yourcompany.com"
```

### Save Results

```bash
python main.py "Event Name" \
  --output "results/analysis.json"
```

### Use in Python

```python
from main import EventICPMatcher

matcher = EventICPMatcher()
results = matcher.analyze_event(
    event_name="Event Name",
    event_url="https://event-url.com"
)
```

## Common Use Cases

### 1. Pre-Event Prospecting
Find high-value attendees to schedule meetings with.

### 2. Post-Event Follow-Up
Prioritize who to contact after the event.

### 3. Event ROI Analysis
Determine if an event is worth attending.

## Tips

- ✅ Always include the `--event-url` for best results
- ✅ Run analysis close to the event date
- ✅ Check your company website has clear ICP signals
- ✅ Review the full README.md for advanced features

## Troubleshooting

**"API key must be provided"**
→ Make sure your `.env` file has both API keys

**"Could not fetch event attendees"**
→ Verify the event URL is correct and publicly accessible

**Low quality results**
→ Try including the event URL and ensure it has public attendee info

## Learn More

- Full documentation: [README.md](README.md)
- Example scripts: [examples/example_usage.py](examples/example_usage.py)
- Linkup docs: https://docs.linkup.so
- Claude docs: https://docs.anthropic.com

Happy prospecting! 🎯
