
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import time
import message
import sys

class registration:

    classes = []

    def __init__(self, crn, username):

        self.browser = webdriver.Firefox()
        self.crn = crn
        self.villanova_username = username
        self.getClassList()

    def get_to_class_list(self):

        self.browser.get("https://novasis.villanova.edu/pls/bannerprd/bvckschd.p_disp_dyn_sched")
        time.sleep(2)
        pressTerm = self.browser.find_element_by_xpath("//option[@value = '201630']")
        actionChains = ActionChains(self.browser)
        actionChains.double_click(pressTerm).perform()
        time.sleep(2)
        self.browser.find_element_by_xpath("//input[@type='submit']").send_keys(Keys.ENTER)
        time.sleep(3)
        self.browser.find_element_by_xpath("//input[@type='submit']").click()

    def getClassList(self):
        self.get_to_class_list()
        time.sleep(3)
        classes = self.browser.find_elements(By.XPATH, "//th[contains(text(),'CRN:')]")
        textClasses = []
        for i in classes:
            textClasses.append(i.text)
            print(i.text)

        self.getCRNList(textClasses)

    def getCRNList(self, textClasses):
        crnList = []
        for item in textClasses:
            crnLocation = item.find("CRN: ")
            thisCrn = item[crnLocation + 5: crnLocation + 10]
            crnList.append(thisCrn)
            print(thisCrn)
        self.isValidCRN(self.crn, crnList, textClasses)

    def isValidCRN(self, crn, crnList, textClasses):
        if crn in crnList:
            print("it is a valid crn")
            self.getClassfromList(crn, textClasses)
        else:
            print("Not a valid crn")
            crn = input("Please enter a valid one: ")
            self.isValidCRN(crn, crnList, textClasses)

    def findOpenSlot(self, courseNumber, crn):
        self.browser.get("https://novasis.villanova.edu/pls/bannerprd/bvckschd.p_disp_dyn_sched")
        pressTerm = self.browser.find_element_by_xpath("//option[@value = '201630']")
        actionChains = ActionChains(self.browser)
        actionChains.double_click(pressTerm).perform()
        time.sleep(3)
        self.browser.find_element_by_xpath("//input[@type='submit']").send_keys(Keys.ENTER)
        time.sleep(3)
        self.browser.find_element_by_xpath("//input[@id ='crse_id']").send_keys(courseNumber)
        time.sleep(3)
        self.browser.find_element_by_xpath("//input[@type='submit']").click()
        time.sleep(3)
        desiredClasses = self.browser.find_element(By.XPATH, "//th[contains(text(),'" + crn + "')]")
        dc = desiredClasses.text
        if "FULL" in dc:                                                # If full:
            time.sleep(120)                                             # Waits for 2 minutes
            print("No open slot yet")
            self.findOpenSlot(courseNumber, crn)                        # Repeats the search for the class
        else:
            print("there is a open slot")                                                # Calls the function that notifies the user the class has an open slot
            message.sendMail(crn, self.villanova_username)
            self.browser.close()
            sys.exit()
    #
    #         Searches for the class by the course registration number (CRN)
    #         If full repeats the process every 1-2 minutes
    #         If spot open will go to add_class(CRN)
    #         If nonexistant CRN will prompt for correct CRN
    #

    def getClassfromList(self, crn, textClasses):
        courseNumber = ""
        course = next((s for s in textClasses if crn in s), None)

        if " " in course[0:2]:
            courseNumber = course[3:7]
        if course[3] is " ":
            courseNumber = course[4:8]
        if course[4] is " ":
            courseNumber = course[5:9]
        self.findOpenSlot(courseNumber, crn)

