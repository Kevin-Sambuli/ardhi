import os
import requests
from .exceptions import ExternalApiException


def get_location(ip):
    url = f'https://api.ipstack.com/{ip}'
    # params = {'access_key': os.environ.get('ACCESS_KEY')}
    params = {'access_key': '0287dd692626cccbd21333cb0e5eeadb'}
    try:
        res = requests.get(url, params=params)
        data = res.json()
        return {
            'ip': data['ip'],
            'country_name': data['country_name'],
            'region_code': data['region_code'],
            'city': data['city'],
            'latitude': data['latitude'],
            'longitude': data['longitude'],
            'zip_code': data['zip']
        }
    except requests.exceptions.ConnectionError:
        raise ExternalApiException('Connection error occured during the fetch process')
    except requests.exceptions.Timeout:
        raise ExternalApiException("Connection timeout. Please check your internet connection and try again later")
    except requests.exceptions.TooManyRedirects:
        raise ExternalApiException("Too many redirects")
    # except requests.exceptions.RequestException:
    #     raise SystemExit(e)
