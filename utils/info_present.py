from typing import List, Dict


def key_search(j_dict: Dict | List) -> Dict:
    search_list: List[str] = ["name", "year", "description", "rating", "poster", "genres", "ageRating"]
    result = {}
    for my_key in search_list:
        if my_key in j_dict:
            result[my_key] = j_dict[my_key]
            continue
        if not isinstance(j_dict, dict):
            return result
        for element in j_dict.values():
            if len(result) == len(search_list):
                return result
            if isinstance(element, dict):
                result = key_search(element)
            if isinstance(element, list):
                for item in element:
                    result = key_search(item)

    return result



