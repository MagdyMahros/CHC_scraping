"""Description:
    * author: Magdy Abdelkader
    * company: Fresh Futures/Seeka Technology
    * position: IT Intern
    * date: 16-11-20
    * description:This script extracts all the courses links and save it in txt file.
"""
from pathlib import Path
from selenium import webdriver
import os


option = webdriver.ChromeOptions()
option.add_argument(" - incognito")
option.add_argument("headless")
exec_path = Path(os.getcwd().replace('\\', '/'))
exec_path = exec_path.parent.__str__() + '/Libraries/Google/v86/chromedriver.exe'
browser = webdriver.Chrome(executable_path=exec_path, options=option)

# MAIN ROUTINE
courses_page_url = 'https://chc.edu.au/courses/?department=&course_category=Postgraduate&keyphrase='
list_of_links = []
browser.get(courses_page_url)

# EXTRACT ALL THE LINKS TO LIST
result_elements = browser.find_elements_by_class_name('course-box')
for element in result_elements:
    a_tag = element.find_element_by_tag_name('a')
    link = a_tag.get_property('href')
    list_of_links.append(link)


# SAVE TO FILE
course_links_file_path = os.getcwd().replace('\\', '/') + '/CHC_postgrad_links.txt'
course_links_file = open(course_links_file_path, 'w')
for link in list_of_links:
    if link is not None and link != "" and link != "\n":
        if link == list_of_links[-1]:
            course_links_file.write(link.strip())
        else:
            course_links_file.write(link.strip() + '\n')
course_links_file.close()
