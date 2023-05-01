import requests
from .constants import AUTH_TOKEN, API_URL, UNIVERSITY_ID
from .queries import (
    combined_query,
    search_teacher_query,
    autocomplete_school_query,
    get_teacher_query,
)

HEADERS = {
    "authorization": f"Basic {AUTH_TOKEN}",
}

def search_school(school_name):
    response = requests.post(
        API_URL,
        json={
            "query": autocomplete_school_query,
            "variables": {
                "query": school_name,
            },
        },
        headers=HEADERS,
    )
    result = response.json()
    schools = result['data']['autocomplete']['schools']['edges']
    schools = list(map(lambda x: x['node'], schools))
    return schools

def get_teacher_by_id(teacher_id):
    response = requests.post(
        API_URL,
        json={
            "query": get_teacher_query,
            "variables": {
                "id": teacher_id,
            },
        },
        headers=HEADERS,
    )
    result = response.json()
    teacher = result['data']['node']
    return teacher

def search_teacher(name, school_id=UNIVERSITY_ID):
    response = requests.post(
        API_URL,
        json={
            "query": search_teacher_query,
            "variables": {
                "text": name,
                "schoolID": school_id,
            },
        },
        headers=HEADERS,
    )
    result = response.json()
    teachers = result['data']['newSearch']['teachers']['edges']
    teachers = list(map(lambda x: x['node'], teachers))
    return teachers

def get_teacher_info(name, school_id=UNIVERSITY_ID):
    response = requests.post(
        API_URL,
        json={
            "query": combined_query,
            "variables": {
                "text": name,
                "schoolID": school_id
            }
        },
        headers=HEADERS
    )
    result = response.json()
    teachers = result['data']['newSearch']['teachers']['edges']
    if not teachers:
        return None
    return teachers[0]['node']

def get_ratings_for_teachers(instructors, school_id=UNIVERSITY_ID):
    results = [get_teacher_info(instructor, school_id) for instructor in instructors]
    return results