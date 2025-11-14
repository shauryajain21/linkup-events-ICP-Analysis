# 🚀 Quick Start - Web App

Get the Event ICP Matcher web interface running in 3 steps!

## Step 1: Install

```bash
cd event-icp-matcher
pip install -r requirements.txt
```

## Step 2: Configure

Create `.env` file with your API keys:

```bash
cp .env.example .env
```

Then edit `.env`:
```bash
LINKUP_API_KEY=your_linkup_key
ANTHROPIC_API_KEY=your_anthropic_key
```

**Get API Keys:**
- Linkup: https://linkup.so
- Anthropic: https://console.anthropic.com

## Step 3: Run

```bash
python app.py
```

## Step 4: Open Browser

Navigate to: **http://localhost:5001**

---

## What You'll See

### 1. Beautiful Landing Page
- Linkup-themed design with beige background
- Serif typography for headings
- Dark olive green accent colors
- Clean, minimal interface

### 2. Analysis Form
Fill out:
- Event name (required)
- Event URL (recommended)
- Your company name
- Company domain

### 3. Results Page
Get:
- Summary metrics (High/Medium/Low priority counts)
- ICP match scores for each attendee
- Detailed reasoning and recommendations
- Contact information and talking points

---

## Features

✅ **Linkup Brand Theme** - Matches Linkup's design system
✅ **Responsive** - Works on all devices
✅ **Fast** - Results in 20-40 seconds
✅ **Beautiful** - Clean, professional interface
✅ **Actionable** - Get specific next steps for each prospect

---

## Need Help?

- 📖 Full Web Guide: [WEB_APP_GUIDE.md](WEB_APP_GUIDE.md)
- 📚 Main Docs: [README.md](README.md)
- ⚡ Quick Start: [QUICKSTART.md](QUICKSTART.md)

---

## Troubleshooting

**"Address already in use"**
```bash
# Change port
PORT=5002 python app.py
```

**"API clients not initialized"**
- Check your `.env` file has both API keys
- Make sure keys are valid

**Can't access from other devices**
- Server binds to `0.0.0.0` by default
- Access from other devices: `http://<your-ip>:5001`

---

Happy prospecting! 🎯
