# Web App Guide - Event ICP Matcher

A beautiful, Linkup-themed web interface for the Event ICP Matcher.

## Features

- 🎨 **Linkup Brand Theme** - Matches Linkup's design system with beige backgrounds, dark olive green accents, and serif typography
- 📱 **Responsive Design** - Works perfectly on desktop, tablet, and mobile
- ⚡ **Real-time Analysis** - Interactive form with loading states
- 📊 **Beautiful Results** - Clean, organized display of ICP matches
- 🎯 **Priority Scoring** - Visual badges for High/Medium/Low priority matches
- 🔗 **Contact Integration** - Direct links to LinkedIn, email, and Twitter

## Quick Start

### 1. Install Dependencies

```bash
cd event-icp-matcher
pip install -r requirements.txt
```

### 2. Configure Environment

Make sure your `.env` file has the required API keys:

```bash
LINKUP_API_KEY=your_linkup_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
```

### 3. Run the Web Server

```bash
python app.py
```

The server will start at: **http://localhost:5001**

### 4. Open in Browser

Navigate to `http://localhost:5001` in your web browser.

## Using the Web Interface

### Step 1: Enter Event Details

1. **Event Name** (required) - e.g., "AI Agents Hackathon NYC 2025"
2. **Event URL** (recommended) - The event page URL for better accuracy
3. **Your Company Name** - Defaults to "Linkup"
4. **Company Domain** - Defaults to "linkup.so"

### Step 2: Analyze

Click "Analyze Event" and wait 20-40 seconds while:
- Linkup searches for attendees
- Your company's ICP is researched
- Claude analyzes each match

### Step 3: Review Results

The results page shows:

#### Summary Cards
- High Priority Matches
- Medium Priority Matches
- Low Priority Matches
- Not a Fit count

#### Overall Assessment
Claude's summary of the event's ICP fit

#### Attendee Cards
For each attendee:
- Name, role, and company
- ICP match score (1-10)
- Match reasoning
- Recommended action
- Key talking points
- Contact links (LinkedIn, email, Twitter)

## Design System

The web app uses Linkup's brand colors and design principles:

### Colors

```css
--color-bg: #F5F3EF           /* Beige background */
--color-bg-white: #FFFFFF     /* White cards */
--color-primary: #3D5A45      /* Dark olive green */
--color-text: #1A1A1A         /* Black text */
--color-text-secondary: #666  /* Gray text */
--color-border: #E0DDD8       /* Subtle borders */
```

### Typography

- **Headings**: Crimson Pro (serif)
- **Body**: Inter (sans-serif)

### Components

- **Buttons**: Rounded corners, olive green primary, hover effects
- **Cards**: White backgrounds with subtle shadows
- **Forms**: Clean inputs with focus states
- **Badges**: Color-coded priority levels

## API Endpoints

### POST /api/analyze

Analyze an event and return ICP matches.

**Request:**
```json
{
  "event_name": "Event Name",
  "event_url": "https://...",
  "company_name": "Company",
  "company_domain": "domain.com",
  "use_company_research": true
}
```

**Response:**
```json
{
  "metadata": {
    "event_name": "...",
    "analysis_date": "2025-01-11T..."
  },
  "icp_analysis": {
    "summary": {
      "total_attendees_analyzed": 10,
      "high_priority_matches": 3,
      ...
    },
    "attendees": [...],
    "overall_event_assessment": "...",
    "recommendations": [...]
  }
}
```

### GET /api/health

Check API configuration status.

**Response:**
```json
{
  "status": "healthy",
  "linkup_configured": true,
  "claude_configured": true
}
```

## File Structure

```
event-icp-matcher/
├── app.py                      # Flask web server
├── templates/
│   └── index.html             # Main HTML template
├── static/
│   ├── css/
│   │   └── style.css          # Linkup-themed styles
│   └── js/
│       └── app.js             # Frontend JavaScript
└── ...
```

## Customization

### Change Port

Set the `PORT` environment variable:

```bash
PORT=3000 python app.py
```

Or in `.env`:
```bash
PORT=3000
```

### Enable Debug Mode

In `.env`:
```bash
FLASK_DEBUG=True
```

### Modify Theme Colors

Edit `static/css/style.css` and change the CSS variables:

```css
:root {
    --color-primary: #3D5A45;  /* Change this */
    --color-bg: #F5F3EF;       /* And this */
}
```

### Customize Company Defaults

In the HTML form (`templates/index.html`), change:

```html
<input id="company-name" value="Your Company">
<input id="company-domain" value="yourcompany.com">
```

## Development

### Watch for Changes

For development, use Flask's debug mode:

```bash
FLASK_DEBUG=True python app.py
```

This enables:
- Auto-reload on code changes
- Detailed error pages
- Debug console

### Add New Features

**Frontend:**
1. Edit `templates/index.html` for structure
2. Edit `static/css/style.css` for styling
3. Edit `static/js/app.js` for interactivity

**Backend:**
1. Edit `app.py` for new API endpoints
2. Edit `linkup_client.py` or `icp_matcher.py` for core logic

## Deployment

### Local Network Access

To access from other devices on your network:

```bash
python app.py
```

Then visit `http://<your-ip>:5001` from other devices.

### Production Deployment

For production, use a WSGI server like Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5001 app:app
```

Or use a Platform as a Service (PaaS):

**Heroku:**
1. Add `Procfile`: `web: gunicorn app:app`
2. Deploy: `git push heroku main`

**Railway/Render:**
1. Connect GitHub repo
2. Set build command: `pip install -r requirements.txt`
3. Set start command: `gunicorn app:app`

### Environment Variables in Production

Make sure to set:
- `LINKUP_API_KEY`
- `ANTHROPIC_API_KEY`
- `PORT` (if required by platform)

## Troubleshooting

### "Connection refused" error

Make sure the server is running:
```bash
python app.py
```

### "API clients not initialized"

Check your `.env` file has both API keys set correctly.

### Slow analysis

- Normal analysis takes 20-40 seconds
- Deep search adds time but improves accuracy
- Event URL helps Linkup find better results

### Styling issues

Clear browser cache:
- Chrome: Ctrl+Shift+R (Cmd+Shift+R on Mac)
- Firefox: Ctrl+F5
- Safari: Cmd+Option+R

### CORS errors

If accessing from a different domain, CORS is already enabled in `app.py`:
```python
from flask_cors import CORS
CORS(app)
```

## Screenshots

The web app features:

1. **Hero Section**
   - Linkup-inspired beige background
   - Serif headline typography
   - Clean CTA buttons

2. **Analysis Form**
   - White card with subtle shadow
   - Clean input fields with focus states
   - Loading animations

3. **Results Display**
   - Summary cards with key metrics
   - Color-coded priority badges
   - Expandable attendee cards
   - Contact information links

4. **How It Works**
   - Step-by-step explanation
   - Icon-based visual design
   - Responsive grid layout

## Browser Support

- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+

## Performance

- First load: ~1-2 seconds
- Analysis time: 20-40 seconds
- Results rendering: Instant
- No page reloads needed

## Accessibility

- Semantic HTML structure
- ARIA labels where needed
- Keyboard navigation support
- High contrast colors
- Responsive text sizing

## Next Steps

1. Try the demo at `http://localhost:5001`
2. Analyze a real event
3. Customize the theme for your brand
4. Deploy to production
5. Share with your team!

---

**Questions?** Check the main [README.md](README.md) or [QUICKSTART.md](QUICKSTART.md)
