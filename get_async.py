import asyncio
import aiohttp
from aiohttp import TCPConnector
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

async def search_school_async(session, school_name):
    response = await session.post(
        API_URL,
        json={
            "query": autocomplete_school_query,
            "variables": {
                "query": school_name,
            },
        },
        headers=HEADERS,
    )
    result = await response.json(content_type=None)
    schools = result['data']['autocomplete']['schools']['edges']
    schools = list(map(lambda x: x['node'], schools))
    return schools

async def get_teacher_by_id_async(session, teacher_id):
    response = await session.post(
        API_URL,
        json={
            "query": get_teacher_query,
            "variables": {
                "id": teacher_id,
            },
        },
        headers=HEADERS,
    )
    result = await response.json(content_type=None)
    teacher = result['data']['node']
    return teacher

async def search_teacher_async(session, name, school_id=UNIVERSITY_ID):
    response = await session.post(
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
    result = await response.json(content_type=None)
    teachers = result['data']['newSearch']['teachers']['edges']
    teachers = list(map(lambda x: x['node'], teachers))
    return teachers

async def get_teacher_info_async(session, name, school_id=UNIVERSITY_ID):
    response = await session.post(
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
    result = await response.json(content_type=None)
    teachers = result['data']['newSearch']['teachers']['edges']
    if not teachers:
        return None
    return teachers[0]['node']

async def get_ratings_for_teachers_async(instructors, school_id=UNIVERSITY_ID):
    conn = TCPConnector(limit=300)
    async with aiohttp.ClientSession(connector=conn) as session:
        tasks = [get_teacher_info_async(session, instructor, school_id) for instructor in instructors]
        results = await asyncio.gather(*tasks, return_exceptions=True)
    return results