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
               'Prerequisite_3_grade': '', 'Website': '', 'Course_Lang': '', 'Availability': '', 'Description': '',
               'Career_Outcomes': '', 'Online': '', 'Offline': '', 'Distance': '', 'Face_to_Face': '',
               'Blended': '', 'Remarks': ''}

possible_cities = {'rockhampton': 'Rockhampton', 'cairns': 'Cairns', 'bundaberg': 'Bundaberg', 'townsville': 'Townsville',
                   'online': 'Online', 'gladstone': 'Gladstone', 'mackay': 'Mackay', 'mixed': 'Online', 'yeppoon': 'Yeppoon',
                   'brisbane': 'Brisbane', 'sydney': 'Sydney', 'queensland': 'Queensland', 'melbourne': 'Melbourne',
                   'albany': 'Albany', 'perth': 'Perth', 'adelaide': 'Adelaide', 'noosa': 'Noosa', 'emerald': 'Emerald',
                   'hawthorn': 'Hawthorn', 'wantirna': 'Wantirna', 'prahran': 'Prahran'}

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

