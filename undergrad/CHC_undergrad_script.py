"""Description:
    * author: Magdy Abdelkader
    * company: Fresh Futures/Seeka Technology
    * position: IT Intern
    * date: 16-11-20
    * description:This script extracts the corresponding undergraduate courses details and tabulate it.
"""

import csv
import re
import time
from pathlib import Path
from selenium import webdriver
import bs4 as bs4
import os
import copy
from CustomMethods import TemplateData
from CustomMethods import DurationConverter as dura

option = webdriver.ChromeOptions()
option.add_argument(" - incognito")
option.add_argument("headless")
exec_path = Path(os.getcwd().replace('\\', '/'))
exec_path = exec_path.parent.__str__() + '/Libraries/Google/v86/chromedriver.exe'
browser = webdriver.Chrome(executable_path=exec_path, options=option)

# read the url from each file into a list
course_links_file_path = Path(os.getcwd().replace('\\', '/'))
course_links_file_path = course_links_file_path.__str__() + '/CHC_undergrad_links.txt'
course_links_file = open(course_links_file_path, 'r')

# the csv file we'll be saving the courses to
csv_file_path = Path(os.getcwd().replace('\\', '/'))
csv_file = csv_file_path.__str__() + '/CHC_undergrad.csv'

course_data = {'Level_Code': '', 'University': 'Christian Heritage College', 'City': '', 'Country': 'Australia',
               'Course': '', 'Int_Fees': '', 'Local_Fees': '', 'Currency': 'AUD', 'Currency_Time': 'year',
               'Duration': '', 'Duration_Time': '', 'Full_Time': '', 'Part_Time': '', 'Prerequisite_1': '',
               'Prerequisite_2': 'IELTS', 'Prerequisite_3': '', 'Prerequisite_1_grade': '', 'Prerequisite_2_grade': '7.5',
               'Prerequisite_3_grade': '', 'Website': '', 'Course_Lang': '', 'Availability': 'A', 'Description': '',
               'Career_Outcomes': '', 'Online': '', 'Offline': '', 'Distance': '', 'Face_to_Face': '',
               'Blended': '', 'Remarks': '', 'Subject_Description_1': '', 'Subject_or_Unit_2': '',
               'Subject_Objective_2': '', 'Subject_Description_2': '',
               'Subject_or_Unit_3': '', 'Subject_Objective_3': '', 'Subject_Description_3': '',
               'Subject_or_Unit_4': '', 'Subject_Objective_4': '', 'Subject_Description_4': '',
               'Subject_or_Unit_5': '', 'Subject_Objective_5': '', 'Subject_Description_5': '',
               'Subject_or_Unit_6': '', 'Subject_Objective_6': '', 'Subject_Description_6': '',
               'Subject_or_Unit_7': '', 'Subject_Objective_7': '', 'Subject_Description_7': '',
               'Subject_or_Unit_8': '', 'Subject_Objective_8': '', 'Subject_Description_8': '',
               'Subject_or_Unit_9': '', 'Subject_Objective_9': '', 'Subject_Description_9': '',
               'Subject_or_Unit_10': '', 'Subject_Objective_10': '', 'Subject_Description_10': '',
               'Subject_or_Unit_11': '', 'Subject_Objective_11': '', 'Subject_Description_11': '',
               'Subject_or_Unit_12': '', 'Subject_Objective_12': '', 'Subject_Description_12': '',
               'Subject_or_Unit_13': '', 'Subject_Objective_13': '', 'Subject_Description_13': '',
               'Subject_or_Unit_14': '', 'Subject_Objective_14': '', 'Subject_Description_14': '',
               'Subject_or_Unit_15': '', 'Subject_Objective_15': '', 'Subject_Description_15': '',
               'Subject_or_Unit_16': '', 'Subject_Objective_16': '', 'Subject_Description_16': '',
               'Subject_or_Unit_17': '', 'Subject_Objective_17': '', 'Subject_Description_17': '',
               'Subject_or_Unit_18': '', 'Subject_Objective_18': '', 'Subject_Description_18': '',
               'Subject_or_Unit_19': '', 'Subject_Objective_19': '', 'Subject_Description_19': '',
               'Subject_or_Unit_20': '', 'Subject_Objective_20': '', 'Subject_Description_20': '',
               'Subject_or_Unit_21': '', 'Subject_Objective_21': '', 'Subject_Description_21': '',
               'Subject_or_Unit_22': '', 'Subject_Objective_22': '', 'Subject_Description_22': '',
               'Subject_or_Unit_23': '', 'Subject_Objective_23': '', 'Subject_Description_23': '',
               'Subject_or_Unit_24': '', 'Subject_Objective_24': '', 'Subject_Description_24': '',
               'Subject_or_Unit_25': '', 'Subject_Objective_25': '', 'Subject_Description_25': '',
               'Subject_or_Unit_26': '', 'Subject_Objective_26': '', 'Subject_Description_26': '',
               'Subject_or_Unit_27': '', 'Subject_Objective_27': '', 'Subject_Description_27': '',
               'Subject_or_Unit_28': '', 'Subject_Objective_28': '', 'Subject_Description_28': '',
               'Subject_or_Unit_29': '', 'Subject_Objective_29': '', 'Subject_Description_29': '',
               'Subject_or_Unit_30': '', 'Subject_Objective_30': '', 'Subject_Description_30': '',
               'Subject_or_Unit_31': '', 'Subject_Objective_31': '', 'Subject_Description_31': '',
               'Subject_or_Unit_32': '', 'Subject_Objective_32': '', 'Subject_Description_32': '',
               'Subject_or_Unit_33': '', 'Subject_Objective_33': '', 'Subject_Description_33': '',
               'Subject_or_Unit_34': '', 'Subject_Objective_34': '', 'Subject_Description_34': '',
               'Subject_or_Unit_35': '', 'Subject_Objective_35': '', 'Subject_Description_35': '',
               'Subject_or_Unit_36': '', 'Subject_Objective_36': '', 'Subject_Description_36': '',
               'Subject_or_Unit_37': '', 'Subject_Objective_37': '', 'Subject_Description_37': '',
               'Subject_or_Unit_38': '', 'Subject_Objective_38': '', 'Subject_Description_38': '',
               'Subject_or_Unit_39': '', 'Subject_Objective_39': '', 'Subject_Description_39': '',
               'Subject_or_Unit_40': '', 'Subject_Objective_40': '', 'Subject_Description_40': ''}

possible_cities = {'rockhampton': 'Rockhampton', 'cairns': 'Cairns', 'bundaberg': 'Bundaberg', 'townsville': 'Townsville',
                   'online': 'Online', 'gladstone': 'Gladstone', 'mackay': 'Mackay', 'mixed': 'Online', 'yeppoon': 'Yeppoon',
                   'brisbane': 'Brisbane', 'sydney': 'Sydney', 'queensland': 'Queensland', 'melbourne': 'Melbourne',
                   'albany': 'Albany', 'perth': 'Perth', 'adelaide': 'Adelaide', 'noosa': 'Noosa', 'emerald': 'Emerald',
                   'hawthorn': 'Hawthorn', 'wantirna': 'Wantirna', 'prahran': 'Prahran', 'carindale': 'Carindale'}

possible_languages = {'Japanese': 'Japanese', 'French': 'French', 'Italian': 'Italian', 'Korean': 'Korean',
                      'Indonesian': 'Indonesian', 'Chinese': 'Chinese', 'Spanish': 'Spanish'}

course_data_all = []
level_key = TemplateData.level_key  # dictionary of course levels
faculty_key = TemplateData.faculty_key  # dictionary of course levels

# GET EACH COURSE LINK
for each_url in course_links_file:
    actual_cities = []
    remarks_list = []
    browser.get(each_url)
    pure_url = each_url.strip()
    each_url = browser.page_source

    soup = bs4.BeautifulSoup(each_url, 'lxml')
    time.sleep(1)

    # SAVE COURSE URL
    course_data['Website'] = pure_url

    # SAVE COURSE TITLE
    title_tag = soup.find('h1', class_='highlight-text fusion-responsive-typography-calculated')
    if title_tag:
        course_data['Course'] = title_tag.get_text().strip()
        print('COURSE TITLE: ', title_tag.get_text().strip())

    # DECIDE THE LEVEL CODE
    for i in level_key:
        for j in level_key[i]:
            if j in course_data['Course']:
                course_data['Level_Code'] = i
    print('COURSE LEVEL CODE: ', course_data['Level_Code'])

    # DECIDE THE FACULTY
    for i in faculty_key:
        for j in faculty_key[i]:
            if j.lower() in course_data['Course'].lower():
                course_data['Faculty'] = i
    print('COURSE FACULTY: ', course_data['Faculty'])

    # COURSE LANGUAGE
    for language in possible_languages:
        if language in course_data['Course']:
            course_data['Course_Lang'] = language
        else:
            course_data['Course_Lang'] = 'English'
    print('COURSE LANGUAGE: ', course_data['Course_Lang'])

    # COURSE DESCRIPTION
    description_tag = soup.find('h3', class_='proxima-heading fusion-responsive-typography-calculated')
    if description_tag:
        description_list = []
        description_p_list = description_tag.find_next_siblings('p')
        if description_p_list:
            for p in description_p_list:
                description_list.append(p.get_text().strip())
            description_list = ' '.join(description_list)
            course_data['Description'] = description_list
            print('COURSE DESCRIPTION: ', description_list)

    # DURATION
    duration_list = soup.find('ul', class_='duration-list')
    if duration_list:
        duration_li = duration_list.find_all('li')
        if duration_li:
            for index, li in enumerate(duration_li):
                if index == 0:
                    duration = li.find('span')
                    if duration:
                        duration_text = duration.get_text().lower()
                        if 'full-time' in duration_text:
                            course_data['Full_Time'] = 'yes'
                        else:
                            course_data['Full_Time'] = 'no'
                        if 'part-time' in duration_text:
                            course_data['Part_Time'] = 'yes'
                        else:
                            course_data['Part_Time'] = 'no'
                        print('FULL-TIME/PART-TIME: ', course_data['Full_Time'] + ' / ' + course_data['Part_Time'])
                        converted_dura = dura.convert_duration(duration_text)
                        if converted_dura is not None:
                            conv_duration_list = list(converted_dura)
                            if conv_duration_list[0] == 1 and 'Years' in conv_duration_list[1]:
                                conv_duration_list[1] = 'Year'
                            elif conv_duration_list[0] == 1 and 'Months' in conv_duration_list[1]:
                                conv_duration_list[1] = 'Month'
                            course_data['Duration'] = conv_duration_list[0]
                            course_data['Duration_Time'] = conv_duration_list[1]
                            print('DURATION/DURATION-TIME',
                                  str(course_data['Duration']) + ' / ' + course_data['Duration_Time'])

    #ATAR
    atar_tag = soup.find('h4', class_='fusion-responsive-typography-calculated',
                         text=re.compile(r'MINIMUM SELECTION THRESHOLD \(OP/RANK\)', re.IGNORECASE))
    if atar_tag:
        atar_p = atar_tag.find_next_sibling('p')
        if atar_p:
            atar = re.findall(r'\d+', atar_p.get_text())
            if atar is not None:
                if len(atar) == 2:
                    course_data['Prerequisite_1_grade'] = atar[1]
                    course_data['Prerequisite_1'] = 'year 12'
                else:
                    course_data['Prerequisite_1_grade'] = 'N/A'
                    course_data['Prerequisite_1'] = 'year 12'
                print('ATAR: ', course_data['Prerequisite_1_grade'])

    # CAREER OUTCOMES
    career_outcome_title = soup.find('span', class_='fusion-toggle-heading', text=re.compile('Career Outcomes', re.IGNORECASE))
    course_data['Career_Outcomes'] = ''
    if career_outcome_title:
        title_parent = career_outcome_title.find_parent('div', class_='panel-heading')
        if title_parent:
            career_container = title_parent.find_next_sibling('div')
            if career_container:
                career_p = career_container.find('p')
                if career_p:
                    course_data['Career_Outcomes'] = career_p.get_text()
                    print('CAREER OUTCOMES: ', course_data['Career_Outcomes'])

    # DELIVERY MODE
    mode_tag = soup.find('h4', class_='fusion-responsive-typography-calculated',
                         text=re.compile('MODE', re.IGNORECASE))
    if mode_tag:
        mode_p = mode_tag.find_next_sibling('p')
        if mode_p:
            mode_text = mode_p.get_text().lower()
            if 'on campus' in mode_text:
                actual_cities.append('carindale')
                course_data['Face_to_Face'] = 'yes'
                course_data['Offline'] = 'yes'
            else:
                course_data['Face_to_Face'] = 'no'
                course_data['Offline'] = 'no'
            if 'online' in mode_text:
                course_data['Online'] = 'yes'
                actual_cities.append('online')
            else:
                course_data['Online'] = 'no'
            if 'external' in mode_text:
                course_data['Distance'] = 'yes'
            else:
                course_data['Distance'] = 'no'
            if 'mixed' in mode_text:
                course_data['Blended'] = 'yes'
            else:
                course_data['Blended'] = 'no'
        print('DELIVERY: online: ' + course_data['Online'] + ' offline: ' + course_data['Offline'] + ' face to face: ' +
              course_data['Face_to_Face'] + ' blended: ' + course_data['Blended'] + ' distance: ' +
              course_data['Distance'])

        # UNIT
        unit_table = soup.find_all('table', class_='unit-table-data')
        i = 1
        if unit_table:
            a_list = []
            for table in unit_table:
                a_tags = table.find_all('a')
                for a in a_tags:
                    a_list.append(a.get_text().replace('Download', ''))
            for name in a_list:
                if i < 40:
                    course_data['Subject_or_Unit_' + str(i)] = name
                i += 1

    # duplicating entries with multiple cities for each city
    for i in actual_cities:
        course_data['City'] = possible_cities[i]
        course_data_all.append(copy.deepcopy(course_data))
    del actual_cities

    # TABULATE THE DATA
    desired_order_list = ['Level_Code', 'University', 'City', 'Course', 'Faculty', 'Int_Fees', 'Local_Fees',
                          'Currency', 'Currency_Time', 'Duration', 'Duration_Time', 'Full_Time', 'Part_Time',
                          'Prerequisite_1', 'Prerequisite_2', 'Prerequisite_3', 'Prerequisite_1_grade',
                          'Prerequisite_2_grade', 'Prerequisite_3_grade', 'Website', 'Course_Lang', 'Availability',
                          'Description', 'Career_Outcomes', 'Country', 'Online', 'Offline', 'Distance', 'Face_to_Face',
                          'Blended', 'Remarks', 'Subject_or_Unit_1', 'Subject_Objective_1',
                          'Subject_Description_1', 'Subject_or_Unit_2', 'Subject_Objective_2', 'Subject_Description_2',
                          'Subject_or_Unit_3', 'Subject_Objective_3', 'Subject_Description_3',
                          'Subject_or_Unit_4', 'Subject_Objective_4', 'Subject_Description_4',
                          'Subject_or_Unit_5', 'Subject_Objective_5', 'Subject_Description_5',
                          'Subject_or_Unit_6', 'Subject_Objective_6', 'Subject_Description_6',
                          'Subject_or_Unit_7', 'Subject_Objective_7', 'Subject_Description_7',
                          'Subject_or_Unit_8', 'Subject_Objective_8', 'Subject_Description_8',
                          'Subject_or_Unit_9', 'Subject_Objective_9', 'Subject_Description_9',
                          'Subject_or_Unit_10', 'Subject_Objective_10', 'Subject_Description_10',
                          'Subject_or_Unit_11', 'Subject_Objective_11', 'Subject_Description_11',
                          'Subject_or_Unit_12', 'Subject_Objective_12', 'Subject_Description_12',
                          'Subject_or_Unit_13', 'Subject_Objective_13', 'Subject_Description_13',
                          'Subject_or_Unit_14', 'Subject_Objective_14', 'Subject_Description_14',
                          'Subject_or_Unit_15', 'Subject_Objective_15', 'Subject_Description_15',
                          'Subject_or_Unit_16', 'Subject_Objective_16', 'Subject_Description_16',
                          'Subject_or_Unit_17', 'Subject_Objective_17', 'Subject_Description_17',
                          'Subject_or_Unit_18', 'Subject_Objective_18', 'Subject_Description_18',
                          'Subject_or_Unit_19', 'Subject_Objective_19', 'Subject_Description_19',
                          'Subject_or_Unit_20', 'Subject_Objective_20', 'Subject_Description_20',
                          'Subject_or_Unit_21', 'Subject_Objective_21', 'Subject_Description_21',
                          'Subject_or_Unit_22', 'Subject_Objective_22', 'Subject_Description_22',
                          'Subject_or_Unit_23', 'Subject_Objective_23', 'Subject_Description_23',
                          'Subject_or_Unit_24', 'Subject_Objective_24', 'Subject_Description_24',
                          'Subject_or_Unit_25', 'Subject_Objective_25', 'Subject_Description_25',
                          'Subject_or_Unit_26', 'Subject_Objective_26', 'Subject_Description_26',
                          'Subject_or_Unit_27', 'Subject_Objective_27', 'Subject_Description_27',
                          'Subject_or_Unit_28', 'Subject_Objective_28', 'Subject_Description_28',
                          'Subject_or_Unit_29', 'Subject_Objective_29', 'Subject_Description_29',
                          'Subject_or_Unit_30', 'Subject_Objective_30', 'Subject_Description_30',
                          'Subject_or_Unit_31', 'Subject_Objective_31', 'Subject_Description_31',
                          'Subject_or_Unit_32', 'Subject_Objective_32', 'Subject_Description_32',
                          'Subject_or_Unit_33', 'Subject_Objective_33', 'Subject_Description_33',
                          'Subject_or_Unit_34', 'Subject_Objective_34', 'Subject_Description_34',
                          'Subject_or_Unit_35', 'Subject_Objective_35', 'Subject_Description_35',
                          'Subject_or_Unit_36', 'Subject_Objective_36', 'Subject_Description_36',
                          'Subject_or_Unit_37', 'Subject_Objective_37', 'Subject_Description_37',
                          'Subject_or_Unit_38', 'Subject_Objective_38', 'Subject_Description_38',
                          'Subject_or_Unit_39', 'Subject_Objective_39', 'Subject_Description_39',
                          'Subject_or_Unit_40', 'Subject_Objective_40', 'Subject_Description_40']

    course_dict_keys = set().union(*(d.keys() for d in course_data_all))

    with open(csv_file, 'w', encoding='utf-8', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, course_dict_keys)
        dict_writer.writeheader()
        dict_writer.writerows(course_data_all)

    with open(csv_file, 'r', encoding='utf-8') as infile, open('CHC_undergrad_ordered.csv', 'w', encoding='utf-8',
                                                               newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=desired_order_list)
        # reorder the header first
        writer.writeheader()
        for row in csv.DictReader(infile):
            # writes the reordered rows to the new file
            writer.writerow(row)
