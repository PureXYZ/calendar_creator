from uwaterlooapi import UWaterlooAPI
import pprint
uw = UWaterlooAPI(api_key="8ab9363c27cf84a3fdf526a89269e81a")

#pprint.pprint(uw.term_course_schedule(1165, "math", 237), width=20)


input_file = open("input.txt", "r")

lines = input_file.read().splitlines()

term_num = lines[0]


counter = 0

for line in lines:
	if counter != 0:
		print line
	counter += 1