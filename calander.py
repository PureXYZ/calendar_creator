from uwaterlooapi import UWaterlooAPI
import pprint
uw = UWaterlooAPI(api_key="8ab9363c27cf84a3fdf526a89269e81a")


input_file = open("input.txt", "r")

lines = input_file.read().splitlines()

term_num = lines[0].strip()


del lines[0]

counter = 0

course_name = []
course_num = []
course_section = []

for line in lines:
	course_name.append((line.strip()[:-3]).strip()[:-3].strip())
	course_num.append((line.strip()[:-3]).strip()[-3:])
	course_section.append((line.strip()[-3:]).strip())
	counter += 1
	
print course_name
print course_num
print course_section

for index in range(len(course_name)):
	name = course_name[index]
	num = course_num[index]
	sec = course_section[index]
	
	course_info = uw.term_course_schedule(term_num, name, num)



