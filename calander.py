from uwaterlooapi import UWaterlooAPI
from ics import Calendar, Event
from datetime import date, datetime, time
import pprint

uw = UWaterlooAPI(api_key="8ab9363c27cf84a3fdf526a89269e81a")

calendar = Calendar()
                              
term_dates = {"1165":{"start":date(2016, 5, 2), "end":date(2016, 7, 26)},
              "1169":{"start":date(2016, 8, 8), "end":date(2016, 12, 5)}}


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
                        sections.append(section)
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



def add_event(date, location, my_name):

        pprint.pprint(date)
        print my_name

        for specific_event in date:

                if specific_event["date"]["start_date"]:

                        if specific_event["date"]["start_date"] != specific_event["date"]["end_date"]:
                                print "Error! Unexpected api return! Start date not same as end date!"
                                break

                        start_time = specific_event["date"]["start_time"]
                        end_time = specific_event["date"]["end_time"]
                        location_str = specific_event["location"]["building"] + " " + specific_event["location"]["room"]
                        start_date = specific_event["date"]["start_date"]
                        date_year = term_dates[str(term_num)]["start"].year

                        datetime_str_start = str(date_year) + start_date[:2] + start_date[2:] + " " + start_time + ":00"
                        
                        datetime_str_end = str(date_year) + start_date[:2] + start_date[2:] + " " + end_time + ":00"

   
                        new_event = Event(name = my_name, begin = datetime_str_start,
                                          end = datetime_str_end, duration = None, uid = None,
                                          description = None, created = None, location = location_str)
                        calendar.events.append(new_event)

        
        return


        

for index in range(len(course_name)):
        name = course_name[index]
        num = course_num[index]
        sec = course_section[index]
        
        course_info = uw.term_course_schedule(term_num, name, num)

        if not course_info:
                print "Warning! Course " + name + " " + num + " could not be found!"
                continue


        custom_pick = 0;
        section_found = 0;
        
        for section in course_info:

                if section["associated_class"] == 99:
                        custom_pick = 1;
                
                if section["section"][-3:] == sec:

                        section_found = 1;

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

        if section_found == 0:
                print "Warning! Course section " + sec + " could not be found!"
                continue
        

        if custom_pick == 1:
                already_chosen1 = ""
                already_chosen2 = ""

                if related_section_1:
                        already_chosen1 = related_section_1["section"][:-3].strip()

                if related_section_2:
                        already_chosen2 = related_section_2["section"][:-3].strip()
                        
                pick_sections = get_sections_ass(course_info, 99, already_chosen1, already_chosen2)

                if pick_sections:
                        print "\nNote: Section numbers are different for lectures and tutorials. (e.g. LEC 001 and TUT 101, 001 != 101)"

                while pick_sections:
                        print "\nNote for " + the_section["subject"] + " " + the_section["catalog_number"] + ": " + the_section["note"]
                        section_type = pick_sections[0]["section"][:-3].strip()

                        section_chosen = -1
                        while section_chosen == -1:
                                
                                pick_input = (raw_input("\nPlease enter your enrolled " + section_type + \
                                                        " section for " + the_section["subject"] + " " + \
                                                        the_section["catalog_number"] + " (e.g. TUT 101 = 101): ")).strip()
                                section_input_cleaned = section_type + " " + pick_input
                                   
                                section_chosen = get_section_full(course_info, section_input_cleaned)

                                if section_chosen == -1:
                                        print "\nError! section not found please try again!"
                        

                        section_chosen_date = get_section_date(section_chosen)
                        section_chosen_location = get_section_location(section_chosen)
                        section_chosen_name = get_section_name(section_chosen)
                                
                        add_event(section_chosen_date, section_chosen_location, section_chosen_name)

                        pick_sections = remove_section_type(pick_sections, section_type)


        if custom_pick == 0:
                ass_id = the_section["associated_class"]

                course_info_main_removed = remove_section_type(course_info, the_section["section"][:-3].strip())

                already_chosen1 = ""
                already_chosen2 = ""

                if related_section_1:
                        already_chosen1 = related_section_1["section"][:-3].strip()

                if related_section_2:
                        already_chosen2 = related_section_2["section"][:-3].strip()
                        
                course_info_main_removed = get_sections_ass(course_info, ass_id, already_chosen1, already_chosen2)
                
                
                for section in course_info_main_removed:
                        if section["associated_class"] == ass_id:
                                section_date = get_section_date(section)
                                section_location = get_section_location(section)
                                section_name = get_section_name(section)
                                add_event(section_date, section_location, section_name)
                


                



file_out = open(term_cleaned + '.ics', 'w')
file_out.writelines(calendar)
file_out.close()

import os
file_path = os.path.dirname(os.path.abspath(__file__))

print "\n\nCalendar file (.ics) created. Located in " + file_path
