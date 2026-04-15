# Profiles API

A REST API that enriches a name with gender, age, and nationality data from three external APIs.

## Base URL
https://your-app.railway.app

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/profiles | Create a profile |
| GET | /api/profiles | List all profiles (filterable) |
| GET | /api/profiles/{id} | Get single profile |
| DELETE | /api/profiles/{id} | Delete a profile |

## Filters for GET /api/profiles
- `gender` — e.g. `?gender=male`
- `country_id` — e.g. `?country_id=NG`
- `age_group` — `child`, `teenager`, `adult`, `senior`

## Setup Locally
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver