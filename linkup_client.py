"""
Linkup API Client for searching and retrieving online content.
"""
import os
import requests
from typing import Optional, List, Dict, Any
from dotenv import load_dotenv

load_dotenv()


class LinkupClient:
    """Client for interacting with the Linkup API."""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Linkup client.

        Args:
            api_key: Linkup API key. If not provided, will look for LINKUP_API_KEY env variable.
        """
        self.api_key = api_key or os.getenv("LINKUP_API_KEY")
        if not self.api_key:
            raise ValueError("Linkup API key must be provided or set in LINKUP_API_KEY environment variable")

        self.base_url = "https://api.linkup.so/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def search(
        self,
        query: str,
        depth: str = "standard",
        output_type: str = "sourcedAnswer",
        structured_output_schema: Optional[Dict[str, Any]] = None,
        include_images: bool = False,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        exclude_domains: Optional[List[str]] = None,
        include_domains: Optional[List[str]] = None,
        include_inline_citations: bool = False,
        include_sources: bool = False
    ) -> Dict[str, Any]:
        """
        Search for information using the Linkup API.

        Args:
            query: The natural language question for which you want to retrieve context.
            depth: Precision of the search. "standard" or "deep".
            output_type: Type of output. "sourcedAnswer", "searchResults", or "structured".
            structured_output_schema: JSON schema for structured output (required if output_type is "structured").
            include_images: Whether to include images in results.
            from_date: Start date for search results (ISO 8601 format: YYYY-MM-DD).
            to_date: End date for search results (ISO 8601 format: YYYY-MM-DD).
            exclude_domains: List of domains to exclude from search.
            include_domains: List of domains to search on.
            include_inline_citations: Whether to include inline citations (for sourcedAnswer).
            include_sources: Whether to include sources (for structured output).

        Returns:
            API response containing search results.
        """
        payload = {
            "q": query,
            "depth": depth,
            "outputType": output_type,
            "includeImages": include_images,
            "includeInlineCitations": include_inline_citations,
            "includeSources": include_sources
        }

        # Add optional parameters
        if structured_output_schema is not None:
            payload["structuredOutputSchema"] = structured_output_schema

        if from_date:
            payload["fromDate"] = from_date

        if to_date:
            payload["toDate"] = to_date

        if exclude_domains:
            payload["excludeDomains"] = exclude_domains

        if include_domains:
            payload["includeDomains"] = include_domains

        try:
            response = requests.post(
                f"{self.base_url}/search",
                headers=self.headers,
                json=payload
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error making Linkup API request: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response: {e.response.text}")
            raise

    def search_event_attendees(
        self,
        event_name: str,
        event_url: Optional[str] = None,
        additional_context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Search for people attending a specific event.

        Args:
            event_name: Name of the event.
            event_url: URL of the event page (optional but recommended).
            additional_context: Additional context about the event.

        Returns:
            Dictionary containing information about event attendees.
        """
        # Build a detailed prompt following Linkup's best practices
        query_parts = [
            f"You are an expert business analyst researching attendees for the event '{event_name}'."
        ]

        if event_url:
            query_parts.append(f"The event page is at {event_url}.")

        if additional_context:
            query_parts.append(additional_context)

        query_parts.extend([
            "Find information about:",
            "1. People who have publicly announced they are attending or speaking at this event",
            "2. Their professional backgrounds and current companies",
            "3. Their LinkedIn profiles or professional websites if mentioned",
            "4. Their roles and job titles",
            "5. The companies they represent",
            "",
            "Focus on factual information from:",
            "- Event registration pages",
            "- Speaker lists and bios",
            "- LinkedIn posts about attending the event",
            "- Twitter/X announcements",
            "- Event organizer announcements",
            "",
            "Be thorough and include as many attendees as you can find with their professional details.",
            "Return the information in a structured format with clear sources."
        ])

        query = "\n".join(query_parts)

        # Use deep search for more comprehensive results
        include_domains_list = []
        if event_url:
            # Extract domain from event URL
            from urllib.parse import urlparse
            domain = urlparse(event_url).netloc
            if domain:
                include_domains_list.append(domain)

        # Add common professional networking sites
        include_domains_list.extend([
            "linkedin.com",
            "twitter.com",
            "x.com",
            "eventbrite.com",
            "lu.ma",
            "partful.com"
        ])

        return self.search(
            query=query,
            depth="deep",
            output_type="sourcedAnswer",
            include_domains=include_domains_list if include_domains_list else None,
            include_inline_citations=True
        )

    def extract_attendees_from_url(
        self,
        event_url: str
    ) -> Dict[str, Any]:
        """
        Extract attendees from an event URL and return as a structured table.

        Args:
            event_url: URL of the event page to extract attendees from.

        Returns:
            Dictionary containing the attendee list and sources.
        """
        query = f"""Visit {event_url} and extract ALL people listed on the page (attendees, speakers, sponsors, organizers, etc.). This page may be dynamically loaded with JavaScript - wait for it to fully render and look at ALL content on the page.

Search EVERYWHERE on the page for:
- Profile cards, grids, or lists showing people
- Speaker lineups or panels
- Company representatives or sponsors
- Organizers or hosts
- Any names with photos, titles, or company logos
- LinkedIn profiles or social media links
- Team pages or About sections
- "Who's Attending", "Speakers", "Sponsors", "Team" sections

For EACH person you find, extract:
1. Their full name
2. Their job title/role (if visible - otherwise use "N/A")
3. Their company name (if visible - otherwise use "N/A")

Format as a markdown table:
| Name | Role/Title | Affiliation/Company |

Extract EVERYONE you can find - speakers, sponsors, organizers, or anyone else mentioned. If the page truly has zero people listed, return: "No individuals found on this page." But try very hard to find at least some people first."""

        # Don't restrict domains - let Linkup search broadly
        return self.search(
            query=query,
            depth="deep",
            output_type="sourcedAnswer",
            include_inline_citations=True
        )

    def enrich_company_descriptions(
        self,
        attendee_data: str
    ) -> Dict[str, Any]:
        """
        Enrich attendee data with company descriptions.

        Args:
            attendee_data: The attendee table data from extract_attendees_from_url.

        Returns:
            Dictionary containing enriched attendee data with company descriptions.
        """
        query = f"""You are a business research assistant. I have a table of people and their companies from an event. For each company in the table, research what the company does by visiting their official website and business sources.

Create a new table with these columns:
1. Name (person's name)
2. Role/Title
3. Affiliation/Company
4. Company Description (what the company does - 1-2 sentences)

Research each company to understand:
- What products/services they offer
- What industry they're in
- What problem they solve
- Their target customers

Here is the attendee table to enrich:

{attendee_data}

Return the enriched table in markdown format with all 4 columns. Focus on searching for factual information from company websites, LinkedIn company pages, Crunchbase, and reputable tech/business news sources."""

        return self.search(
            query=query,
            depth="deep",
            output_type="sourcedAnswer",
            include_inline_citations=True
        )

    def get_company_icp_from_url(
        self,
        company_url: str,
        company_name: str = "the company"
    ) -> Dict[str, Any]:
        """
        Get the Ideal Customer Profile for a company from their website.

        Args:
            company_url: URL of the company website.
            company_name: Name of the company (for better context).

        Returns:
            Dictionary containing ICP analysis.
        """
        query = f"""You are an expert in B2B SaaS market analysis. Identify and describe the Ideal Customer Profile (ICP) for {company_name} (website: {company_url}). Focus your research on the company's homepage, product pages, and any case studies or customer testimonials available on the site. Analyze the target industries, company sizes, buyer personas, and typical use cases addressed by {company_name}. Present your findings in a concise bullet-point list, highlighting key characteristics and patterns."""

        # Don't restrict domains - let Linkup search broadly
        return self.search(
            query=query,
            depth="deep",
            output_type="sourcedAnswer",
            include_inline_citations=True
        )

    def get_company_info(
        self,
        company_name: str,
        company_domain: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get detailed information about a company to help define ICP.

        Args:
            company_name: Name of the company.
            company_domain: Domain of the company website.

        Returns:
            Dictionary containing company information.
        """
        query_parts = [
            f"You are an expert business analyst. Describe {company_name}'s activities in detail."
        ]

        if company_domain:
            query_parts.append(
                f"The company domain is {company_domain}. "
                f"Analyze the homepage, about us page, pricing page, and blog section."
            )

        query_parts.extend([
            "Include:",
            "1. Products and services offered",
            "2. Business model and pricing approach",
            "3. Target market and ideal customer profile (ICP)",
            "4. Key value propositions and differentiators",
            "5. Industries they serve",
            "6. Company size they typically target (SMB, Mid-market, Enterprise)",
            "7. Key customer pain points they address",
            "",
            "Be sharp and business oriented in your answer.",
            "Focus on factual information from their website and public materials."
        ])

        query = "\n".join(query_parts)

        include_domains_list = []
        if company_domain:
            include_domains_list.append(company_domain)

        return self.search(
            query=query,
            depth="deep",
            output_type="sourcedAnswer",
            include_domains=include_domains_list if include_domains_list else None,
            include_inline_citations=True
        )
