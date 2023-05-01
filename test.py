import asyncio
from rmpy.get_sync import search_school, get_teacher_by_id, search_teacher, get_teacher_info, get_ratings_for_teachers
from rmpy.get_all import fetch_all_professors
from rmpy.constants import UNIVERSITY_ID

def test_search_school():
    school_name = "New York University"
    result = search_school(school_name)
    for school in result:
        if school['name'] == school_name:
            assert True
            return

def test_get_teacher_by_id():
    teacher_id = "VGVhY2hlci0xODE1NzQy"
    result = get_teacher_by_id(teacher_id)
    assert result['id'] == teacher_id

def test_search_teacher():
    name = "Wade"
    school_id = UNIVERSITY_ID
    result = search_teacher(name, school_id)
    print(result)
    for teacher in result:
        if name in teacher['firstName']:
            assert True
            return

def test_get_teacher_info():
    instructor = "Woodley"
    school_id = UNIVERSITY_ID
    result = get_teacher_info(instructor)
    print(result)
    assert result['lastName'] == instructor

def test_get_ratings_for_teachers():
    instructors = ["Woodley", "Fagen"]
    school_id = UNIVERSITY_ID
    result = get_ratings_for_teachers(instructors, school_id)
    assert len(result) == len(instructors)
    for teacher in result:
        assert teacher['lastName'] in instructors

# def test_fetch_all_professors():
#     async def run_test():
#         school_id = UNIVERSITY_ID
#         professors = fetch_all_professors(school_id, debug=True)
#         assert len(professors) > 0
#     asyncio.run(run_test())
