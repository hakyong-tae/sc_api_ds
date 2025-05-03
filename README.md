# SmartChip Proxy API

This is a simple proxy server for SmartChip race records, built with Flask.  
It fetches race lists and runner records from SmartChip and serves them as an API for frontend use (K-TRACKER project).

## Features

- Fetch SmartChip race list
- Fetch individual runner records by bib number
- CORS support for frontend integration
- JSON API responses

## Endpoints

### GET /races

Returns the list of races.

GET https://your-flyio-app.fly.dev/races

pgsql
복사
편집

### GET /runner

Returns runner record by usedata (race id) and bib (runner number).

GET https://your-flyio-app.fly.dev/runner?usedata=XXX&bib=YYY

## Usage

1. Install requirements

pip install -r requirements.txt


2. Run the server

python app.py

3. Deploy (optional)

You can deploy to Fly.io for public use.

## License

MIT