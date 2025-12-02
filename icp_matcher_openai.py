"""
ICP Matcher using OpenAI to analyze if event attendees match company's ideal customer profile.
"""
import os
import json
from typing import Dict, List, Any, Optional
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class ICPMatcher:
    """Analyzes event attendees to determine if they match the company's ICP using OpenAI."""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the ICP Matcher with OpenAI.

        Args:
            api_key: OpenAI API key. If not provided, will look for OPENAI_API_KEY env variable.
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "OpenAI API key must be provided or set in OPENAI_API_KEY environment variable"
            )

        self.client = OpenAI(api_key=self.api_key)

    def analyze_icp_match(
        self,
        company_info: str,
        attendee_info: str,
        company_name: str = "your company"
    ) -> Dict[str, Any]:
        """
        Analyze if event attendees match the company's ICP using OpenAI.

        Args:
            company_info: Information about your company and its ICP (from Linkup).
            attendee_info: Information about event attendees (from Linkup).
            company_name: Name of your company.

        Returns:
            Dictionary containing ICP match analysis for each attendee.
        """
        prompt = f"""You are an expert sales and marketing analyst. Your task is to analyze event attendees and determine if they are a good match for {company_name}'s Ideal Customer Profile (ICP).

## Company Information and ICP:
{company_info}

## Event Attendees Information:
{attendee_info}

## Your Task:
Analyze each attendee mentioned and determine if they or their company would be a good fit for {company_name}. For each person:

1. **Identify the person**: Name, role, company
2. **ICP Match Score**: Rate from 1-10 (10 = perfect match)
3. **Match Reasoning**: Why they are or aren't a good fit based on:
   - Their company size and industry
   - Their role and decision-making authority
   - Pain points they might have that {company_name} solves
   - Budget and resources (if inferable)
   - Geographic location (if relevant)
4. **Opportunity Type**:
   - "High Priority" - Perfect ICP match, should reach out immediately
   - "Medium Priority" - Good potential, worth exploring
   - "Low Priority" - Weak fit, low priority for outreach
   - "Not a Fit" - Doesn't match ICP
5. **Recommended Action**: Specific next steps (e.g., "Schedule demo call", "Send product overview", "Connect on LinkedIn", "Skip - not a fit")
6. **Key Talking Points**: If it's a good match, what should you emphasize when reaching out?

## Output Format:
Return your analysis as a structured JSON with this exact schema:

{{
  "summary": {{
    "total_attendees_analyzed": <number>,
    "high_priority_matches": <number>,
    "medium_priority_matches": <number>,
    "low_priority_matches": <number>,
    "not_a_fit": <number>
  }},
  "attendees": [
    {{
      "name": "<person's name>",
      "role": "<job title>",
      "company": "<company name>",
      "icp_match_score": <1-10>,
      "match_reasoning": "<detailed explanation>",
      "opportunity_type": "<High Priority|Medium Priority|Low Priority|Not a Fit>",
      "recommended_action": "<specific next step>",
      "key_talking_points": ["<point 1>", "<point 2>", "<point 3>"],
      "contact_info": {{
        "linkedin": "<url if available>",
        "email": "<email if available>",
        "twitter": "<handle if available>"
      }}
    }}
  ],
  "overall_event_assessment": "<1-2 sentence summary of whether this event has good ICP matches>",
  "recommendations": ["<overall recommendation 1>", "<overall recommendation 2>"]
}}

Be thorough, analytical, and business-focused. Base your assessment on factual information provided."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert sales and marketing analyst specializing in ICP analysis and lead qualification."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                response_format={"type": "json_object"},
                temperature=0.7,
                max_tokens=4096
            )

            # Extract the text response
            response_text = response.choices[0].message.content

            try:
                result = json.loads(response_text)
            except json.JSONDecodeError:
                # If JSON parsing fails, return the raw text with a warning
                result = {
                    "error": "Failed to parse JSON response",
                    "raw_response": response_text
                }

            return result

        except Exception as e:
            return {
                "error": f"Failed to analyze ICP match: {str(e)}",
                "details": str(e)
            }

    # Hardcoded Linkup ICP for faster results
    LINKUP_ICP = """Linkup's Ideal Customer Profile:
- Company Size: Startups to large enterprises needing scalable API solutions
- Target Industries: AI apps, SaaS platforms, Business Intelligence, Fintech, Legal Tech, LLM developers
- Buyer Roles: Product Directors, CPOs, COOs, AI/ML Engineers, CTOs, Technical Founders
- Pain Points:
  • Need fast, accurate web search for AI grounding and fact-checking
  • Require real-time fact-based information for AI agents
  • CRM enrichment with verified web data
  • Secure, compliant enterprise API solutions
- Primary Use Cases:
  • Powering AI agents with reliable, up-to-date data
  • Building chatbots and answer engines with sourced information
  • Company enrichment for lead generation and sales intelligence
  • Deep research, due diligence, and risk analysis
- Value Proposition: Linkup provides a search API that delivers accurate, real-time web data optimized for AI applications"""

    def match_companies_to_icp(
        self,
        user_icp: str,
        enriched_attendees: str,
        company_name: str = "your company"
    ) -> Dict[str, Any]:
        """
        Match attendee companies against the user company's ICP.

        Args:
            user_icp: The ICP analysis of the user's company.
            enriched_attendees: The enriched attendee data with company descriptions.
            company_name: Name of the user's company.

        Returns:
            Dictionary containing match analysis with scores and recommendations.
        """
        # Check if we actually have attendee data
        no_data_phrases = [
            "no individuals found",
            "no detailed information",
            "no data is available",
            "no attendees",
            "not available",
            "cannot be found"
        ]

        if len(enriched_attendees) < 200 or any(phrase in enriched_attendees.lower() for phrase in no_data_phrases):
            return {
                "summary": {
                    "total_attendees_analyzed": 0,
                    "high_priority_matches": 0,
                    "medium_priority_matches": 0,
                    "low_priority_matches": 0,
                    "not_a_fit": 0
                },
                "attendees": [],
                "overall_event_assessment": "Could not extract attendee information from the event page. The page may be private, behind authentication, or dynamically loaded with JavaScript that prevented data extraction.",
                "recommendations": [
                    "Try a different event URL with publicly visible attendee lists",
                    "Check if the event has a public speakers or sponsors page",
                    "Consider using event platforms that display public RSVPs (some Eventbrite or Luma events)"
                ]
            }

        # Use hardcoded ICP for Linkup, dynamic ICP for others
        is_linkup = company_name.lower() in ["linkup", "linkup.so", "linkup api"]
        icp_to_use = self.LINKUP_ICP if is_linkup else user_icp

        prompt = f"""You are an expert sales and marketing analyst. Your task is to analyze the attendees and their companies from an event and determine which ones are a good match for {company_name}'s Ideal Customer Profile (ICP).

IMPORTANT: Only analyze people who are actually mentioned in the Event Attendees data below. Do NOT make up or hallucinate any attendees. If no attendees are listed, return an empty attendees array.

## {company_name}'s ICP:
{icp_to_use}

## Event Attendees with Company Information:
{enriched_attendees}

## Your Task:
Analyze EVERY attendee and their company. You MUST return an entry for EACH person in the attendees list above. For each person, generate:

1. **ICP Match Score (0-100)**: How well the person matches {company_name}'s ICP defined above
   - 86-100: Perfect ICP fit (matches target industries, roles, and pain points)
   - 61-85: Good match (relevant role or company)
   - 31-60: Moderate match (some relevance)
   - 0-30: Poor match (not relevant to {company_name}'s target market)

2. **Business Value Score (0-100)**: The potential business value
   - 86-100: Exceptional (key decision makers, industry leaders)
   - 61-85: High value (decision makers, influencers, partners)
   - 31-60: Moderate (potential users/customers)
   - 0-30: Low value

3. **Match Reasoning**: 1-2 sentences explaining the score

4. **Opportunity Type** (based on average of both scores):
   - "Perfect" - Average 86-100
   - "Good" - Average 61-85
   - "Moderate" - Average 31-60
   - "Poor" - Average 0-30

5. **Recommended Action**: Brief next step

## Output Format:
Return your analysis as a structured JSON. CRITICAL: Include ALL attendees from the input.

{{
  "summary": {{
    "total_attendees_analyzed": <number - MUST match number of input attendees>,
    "perfect_matches": <number>,
    "good_matches": <number>,
    "moderate_matches": <number>,
    "poor_matches": <number>
  }},
  "attendees": [
    {{
      "name": "<name>",
      "role": "<title>",
      "company": "<company>",
      "icp_match_score": <0-100>,
      "business_value_score": <0-100>,
      "match_reasoning": "<1-2 sentences>",
      "opportunity_type": "<Perfect|Good|Moderate|Poor>",
      "recommended_action": "<brief action>"
    }}
  ],
  "overall_event_assessment": "<1 sentence summary>"
}}

You MUST analyze every single person. Do not truncate or skip anyone."""

        # Retry logic for connection errors (common on serverless)
        max_retries = 3
        last_error = None

        for attempt in range(max_retries):
            try:
                response = self.client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are an expert sales and marketing analyst specializing in ICP analysis and lead qualification."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    response_format={"type": "json_object"},
                    temperature=0.7,
                    max_tokens=16000,
                    timeout=120  # 2 minute timeout per request
                )

                response_text = response.choices[0].message.content

                try:
                    result = json.loads(response_text)
                except json.JSONDecodeError:
                    result = {
                        "error": "Failed to parse JSON response",
                        "raw_response": response_text
                    }

                return result

            except Exception as e:
                last_error = e
                if attempt < max_retries - 1:
                    import time
                    time.sleep(2)  # Wait 2 seconds before retry
                    continue
                break

        # If all retries failed, return error
        return {
            "error": f"Failed to match companies to ICP: {str(last_error)}",
            "details": str(last_error)
        }

    def quick_company_icp_analysis(
        self,
        company_name: str,
        company_domain: Optional[str] = None,
        additional_context: Optional[str] = None
    ) -> str:
        """
        Generate a quick ICP summary for a company when Linkup data isn't available.

        Args:
            company_name: Name of the company.
            company_domain: Domain of the company.
            additional_context: Any additional context about the company.

        Returns:
            String containing ICP analysis.
        """
        prompt = f"""You are an expert in B2B sales and Ideal Customer Profile (ICP) definition.

Based on what you know about {company_name}"""

        if company_domain:
            prompt += f" (website: {company_domain})"

        if additional_context:
            prompt += f" and this context: {additional_context}"

        prompt += """, please provide:

1. **Company Overview**: Brief description of what the company does
2. **Ideal Customer Profile**:
   - Target industries
   - Company size (SMB, Mid-market, Enterprise)
   - Key decision-maker roles
   - Geographic focus
3. **Customer Pain Points**: What problems do they solve?
4. **Value Proposition**: Why customers choose them

Keep it concise and business-focused (3-4 paragraphs max)."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert in B2B sales and ICP definition."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=1024
            )

            return response.choices[0].message.content

        except Exception as e:
            return f"Error generating ICP analysis: {str(e)}"
