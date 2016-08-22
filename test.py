#!/usr/bin/env python
#coding: utf-8

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from pyvirtualdisplay import Display
from email.mime.text import MIMEText
import unittest
import smtplib
import time

display = Display(visible=0, size=(1024, 768))
display.start()

class PythonOrgSearch(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_search_in_python_org(self):
        base = "http://ipc.fmprc.gov.cn/chn/hdtz/"
        driver = self.driver
        driver.get(base)
       # self.assertIn("Python", driver.title)
        #elem = driver.find_element_by_id("docMore")
        eleList = driver.find_elements_by_class_name("glfont12")
        old = self.get_file_content()
        new = []
        for i in eleList[:5]:
            a = i.find_element_by_tag_name('a')
            b = a.get_attribute('href')
            new.append(b.encode('ascii', 'ignore'))
        self.write_to_file(new)
        
        checkList = []
        for i in new:
            if i+'\n' not in old:
                checkList.append(i)
            else:
                break

        if len(checkList) != 0:
            s = smtplib.SMTP('localhost')
            for i in checkList:
                title, content = self.getContent(i)
                self.send_mail(title, content, s)
            s.quit()


    def getContent(self, checkURL):
        driver = self.driver
        driver.get(checkURL)
        content = driver.find_element_by_class_name('content')
        
        return driver.title, content.text
        
        
    # Sent new content to mail
    def send_mail(self, title, content, s):
        msg = MIMEText(content, _charset="UTF-8")
        me = 'sasori.haku@xinbai.com'
        you = '95447986@qq.com'
        msg['Subject'] = title 
        msg['From'] = me
        msg['To'] = you

        s.sendmail(me, [you], msg.as_string())

    # Write new record to file
    def write_to_file(self, l):
        f = open('/root/seleniumTest/record', 'w')
        for i in l:
            f.write(i.encode('ascii', 'ignore')+'\n')
        f.close()

    # Get saved record
    def get_file_content(self):
        f = open('/root/seleniumTest/record', 'r')
        a = f.readlines()
        f.close()
        return a

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()
    display.stop()
