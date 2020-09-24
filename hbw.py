from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import unittest
from selenium.webdriver.common.keys import Keys
import time
 
 
class TellBK(unittest.TestCase):
    def setUp(self) -> None:
        #print("88888")
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
 
    def test_fillFeedBack(self):
        #  FeedbackCode.txt保存调查代码，3个一组，空格分开
        #  换行为另一个号
        codefile = open('FeedbackCode.txt', 'r')
        rowsbackcode = codefile.read().splitlines()        
        codefile.close()
        #print(rowsbackcode)
        for i in range(len(rowsbackcode)):
            rowbackcode=rowsbackcode[i]
            print(rowbackcode)
            self.fillFeedBack(rowbackcode)
            num=i%3
            if num == 0:
                self.driver.quit()
                time.sleep(5)
                self.driver = webdriver.Firefox()
                self.driver.implicitly_wait(30)
            else:
                time.sleep(2)
            


    def fillFeedBack(self,rowbackcode):    
        #print("66666")
        driver = self.driver
        driver.set_window_size(100,50)
        #driver.minimize_window()
        driver.get('https://tellburgerking.com.cn')
       
        time.sleep(2)
 
        # Page 1 - Welcome
        # 点击继续
        element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//input[@id="NextButton"]')))
        element.click()
 
        # Page 2 - Fill the codes and continue
        # 填写调查代码, FeedbackCode.txt保存调查代码，3个一组，空格分开
        feedbackcode = rowbackcode.split(" ")
        for i in range(len(feedbackcode)):
            driver.find_element_by_xpath('//input[@id="CN{}"]'.format(i+1)).send_keys(feedbackcode[i])
        # 点击开始
        driver.find_element_by_xpath('//input[@id="NextButton"]').submit()
 
        # Page 3 - Page 12
        radiovaluelist = [('simpleInput rblv', 2), ('simpleInput rblv', 2), ('simpleInput rblv', 1),
                          ('simpleInput rbl', 5), ('simpleInput rbl', 5), ('simpleInput rbl', 5),
                          ('simpleInput rbl', 5), ('simpleInput rbl', 9), ('simpleInput rbl', 2),
                          ('simpleInput rbl', 5)]
        for radiovalue in radiovaluelist:
            self.selectRadiosSubmit(radiovalue)
        time.sleep(1)
        # Page 13 - Say something
        #with open('HappyReason.txt') as filereason:
        #    reasontext = filereason.read()
        driver.find_element_by_xpath('//textarea[@id="S000122"]').send_keys()
        # Next
        driver.find_element_by_xpath('//input[@id="NextButton"]').submit()
        time.sleep(1)
        # Page 14 - What you ordered
        element = self.driver.find_element_by_id("R000091")
        self.driver.execute_script("arguments[0].click();", element)
        driver.find_element_by_xpath('//input[@id="NextButton"]').submit()
        time.sleep(1)
        # Page 15 - What you ordered
        element = self.driver.find_element_by_id("R000097")
        self.driver.execute_script("arguments[0].click();", element)
        driver.find_element_by_xpath('//input[@id="NextButton"]').submit()
        time.sleep(5)
        # Page 16 - Page 18
        radiovaluelist = [('simpleInput rblv', 5),('simpleInput rblv', 2),('simpleInput rblv', 1)]
        for radiovalue in radiovaluelist:
            self.selectRadiosSubmit(radiovalue)
        time.sleep(1)
        # Page 19- Gender and age
        #driver.find_element_by_xpath("//select[@id='R069000']").find_element_by_xpath("//option[@value='2']").click()
        #time.sleep(1)
       # driver.find_element_by_xpath("//select[@id='R070000']").find_element_by_xpath("//option[@value='3']").click()
        driver.find_element_by_xpath('//input[@id="NextButton"]').submit()
        time.sleep(1)
 
        # Page -  Share zip code
        driver.find_element_by_xpath('//input[@id="NextButton"]').click()
        time.sleep(1)
 
        # Page - Last page get screenshot codefile time.strftime("%Y%m%d.%H.%M.%S")
        #driver.get_screenshot_as_file('%s.png' % rowbackcode.replace(' ',''))
        content=driver.find_element_by_xpath("//*[@class='ValCode']").text
        content=content.replace('验证代码：','')
        print(rowbackcode.replace(' ','')+'_'+content)
        output = open('output.txt', 'a')
        output.write(rowbackcode.replace(' ','')+'_'+content+'\n')        
        output.close()

        time.sleep(1)
 
    def selectRadiosSubmit(self, radioattribute):
        elements = self.driver.find_elements_by_xpath(
            '//input[@class="{}" and @value="{}"]'.format(radioattribute[0], radioattribute[1]))
        #print(len(elements))
        for element in elements:
            self.driver.execute_script("arguments[0].click();", element)
            time.sleep(0.3)
        self.driver.find_element_by_xpath('//input[@id="NextButton"]').submit()
        time.sleep(1)
 
    def tearDown(self) -> None:
        print("结束")
        self.driver.quit()
 
 
if __name__ == "__main__":
    print("开始")
    unittest.main()