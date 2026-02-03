# HealthAI Radar

HealthAI Radar is a multi-sector health-tech tracker designed to monitor and analyze the top digital health and AI companies.

## Overview

This project tracks companies across various intersections of health technology, including:
- Artificial Intelligence
- Robotics
- Medical Imaging
- Remote Care
- Mental Health
- And more...

The core of the project is based on the "Top 100 Digital Health and AI Companies" list, mapping their specialized categories and overlaps.

## Data Structure

Companies are stored in `companies.json` with the following format:

```json
{
  "name": "Company Name",
  "categories": ["Category 1", "Category 2"]
}
```

## Scraper

The `scraper.py` script is designed to iterate through the company list and fetch relevant news or updates (currently a prototype structure).

## Usage

1. Install dependencies (requires `beautifulsoup4`, `requests`):
   ```bash
   pip install beautifulsoup4 requests
   ```
2. Run the scraper:
   ```bash
   python scraper.py
   ```

## License

[MIT](LICENSE)
