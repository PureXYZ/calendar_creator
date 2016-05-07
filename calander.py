from uwaterlooapi import UWaterlooAPI
import pprint
uw = UWaterlooAPI(api_key="8ab9363c27cf84a3fdf526a89269e81a")



def add_event(date, location, name):
        return



def get_section(course_info, sec_id):
        for section in course_info:
                if section["section"][-3:] == sec_id:
                        return section


def get_section_date(section):
        return section["classes"][0]["date"]


def get_section_location(section):
        return section["classes"][0]["location"]


def get_section_name(section):
        return section["subject"] + " " + section["catalog_number"] + " - " \
               + section["section"] + " - " + section["title"]



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

        for section in course_info:
                if section["section"][-3:] == sec:

                        section_date = get_section_date(section)
                        section_location = get_section_location(section)
                        section_name = get_section_name(section)

                        add_event(section_date, section_location, section_name)
                        
                        related_class_1 = section["related_component_1"]
                        related_class_2 = section["related_component_2"]


                        if related_class_1:
                                related_section_1 = get_section(course_info, related_class_1)
                                
                                section_rel_1_date = get_section_date(related_section_1)
                                section_rel_1_location = get_section_location(related_section_1)
                                section_rel_1_name = get_section_name(related_section_1)
                                
                                add_event(section_rel_1_date, section_rel_1_location, section_rel_1_name)


                        if related_class_2:
                                related_section_2 = get_section(course_info, related_class_2)

                                section_rel_2_date = get_section_date(related_section_2)
                                section_rel_2_location = get_section_location(related_section_2)
                                section_rel_2_name = get_section_name(related_section_2)
                                
                                add_event(section_rel_2_date, section_rel_2_location, section_rel_2_name)
                                
                        
                        
