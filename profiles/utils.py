import requests
from urllib.parse import quote


def get_age_group(age):
    if age <= 12:
        return 'child'
    elif age <= 19:
        return 'teenager'
    elif age <= 59:
        return 'adult'
    else:
        return 'senior'


def fetch_external_data(name):
    encoded_name = quote(name)

    # Genderize
    try:
        g_res = requests.get(
            f'https://api.genderize.io?name={encoded_name}',
            timeout=15,
            headers={'Accept': 'application/json'}
        )
        g_res.raise_for_status()
        g_data = g_res.json()
    except Exception:
        raise ValueError('Genderize returned an invalid response')

    if not g_data.get('gender') or not g_data.get('count'):
        raise ValueError('Genderize returned an invalid response')

    # Agify
    try:
        a_res = requests.get(
            f'https://api.agify.io?name={encoded_name}',
            timeout=15,
            headers={'Accept': 'application/json'}
        )
        a_res.raise_for_status()
        a_data = a_res.json()
    except Exception:
        raise ValueError('Agify returned an invalid response')

    if a_data.get('age') is None:
        raise ValueError('Agify returned an invalid response')

    # Nationalize
    try:
        n_res = requests.get(
            f'https://api.nationalize.io?name={encoded_name}',
            timeout=15,
            headers={'Accept': 'application/json'}
        )
        n_res.raise_for_status()
        n_data = n_res.json()
    except Exception:
        raise ValueError('Nationalize returned an invalid response')

    countries = n_data.get('country', [])
    if not countries:
        raise ValueError('Nationalize returned an invalid response')

    top_country = max(countries, key=lambda c: c.get('probability', 0))

    return {
        'gender': g_data['gender'],
        'gender_probability': g_data['probability'],
        'sample_size': g_data['count'],
        'age': a_data['age'],
        'age_group': get_age_group(a_data['age']),
        'country_id': top_country['country_id'],
        'country_probability': top_country['probability'],
    }