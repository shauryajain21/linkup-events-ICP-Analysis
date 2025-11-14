"""
ICP Matcher using Claude AI to analyze if event attendees match company's ideal customer profile.
"""
import os
import json
from typing import Dict, List, Any, Optional
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()


class ICPMatcher:
    """Analyzes event attendees to determine if they match the company's ICP using Claude."""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the ICP Matcher with Claude.

        Args:
            api_key: Anthropic API key. If not provided, will look for ANTHROPIC_API_KEY env variable.
        """
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError(
                "Anthropic API key must be provided or set in ANTHROPIC_API_KEY environment variable"
            )

        self.client = Anthropic(api_key=self.api_key)

    def analyze_icp_match(
        self,
        company_info: str,
        attendee_info: str,
        company_name: str = "your company"
    ) -> Dict[str, Any]:
        """
        Analyze if event attendees match the company's ICP using Claude.

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
            message = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=4096,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            # Extract the text response
            response_text = message.content[0].text

            # Try to parse as JSON
            # Claude might wrap it in markdown code blocks, so handle that
            response_text = response_text.strip()
            if response_text.startswith("```json"):
                response_text = response_text[7:]  # Remove ```json
            if response_text.startswith("```"):
                response_text = response_text[3:]  # Remove ```
            if response_text.endswith("```"):
                response_text = response_text[:-3]  # Remove trailing ```
            response_text = response_text.strip()

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
            message = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1024,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            return message.content[0].text

        except Exception as e:
            return f"Error generating ICP analysis: {str(e)}"
