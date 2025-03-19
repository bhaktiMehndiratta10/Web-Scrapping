from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)

driver.get("https://engineering.careers360.com/colleges/ranking/top-private-engineering-colleges-in-India")
print("loading page")


college_data = []
for college in driver.find_elements(By.CLASS_NAME, "college_name"):
    name = college.get_attribute("title")
    url_ = college.find_element(By.TAG_NAME, "a").get_attribute("href")
    print(name, url_)

    if any(d['College Name'] == name for d in college_data):
        print(f"Skipping duplicate entry for {name}")
        continue

    print("LOADING ", name)
    driver2 = webdriver.Chrome(options=options)
    driver2.get(url_)
    sleep(2)


    college_info = {"College Name": name, "URL": url_}
    tables = driver2.find_elements(By.TAG_NAME, "table")
    for table in tables:
        trs = table.find_elements(By.TAG_NAME, "tr")
        for tr in trs:
            tds = tr.find_elements(By.TAG_NAME, "td")
            if len(tds) == 2:
                key = tds[0].text
                value = tds[1].text
                print(key, value)
                college_info[key] = value
            if len(tds) > 2:
                data = []
                for td in tds:
                    if td.text:
                        data.append(td.text)
                if len(data) > 0:
                    print(data)


    coursesTags = []
    courseTags = driver.find_elements(By.CLASS_NAME, "tagsBlk")
    for courseTag in courseTags:
        links = courseTag.find_elements(By.TAG_NAME, "a")
        for link in links:
            coursesTags.append(link.text)
    print("course tags", coursesTags)

    college_info["Course Tags"] = ", ".join(coursesTags)

    courses = []
    courseCards = driver.find_elements(By.CLASS_NAME, "cardBlk")
    for courseCard in courseCards:
        course = courseCard.find_element(By.TAG_NAME, "a").text
        cardTitle = courseCard.find_element(By.CLASS_NAME, "card-title")
        cardTitleLink = cardTitle.find_element(By.TAG_NAME, "a")
        cardTitleLinkText = cardTitleLink.text
        col4 = courseCard.find_elements(By.CLASS_NAME, "col-4")
        for col in col4:

            label = col.find_element(By.CLASS_NAME, "label").text
            text = col.find_element(By.CLASS_NAME, "text").text
            print("lt", label, text)
            courses.append({label: text})
    print("course cards", courses)


    college_info["Courses"] = courses
    college_data.append(college_info)

    driver2.close()
    print("\n\nNEXT\n\n")
    sleep(2)

driver.quit()

df = pd.DataFrame(college_data).drop_duplicates(subset=["College Name"], keep="first")
df.to_excel("info_college.xlsx", index=False)
print("Data saved to info_college.xlsx")
