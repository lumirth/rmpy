import aiohttp
import asyncio
import json
import sys

from .constants import AUTH_TOKEN, API_URL, UNIVERSITY_ID
from .queries import get_all_professors_query, total_count_query

async def fetch_professors(first, session, school_id=UNIVERSITY_ID):
    variables = {"schoolID": school_id, "first": first}
    payload = {"query": get_all_professors_query, "variables": variables}
    response = await session.post(API_URL, data=json.dumps(payload))
    response_json = json.loads(await response.text())
    professors = {}
    for professor in response_json['data']['newSearch']['teachers']['edges']:
        full_name = professor['node']['firstName'][0] + ' ' + professor['node']['lastName']
        professors[full_name] = professor['node']
    return professors

async def fetch_all_professors(school_id=UNIVERSITY_ID, debug=False):
    async with aiohttp.ClientSession(headers={'authorization': f"Basic {AUTH_TOKEN}"}) as session:
        variables = {"schoolID": school_id}
        payload = {"query": total_count_query, "variables": variables}
        response = await session.post(API_URL, data=json.dumps(payload))
        total_count_response_json = json.loads(await response.text())
        total_count = total_count_response_json['data']['newSearch']['teachers']['resultCount']

        if debug:
            print(f"Total number of professors: {total_count}")

        professors = {}
        tasks = []
        task = asyncio.create_task(fetch_professors(total_count, session))
        tasks.append(task)
        for task in asyncio.as_completed(tasks):
            result = await task
            professors.update(result)

            if debug:
                print(f"Progress: {len(professors)} / {total_count}", end='\r')

        if debug:
            print("\nFinished fetching all professors")

        return professors

def get_size(obj):
    """Recursively get the size of an object in bytes."""
    size = sys.getsizeof(obj)
    if isinstance(obj, dict):
        size += sum(get_size(v) for v in obj.values())
    elif isinstance(obj, (list, tuple, set)):
        size += sum(get_size(v) for v in obj)
    return size

def sizeof_fmt(num, suffix="B"):
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"
