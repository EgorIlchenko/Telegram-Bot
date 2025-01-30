import requests
import json
from typing import Any, Dict
from config_data.config import API_BASE_URL, HEADERS


def api_request(endpoint: str, params: Dict[str, Any]) -> requests.Response:
    return requests.get(f"{API_BASE_URL}{endpoint}",
                        headers=HEADERS,
                        params=params)


def search_film_name(film_name: str, number_films: int) -> Dict[str, Any]:
    params: Dict[str, Any] = {"limit": number_films, "query": film_name}
    result_req = api_request(endpoint='/search',
                             params=params)

    return json.loads(result_req.text)


def search_film_rating(film_rating: str, number_films: int) -> Dict[str, Any]:
    params: Dict[str, Any] = {"limit": number_films,
                              "notNullFields": ("name", "poster.url"),
                              "rating.kp": film_rating}
    result_req = api_request(endpoint='',
                             params=params)

    return json.loads(result_req.text)


def search_film_genre(film_genre: str, number_films: int) -> Dict[str, Any]:
    params: Dict[str, Any] = {"limit": number_films,
                              "notNullFields": ("name", "poster.url"),
                              "genres.name": film_genre
                              }
    result_req = api_request(endpoint='',
                             params=params)

    return json.loads(result_req.text)


def search_film_low_budget(film_low_budget: str, number_films: int) -> Dict[str, Any]:
    params: Dict[str, Any] = {"limit": number_films,
                              "notNullFields": ("name", "poster.url"),
                              "budget.value": film_low_budget}
    result_req = api_request(endpoint='',
                             params=params)

    return json.loads(result_req.text)


def search_film_high_budget(film_high_budget: str, number_films: int) -> Dict[str, Any]:
    params: Dict[str, Any] = {"limit": number_films,
                              "notNullFields": ("name", "poster.url"),
                              "budget.value": film_high_budget}
    result_req = api_request(endpoint='',
                             params=params)

    return json.loads(result_req.text)
