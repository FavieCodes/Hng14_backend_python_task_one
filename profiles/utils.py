import requests


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
    """
    Calls all three external APIs and returns combined data.
    Raises ValueError with a message on any bad response.
    """
    try:
        g_res = requests.get(f'https://api.genderize.io?name={name}', timeout=10)
        g_data = g_res.json()
    except Exception:
        raise ValueError('Genderize returned an invalid response')

    if not g_data.get('gender') or g_data.get('count', 0) == 0:
        raise ValueError('Genderize returned an invalid response')

    try:
        a_res = requests.get(f'https://api.agify.io?name={name}', timeout=10)
        a_data = a_res.json()
    except Exception:
        raise ValueError('Agify returned an invalid response')

    if a_data.get('age') is None:
        raise ValueError('Agify returned an invalid response')

    try:
        n_res = requests.get(f'https://api.nationalize.io?name={name}', timeout=10)
        n_data = n_res.json()
    except Exception:
        raise ValueError('Nationalize returned an invalid response')

    countries = n_data.get('country', [])
    if not countries:
        raise ValueError('Nationalize returned an invalid response')

    # Pick country with highest probability
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