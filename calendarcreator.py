#       Takes in user input for courses and creates a calendar for them

from uwaterlooapi import UWaterlooAPI
from ics import Calendar, Event
from datetime import date, timedelta, time, datetime
import arrow
from pytz import timezone

#       I should not reveal this
uw = UWaterlooAPI(api_key="8ab9363c27cf84a3fdf526a89269e81a")

cal = Calendar()

#       Term start/end dates (not in api)                              
term_dates = {"1165":{"start":date(2016, 5, 2), "end":date(2016, 7, 26)},
              "1169":{"start":date(2016, 8, 8), "end":date(2016, 12, 5)}}


#       get_section(str, str) returns first section(dic) with same
#               last 3 characters as sec_id.
#        returns -1 if not found
def get_section(course_info, sec_id):
        for section in course_info:
                if section["section"][-3:] == sec_id:
                        return section
        return -1


#       get_section(str, str) returns first section(dic) equal
#               to section_name.
#       returns -1 if not found      
def get_section_full(course_info, section_name):
        for section in course_info:
                if section["section"] == section_name:
                        return section
        return -1
                
#       get_sections_ass(str,str,str,str) returns sections in course_info
#               that have the same associated id as ass_id, but not the same
#               course number as already_chosen1 and already_chosen2
def get_sections_ass(course_info, ass_id, already_chosen1, already_chosen2):
        sections = []
        
        for section in course_info:
                if section["associated_class"] == ass_id and\
                   section["section"][:-3].strip() != already_chosen1 and\
                   section["section"][:-3].strip() != already_chosen2:
                        sections.append(section)
                        
        return sections


#       returns data on classes in section
def get_section_date(section):
        return section["classes"]


#       returns data on classes in section
def get_section_location(section):
        return section["classes"]


#       returns name and title of course in nicely formatted string
def get_section_name(section):
        return section["subject"] + " " + section["catalog_number"] + " - " \
               + section["section"] + " - " + section["title"]

#       returns term number (e.g. 1165) from the name
#               term_cleaned (e.g. "Spring 2016")
def get_term_num(terms_info, term_cleaned):
        for year in terms_info:
                for term in terms_info[year]:
                        if term["name"] == term_cleaned:
                                return term["id"]
        return -1


#       Removes section from pick_sections if it's first 3 characters
#               of section name matches section_type
def remove_section_type(pick_sections, section_type):
        sections = []
        for section in pick_sections:
                if ((section["section"])[:-3]).strip() != section_type:
                        sections.append(section)
        return sections


#       User input term
term_num = -1
while (term_num == -1):
        term_input = (raw_input("Enter the term (e.g. Spring 2016): ")).strip()

        if not term_input:
                print "Error, term not found, try again"
                continue
        
        term_year = term_input[-4:]
        term_season = term_input[:-4].strip()
        term_cleaned = term_season[0].upper() + term_season[1:].lower() + " " + term_year

        terms_info = (uw.terms())["listings"]

        term_num = get_term_num(terms_info, term_cleaned)

        if term_num == -1 or str(term_num) not in term_dates:
                print "Error, term not found, try again"
                term_num = -1


course_name = []
course_num = []
course_section = []

#       User input course name and sections
print ("\nEnter 'done' to finish input\n")

while True:
        course_input = (raw_input("Enter course (e.g. Math 237 in section 1 = Math 237 001): ")).strip()
        if course_input.strip().lower() == "done":
                break
        
        course_name.append((course_input.strip()[:4]).strip())
        course_num.append(((course_input.strip()[:-4]).strip()[-4:]).strip())
        course_section.append((course_input.strip()[-3:]).strip())


is_engineer = False

#       User input is_engineer
while True:
        eng_input = (raw_input("\nAre you an engineer or taking engineering course? (y/n): ")).strip()
        
        if eng_input.lower() != "y" and eng_input.lower() != "n":
                print "Error, invalid input!"
                continue
        else:
                if eng_input.lower() == "y":
                        is_engineer = True
                        break
                elif eng_input.lower() == "n":
                        is_engineer = False
                        break
                else:
                        print "Error! This should never happen"
                        break


#       record of all events added
events_stack = [] 


#       add_event(class info,,name) adds event to calendar with name
#               based on class info.
#       Outputs warning if event already added
#       If no specific date specified, assumed repeats every week in term
def add_event(date, location, my_name):

        for specific_event in date:

                #       If there is a specified date
                if specific_event["date"]["start_date"]:

                        if specific_event["date"]["start_date"] != \
                           specific_event["date"]["end_date"]:
                                print "Error! Unexpected api return! Start date not same as end date!"
                                break

                        start_time = specific_event["date"]["start_time"]
                        end_time = specific_event["date"]["end_time"]

                        format_time = '%H:%M'
                        time_dur = datetime.strptime(end_time, format_time) - \
                                   datetime.strptime(start_time, format_time)

                        if specific_event["location"]["building"] and \
                           specific_event["location"]["room"]:
                                location_str = str(specific_event["location"]["building"]) \
                                               + " " + str(specific_event["location"]["room"])
                        else:
                                location_str = " "
                        
                        start_date = specific_event["date"]["start_date"]
                        date_year = term_dates[str(term_num)]["start"].year

                        my_time_zone = timezone('US/Eastern')
                        dt = my_time_zone.localize(datetime(date_year, int(start_date[:2]),
                                                            int(start_date[-2:]), int(start_time[:2]),
                                                            int(start_time[-2:]),0,0))
                        datetime_str_start = arrow.get(dt)
                        
                        new_event = Event()
                        new_event.name = my_name
                        new_event.location = location_str
                        new_event.begin = datetime_str_start
                        new_event.duration = {"hours":time_dur.seconds//3600,
                                              "minutes":(time_dur.seconds//60)%60}


                        if datetime_str_start in events_stack:
                                print "Warning! Duplicate event detected! Event: " \
                                      + my_name + " discarded!"
                        else:
                                events_stack.append(datetime_str_start)                            
                                cal.events.append(new_event)

                #       If there is no specified date (interates through every day in term)
                else:
                        start_time = specific_event["date"]["start_time"]
                        end_time = specific_event["date"]["end_time"]

                        format_time = '%H:%M'
                        time_dur = datetime.strptime(end_time, format_time) - \
                                   datetime.strptime(start_time, format_time)
                        
                        
                        location_str = str(specific_event["location"]["building"]) \
                                       + " " + str(specific_event["location"]["room"])

                        start_date = term_dates[str(term_num)]["start"]
                        end_date = term_dates[str(term_num)]["end"]

                        weekdays = specific_event["date"]["weekdays"]
                        
                        counter = 0;
                        date_days = [0,0,0,0,0,0,0]
                        while  counter < len(weekdays):
                                if weekdays[counter] == "T":
                                        if (counter + 1) != len(weekdays):
                                                if weekdays[counter + 1] == "h":
                                                        date_days[3] = 1
                                                        counter += 1
                                                else:
                                                        date_days[1] = 1
                                        else:
                                                date_days[3] = 1
                                elif weekdays[counter] == "S":
                                        date_days[5] = 1
                                elif weekdays[counter] == "M":
                                        date_days[0] = 1
                                elif weekdays[counter] == "W":
                                        date_days[2] = 1
                                elif weekdays[counter] == "F":
                                        date_days[4] = 1
                                elif weekdays[counter] == "U":
                                        date_days[6] = 1
                                
                                counter += 1


                        days_in_term = (end_date - start_date).days + 1

                        for index in range(days_in_term):
                                
                                one_day = timedelta(days = 1)
                                current_date = start_date + one_day * index

                                if date_days[current_date.weekday()] == 1:

                                        my_time_zone = timezone('US/Eastern')
                                        dt = my_time_zone.localize\
                                             (datetime(current_date.year, current_date.month,
                                                       current_date.day, int(start_time[:2]),
                                                       int(start_time[-2:]), 0, 0))
                                        datetime_str_start = arrow.get(dt)
                                        
                                        new_event = Event()
                                        new_event.name = my_name
                                        new_event.location = location_str
                                        new_event.begin = datetime_str_start
                                        new_event.duration = {"hours":time_dur.seconds//3600,
                                                              "minutes":(time_dur.seconds//60)%60}
                                        
                                        if datetime_str_start in events_stack:
                                                print "Warning! Duplicate event detected! Event: " \
                                                      + my_name + " discarded!"
                                        else:
                                                events_stack.append(datetime_str_start)                            
                                                cal.events.append(new_event)
        return


       
#       Iterates through every input course
for index in range(len(course_name)):
        name = course_name[index]
        num = course_num[index]
        sec = course_section[index]

        #       Gets course info
        course_info = uw.term_course_schedule(term_num, name, num)

        if not course_info:
                print "Warning! Course " + name + " " + num + " could not be found!"
                continue


        custom_pick = 0;
        section_found = 0;
        
        for section in course_info:

                #       If there are sections manually selected
                if section["associated_class"] == 99:
                        custom_pick = 1;

                #       If the section is found
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


                        #       Adds related classes if not custom choice and not test
                        if related_class_1:
                                related_section_1 = get_section(course_info,
                                                                related_class_1)
                                
                                section_rel_1_date = get_section_date(related_section_1)
                                section_rel_1_location = get_section_location(related_section_1)
                                section_rel_1_name = get_section_name(related_section_1)

                                if related_section_1["associated_class"] != 99 and \
                                   related_section_1["section"][:-3].strip() != "TST":
                                        add_event(section_rel_1_date, section_rel_1_location,
                                                  section_rel_1_name)


                        if related_class_2:
                                related_section_2 = get_section(course_info,
                                                                related_class_2)

                                section_rel_2_date = get_section_date(related_section_2)
                                section_rel_2_location = get_section_location(related_section_2)
                                section_rel_2_name = get_section_name(related_section_2)
                                
                                if related_section_2["associated_class"] != 99 and \
                                   related_section_2["section"][:-3].strip() != "TST":
                                        add_event(section_rel_2_date, section_rel_2_location,
                                                  section_rel_2_name)

        if section_found == 0:
                print "Warning! Course section for " + name + " "\
                      + num + " " + sec + " could not be found!"
                continue
        

        #       courses with custom options or engineers must specify given section
        if custom_pick == 1 or is_engineer:
                already_chosen1 = ""
                already_chosen2 = ""

                #       Engineers pick from associated courses,
                #       else others pick from custom pick courses
                if not is_engineer:              
                        pick_sections = get_sections_ass(course_info, 99, already_chosen1,
                                                         already_chosen2)
                else:
                        pick_sections = get_sections_ass(course_info, the_section["associated_class"],
                                                         already_chosen1, already_chosen2)
                        pick_sections = remove_section_type(pick_sections,
                                                            the_section["section"][:-3].strip())

                if pick_sections:
                        print "\nNote: Section numbers are different for lectures " \
                              + "and tutorials. (e.g. LEC 001 and TUT 101, 001 != 101)"

                #       User chooses sections not specified
                while pick_sections:
                        if the_section["note"]:
                                print "\nNote for " + the_section["subject"] + " " \
                                      + the_section["catalog_number"] + ": " + the_section["note"]
                        section_type = ((pick_sections[0])["section"])[:-3].strip()

                        section_chosen = -1
                        while section_chosen == -1:
                                
                                pick_input = (raw_input("\nPlease enter your enrolled " \
                                                        + section_type + " section for " \
                                                        + the_section["subject"] + " " + \
                                                        the_section["catalog_number"] \
                                                        + " (e.g. TUT 101 = 101): ")).strip()
                                section_input_cleaned = section_type + " " + pick_input
                                   
                                section_chosen = get_section_full(pick_sections,
                                                                  section_input_cleaned)

                                if section_chosen == -1:
                                        print "\nError! section not found please try again!"
                        

                        section_chosen_date = get_section_date(section_chosen)
                        section_chosen_location = get_section_location(section_chosen)
                        section_chosen_name = get_section_name(section_chosen)
                        
                        add_event(section_chosen_date, section_chosen_location,
                                  section_chosen_name)

                        pick_sections = remove_section_type(pick_sections,
                                                            section_type)


        #       No custom selection of courses
        #       Related sections automatically added
        elif custom_pick == 0:
                ass_id = the_section["associated_class"]

                course_info_main_removed = remove_section_type(course_info,
                                                               the_section["section"][:-3].strip())

                already_chosen1 = ""
                already_chosen2 = ""

                if related_section_1:
                        already_chosen1 = related_section_1["section"][:-3].strip()

                if related_section_2:
                        already_chosen2 = related_section_2["section"][:-3].strip()
                        
                course_info_main_removed = get_sections_ass(course_info_main_removed,
                                                            ass_id, already_chosen1,
                                                            already_chosen2)
                
                
                for section in course_info_main_removed:
                        if section["associated_class"] == ass_id:
                                section_date = get_section_date(section)
                                section_location = get_section_location(section)
                                section_name = get_section_name(section)
                                add_event(section_date, section_location, section_name)
                


                


#       Write to file
with open(term_cleaned + '.ics', 'w') as my_file:
        my_file.writelines(cal)

import os
file_path = os.path.dirname(os.path.abspath(__file__))

print "\n\nCalendar file (.ics) created. Located in " + file_path
raw_input("Press Enter to Continue...")
