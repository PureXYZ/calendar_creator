from uwaterlooapi import UWaterlooAPI
import pprint
uw = UWaterlooAPI(api_key="8ab9363c27cf84a3fdf526a89269e81a")


term_num = (raw_input("Enter the term number (e.g. Spring 2016 = 1165): ")).strip()


course_name = []
course_num = []
course_section = []


print ("\nEnter 'done' to finish input\n")


while True:
	course_input = (raw_input("Enter course (e.g. Math 237 in section 1 = Math 237 001): ")).strip()
	if course_input == "done":
		break
	
	course_name.append((course_input.strip()[:-3]).strip()[:-3].strip())
	course_num.append((course_input.strip()[:-3]).strip()[-3:])
	course_section.append((course_input.strip()[-3:]).strip())
	

for index in range(len(course_name)):
	name = course_name[index]
	num = course_num[index]
	sec = course_section[index]
	
	course_info = uw.term_course_schedule(term_num, name, num)
	pprint.pprint(course_info)

	for section in course_info:
		if section["section"][-3:] == sec:
			pprint.pprint("gg")
