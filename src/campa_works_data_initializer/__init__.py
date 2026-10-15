from scrapper.professor import professor, invited, concurrent, visiting
from scrapper.major import major
from scrapper.semester import semester


semester.post_semesters()

professor.post_professors()
invited.post_professors()
concurrent.post_professors()
visiting.post_professors()

major.post_majors()
