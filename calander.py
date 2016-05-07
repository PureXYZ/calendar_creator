from uwaterlooapi import UWaterlooAPI
from ics import Calendar, Event
from datetime import date, datetime
import pprint

uw = UWaterlooAPI(api_key="8ab9363c27cf84a3fdf526a89269e81a")

calendar = Calendar()



def get_section(course_info, sec_id):
        for section in course_info:
                if section["section"][-3:] == sec_id:
                        return section
        return -1


def get_section_full(course_info, section_name):
        for section in course_info:
                if section["section"] == section_name:
                        return section
        return -1
                

def get_sections_ass(course_info, ass_id, already_chosen1, already_chosen2):
        sections = []
        
        for section in course_info:
                if section["associated_class"] == ass_id \
                   and section["section"][:-3].strip() != already_chosen1 \
                   and section["section"][:-3].strip() != already_chosen2:
                        sections.append(section)
                        
        return sections


def get_section_date(section):
        return section["classes"]


def get_section_location(section):
        return section["classes"]


def get_section_name(section):
        return section["subject"] + " " + section["catalog_number"] + " - " \
               + section["section"] + " - " + section["title"]


def get_term_num(terms_info, term_cleaned):
        for year in terms_info:
                for term in terms_info[year]:
                        if term["name"] == term_cleaned:
                                return term["id"]
        return -1


def remove_section_type(pick_sections, section_type):
        sections = []
        for section in pick_sections:
                if section["section"][:-3].strip() != section_type:
                        sections.append(sections)
        return sections



term_num = -1

while (term_num == -1):
        term_input = (raw_input("Enter the term (e.g. Spring 2016): ")).strip()
        term_year = term_input[-4:]
        term_season = term_input[:-4].strip()
        term_cleaned = term_season[0].upper() + term_season[1:].lower() + " " + term_year

        terms_info = (uw.terms())["listings"]

        term_num = get_term_num(terms_info, term_cleaned)

        if term_num == -1:
                print "Error, term not found, try again"


course_name = []
course_num = []
course_section = []


print ("\nEnter 'done' to finish input\n")


while True:
        course_input = (raw_input("Enter course (e.g. Math 237 in section 1 = Math 237 001): ")).strip()
        if course_input.strip().lower() == "done":
                break
        
        course_name.append((course_input.strip()[:-3]).strip()[:-3].strip())
        course_num.append((course_input.strip()[:-3]).strip()[-3:])
        course_section.append((course_input.strip()[-3:]).strip())



def add_event(date, location, name):
        new_event = Event(name)

        
        return


        

for index in range(len(course_name)):
        name = course_name[index]
        num = course_num[index]
        sec = course_section[index]
        
        course_info = uw.term_course_schedule(term_num, name, num)


        custom_pick = 0;
        
        for section in course_info:

                if section["associated_class"] == 99:
                        custom_pick = 1;
                
                if section["section"][-3:] == sec:

                        the_section = section

                        section_date = get_section_date(section)
                        section_location = get_section_location(section)
                        section_name = get_section_name(section)

                        add_event(section_date, section_location, section_name)
                        
                        related_class_1 = section["related_component_1"]
                        related_class_2 = section["related_component_2"]
                        related_section_1 = []
                        related_section_2 = []


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
        

        if custom_pick == 1:
                already_chosen1 = ""
                already_chosen2 = ""

                if related_section_1:
                        already_chosen1 = related_section_1["section"][:-3].strip()

                if related_section_2:
                        already_chosen2 = related_section_2["section"][:-3].strip()
                        
                pick_sections = get_sections_ass(course_info, 99, already_chosen1, already_chosen2)

                if pick_sections:
                        print "Note: Section numbers are different for lectures and tutorials. (e.g. LEC 001 and TUT 101, 001 != 101)"

                while pick_sections:
                        print "Note: " + the_section["note"]
                        section_type = pick_sections[0]["section"][:-3].strip()
                        pick_input = (raw_input("Please enter your enrolled" + section_type + " section (e.g. TUT 101 = 101): ")).strip()
                        section_input_cleaned = section_type + " " + pick_input
                           
                        section_chosen = get_section_full(course_info, section_input_cleaned)

                        section_chosen_date = get_section_date(section_chosen)
                        section_chosen_location = get_section_location(section_chosen)
                        section_chosen_name = get_section_name(section_chosen)
                                
                        add_event(section_chosen_date, section_chosen_location, section_chosen_name)

                        pick_sections = remove_section_type(pick_sections, section_type)


                




file_out = open(term_cleaned + '.ics', 'w')
file_out.writelines(calendar)
file_out.close()
                                
                        
                        
