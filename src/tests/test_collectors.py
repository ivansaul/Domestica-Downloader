from domestica.utils.collectors import get_course_id


def test_get_course_id():
    url_1 = "https://www.domestika.org/es/courses/5455-fotografia-profesional/course"
    url_2 = "https://www.domestika.org/es/courses/5455-fotografia-profesional"
    url_3 = "https://www.domestika.org/es/5455-fotografia-profesional"

    assert get_course_id(url_1) == "5455"
    assert get_course_id(url_2) == "5455"
    assert get_course_id(url_3) == "5455"
