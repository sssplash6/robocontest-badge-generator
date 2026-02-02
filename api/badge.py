
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import requests
from bs4 import BeautifulSoup
import re

def scrape_robocontest(username: str):
    url = f"https://robocontest.uz/profile/{username}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        return None
    soup = BeautifulSoup(response.text, 'html.parser')
    try:
        main_stats_elements = soup.select('div.d-flex.flex-column.align-items-center.mt-4 > h1')
        robo_rank, robo_rating = ("N/A", "N/A")
        if len(main_stats_elements) >= 2:
            robo_rank = main_stats_elements[0].text.strip()
            robo_rating = main_stats_elements[1].text.strip()
        solved_problems_element = soup.select_one("div.d-flex.flex-row.justify-content-around h3")
        solved_count, total_count = (0, 0)
        if solved_problems_element:
            numbers = re.findall(r'\d+', solved_problems_element.text.strip())
            if len(numbers) >= 2:
                solved_count, total_count = int(numbers[0]), int(numbers[1])
        return {"username": username, "robo_rank": robo_rank, "robo_rating": robo_rating, "solved_count": solved_count, "total_count": total_count}
    except Exception:
        return None

def generate_svg_card(stats: dict):
    if not stats or stats.get('robo_rank') == 'N/A':
        return """<svg xmlns="http://www.w3.org/2000/svg" width="350" height="180"><rect width="100%" height="100%" rx="8" fill="#1d1d1d" /><text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" font-family="Segoe UI, sans-serif" font-size="16" fill="#ff4545">User not found or error</text></svg>"""
    username, rank, rating, solved, total = stats['username'], stats['robo_rank'], stats['robo_rating'], stats['solved_count'], stats['total_count']
    progress_percentage = (solved / total * 100) if total > 0 else 0
    progress_width = max(0, min(100, progress_percentage))
    return f"""<svg width="400" height="165" xmlns="http://www.w3.org/2000/svg"><style>.container{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'Helvetica Neue',Arial,sans-serif;animation:fadeIn .8s ease-in-out}}@keyframes fadeIn{{from{{opacity:0}}to{{opacity:1}}}}.header{{font-size:18px;font-weight:600;fill:#f0f6fc}}.stat-label{{font-size:14px;fill:#8b949e}}.stat-value{{font-size:24px;font-weight:700;fill:#c9d1d9}}.problems-solved{{font-size:16px;font-weight:600;fill:#c9d1d9}}</style><rect width="100%" height="100%" rx="8" fill="#0d1117" stroke="#30363d" stroke-width="1"/><g class="container" transform="translate(20,20)"><g transform="translate(0,0)"><svg x="0" y="0" width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" clip-rule="evenodd" d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zM8.5 15.5l-2-2 1.5-1.5 2 2-1.5 1.5zm3.5-6.5c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zm5.5 4.5l-2-2 1.5-1.5 2 2-1.5 1.5z" fill="#f0f6fc"/></svg><text x="30" y="17" class="header">RoboContest Stats / {username}</text></g><g transform="translate(0,50)"><text class="stat-label">Robo Rank</text><text y="25" class="stat-value">{rank}</text></g><g transform="translate(140,50)"><text class="stat-label">Robo Rating</text><text y="25" class="stat-value">{rating}</text></g><g transform="translate(0,100)"><text class="problems-solved">Problems Solved</text><text x="360" y="0" text-anchor="end" class="stat-label">{solved} / {total}</text><rect y="8" width="360" height="8" rx="4" fill="#30363d"/><rect y="8" width="{3.6*progress_width}" height="8" rx="4" fill="#2e9a49"/></g></g></svg>"""

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)
        username = query_params.get('username', [None])[0]

        if not username:
            self.send_response(400)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"Missing 'username' query parameter")
            return

        stats = scrape_robocontest(username)
        svg_content = generate_svg_card(stats)

        self.send_response(200)
        self.send_header('Content-type', 'image/svg+xml')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.end_headers()
        self.wfile.write(svg_content.encode('utf-8'))
        return
