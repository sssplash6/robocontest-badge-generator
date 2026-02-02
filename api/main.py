# File: api/main.py

from fastapi import FastAPI, Response
from fastapi.responses import HTMLResponse
import requests
from bs4 import BeautifulSoup
import re

# Initialize the FastAPI app
app = FastAPI()

def scrape_robocontest(username: str):
    """Scrapes statistics from a robocontest.uz user profile."""
    url = f"https://robocontest.uz/profile/{username}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    try:
        main_stats_elements = soup.select('div.d-flex.flex-column.align-items-center.mt-4 > h1')
        
        robo_rank = "N/A"
        robo_rating = "N/A"

        if len(main_stats_elements) >= 2:
            robo_rank = main_stats_elements[0].text.strip()
            robo_rating = main_stats_elements[1].text.strip()

        solved_problems_element = soup.select_one("div.d-flex.flex-row.justify-content-around h3")
        
        solved_problems = "N/A"
        if solved_problems_element:
            solved_problems_text = solved_problems_element.text.strip()
            # Extract only the numeric and slash part
            match = re.search(r'[\d\s/]+', solved_problems_text)
            if match:
                solved_problems = match.group().strip()

        stats = {
            "username": username,
            "robo_rank": robo_rank,
            "robo_rating": robo_rating,
            "solved_problems": solved_problems
        }
        return stats

    except Exception:
        return None

def generate_svg_badge(stats: dict):
    """Generates an SVG badge from the scraped stats."""
    if not stats:
        # Return a fallback SVG if stats can't be fetched
        return """<svg xmlns="http://www.w3.org/2000/svg" width="300" height="60"><text x="10" y="35">Error fetching stats</text></svg>"""

    # Updated SVG template
    svg_template = f"""
    <svg xmlns="http://www.w3.org/2000/svg" width="450" height="60" viewBox="0 0 450 60">
      <style>
        .header {{ font-size: 16px; font-weight: bold; font-family: 'Segoe UI', Ubuntu, Sans-Serif; fill: #007bff; }}
        .stat-label {{ font-size: 14px; font-family: 'Segoe UI', Ubuntu, Sans-Serif; fill: #333; }}
        .stat-value {{ font-weight: bold; }}
      </style>
      <rect width="100%" height="100%" fill="#f7f7f7" stroke="#e1e1e1" rx="6" ry="6"/>
      <g transform="translate(15, 20)">
        <text class="header">RoboContest Stats: @{stats['username']}</text>
      </g>
      <g transform="translate(20, 48)">
        <text class="stat-label">Rank: <tspan class="stat-value">{stats['robo_rank']}</tspan></text>
        <text x="140" class="stat-label">Rating: <tspan class="stat-value">{stats['robo_rating']}</tspan></text>
        <text x="280" class="stat-label">Solved: <tspan class="stat-value">{stats['solved_problems']}</tspan></text>
      </g>
    </svg>
    """
    return svg_template

# API endpoint to generate the badge
@app.get("/api/badge")
def get_badge(username: str):
    """
    This endpoint scrapes the user's stats and returns a dynamic SVG badge.
    """
    stats = scrape_robocontest(username)
    svg_content = generate_svg_badge(stats)
    return Response(content=svg_content, media_type="image/svg+xml", headers={
        # Prevent caching so the badge is always fresh
        "Cache-Control": "no-cache, no-store, must-revalidate",
        "Pragma": "no-cache",
        "Expires": "0"
    })

# Root endpoint for a simple greeting (optional)
@app.get("/")
def root():
    return HTMLResponse("<h1>RoboContest Badge Generator API</h1><p>Use /api/badge?username=your_username to get your badge.</p>")

