
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import selenium.webdriver.chrome.options
from datetime import datetime
import random
import time
import csv
import os

# driver boot procedure
def boot():
    # manage notifications
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications" : 2}
    chrome_options.add_experimental_option("prefs",prefs)

    # driver itself
    dv = webdriver.Chrome(chrome_options = chrome_options, executable_path = r"./chromedriver81.exe")
    #dv.maximize_window()
    return dv

# kill the driver
def killb(dv):
    dv.quit()
    
# login protocol
def loginProc(dv, username, password):
    dv.get("https://mail.yahoo.com/d/folders/1?.src=fp")

    WebDriverWait(dv, 20).until(EC.visibility_of_all_elements_located)
    time.sleep(2)
    
    # username
    loginUsername = dv.find_element_by_name("username")

    for i in range(len(username)):
        #time.sleep(0.1)
        loginUsername.send_keys(username[i])
        
    loginUsername.send_keys(Keys.ENTER)
    WebDriverWait(dv, 20).until(EC.visibility_of_all_elements_located)
    time.sleep(2)
    
    # password
    loginPassword = dv.find_element_by_name("password")
    
    for i in range(len(password)):
        #time.sleep(0.1)
        loginPassword.send_keys(password[i])

    loginPassword.send_keys(Keys.ENTER)

# scraping function
def scraper(dv, maindir, email_credentials):
    WebDriverWait(dv, 20).until(EC.visibility_of_all_elements_located)
    time.sleep(5)
    
    i = 0
    emails_list = []
    while True:
        i += 1
        try:
            path = "/html/body/div[1]/div/div[1]/div/div[2]/div/div[1]/nav/div/div[3]/div[1]/ul/li[" + str(i) + "]/a/span[1]"
            email = dv.find_element_by_xpath(path)
            emails_list.append(email)
            
            for email in emails_list:
                filename = str(email.text) + ".csv"
                WebDriverWait(dv, 20).until(EC.visibility_of_all_elements_located)
                
                email.click()
                
                WebDriverWait(dv, 20).until(EC.visibility_of_all_elements_located)
                time.sleep(5)
                '''
                goBack = dv.find_element_by_xpath("/html/body")
                for i in range(10): 
                    goBack.send_keys(Keys.PAGE_DOWN)
                    time.sleep(1)
                '''
                with open(filename, 'w', newline='') as mailFile:
                    csvWriter = csv.writer(mailFile)
                
                    mails = []
                    i = 2
                    e = 0
                    while True:
                        goBack = dv.find_element_by_xpath("/html/body")
                        goBack.send_keys(Keys.PAGE_DOWN)
                        try:
                            i += 1  
                            path = "#mail-app-component > div.W_6D6F.D_F > div > div.D_F.ab_FT.em_N.ek_BB.iz_A.H_6D6F > div > div > div.W_6D6F.H_6D6F.cZ1RN91d_n.o_h.p_R.em_N.D_F > div > div.p_R.Z_0.iy_h.iz_A.W_6D6F.H_6D6F.k_w.em_N.c22hqzz_GN > ul > li:nth-child("+str(i)+") > a > div > div.D_F.o_h.ab_C.H_6D6F.a_3vhr3.em_qk.ej_0 > div.D_F.o_h.G_e.em_N > span"
                            message = dv.find_element_by_css_selector(path)
                            try:
                                read_path = "#mail-app-component > div.W_6D6F.D_F > div > div.D_F.ab_FT.em_N.ek_BB.iz_A.H_6D6F > div > div > div.W_6D6F.H_6D6F.cZ1RN91d_n.o_h.p_R.em_N.D_F > div > div.p_R.Z_0.iy_h.iz_A.W_6D6F.H_6D6F.k_w.em_N.c22hqzz_GN > ul > li:nth-child("+str(i)+") > a > div > div.D_F.o_h.ab_C.H_6D6F.a_3vhr3.em_qk.ej_0 > span > button > svg"
                                read_indicator = dv.find_element_by_css_selector(read_path)
                                mail = message.get_attribute("title")
                                mails.append(mail)
                                csvWriter.writerow([str(mail)])
                                
                                message.click()
                                time.sleep(5)
                                goBack = dv.find_element_by_xpath("/html/body")
                                goBack.send_keys(Keys.ESCAPE)
                                time.sleep(3)
                            except Exception:
                                pass
                        
                        except Exception as EXC:
                            #print(EXC)
                            e = e + 1
                            dv.execute_script("window.scrollTo(0, 10)")
                            time.sleep(3)
                            '''
                            goBack = dv.find_element_by_xpath("/html/body")
                            goBack.send_keys(Keys.PAGE_DOWN)
                            '''
                            if e == 20:
                                e = 0
                                break
                        
                mailFile.close()
        except:
            filename = str(email_credentials) + ".csv"
            WebDriverWait(dv, 20).until(EC.visibility_of_all_elements_located)
            time.sleep(5)
            with open(filename, 'w', newline='') as mailFile:
                csvWriter = csv.writer(mailFile)
            
                mails = []
                i = 1
                e = 0
                while True:
                    goBack = dv.find_element_by_xpath("/html/body")
                    goBack.send_keys(Keys.PAGE_DOWN)
                    try:
                        i += 1
                        path = "#mail-app-component > div.W_6D6F.D_F > div > div.D_F.ab_FT.em_N.ek_BB.iz_A.H_6D6F > div > div > div.W_6D6F.H_6D6F.cZ1RN91d_n.o_h.p_R.em_N.D_F > div > div.p_R.Z_0.iy_h.iz_A.W_6D6F.H_6D6F.k_w.em_N.c22hqzz_GN > ul > li:nth-child("+str(i)+") > a > div > div.D_F.o_h.ab_C.H_6D6F.a_3vhr3.em_qk.ej_0 > div.D_F.o_h.G_e.em_N > span"
                        message = dv.find_element_by_css_selector(path)
                        try:
                            read_path = "#mail-app-component > div.W_6D6F.D_F > div > div.D_F.ab_FT.em_N.ek_BB.iz_A.H_6D6F > div > div > div.W_6D6F.H_6D6F.cZ1RN91d_n.o_h.p_R.em_N.D_F > div > div.p_R.Z_0.iy_h.iz_A.W_6D6F.H_6D6F.k_w.em_N.c22hqzz_GN > ul > li:nth-child("+str(i)+") > a > div > div.D_F.o_h.ab_C.H_6D6F.a_3vhr3.em_qk.ej_0 > span > button > svg"
                            read_indicator = dv.find_element_by_css_selector(read_path)
                            mail = message.get_attribute("title")
                            mails.append(mail)
                            csvWriter.writerow([str(mail)])
                            
                            message.click()
                            time.sleep(5)
                            goBack = dv.find_element_by_xpath("/html/body")
                            goBack.send_keys(Keys.ESCAPE)
                            time.sleep(3)
                        except Exception as EXC:
                            #print(EXC)
                            pass
                    
                    except Exception as EXC:
                        #print(EXC)
                        e = e + 1
                        dv.execute_script("window.scrollTo(0, 10)")
                        time.sleep(3)
                        '''
                        goBack = dv.find_element_by_xpath("/html/body")
                        goBack.send_keys(Keys.PAGE_DOWN)
                        '''
                        if e == 20:
                            e = 0
                            break
                
            mailFile.close()
            break    
    
    os.chdir(maindir)



if __name__ == '__main__':
    with open("credentials.txt", "r", newline = '') as credsFile:
        credentials = credsFile.read().splitlines()
        email = credentials[0]
        password = credentials[1]
    #print(credentials)
    maindir = os.getcwd()
    
    file_index = 0
    restart = True
    while restart:
        for i in range(int(len(credentials) / 2)):
            file_index += 1
            dv = boot()
            email = credentials[i*2]
            password = credentials[i*2 + 1]

            loginProc(dv, email, password)
            
            fname = str(datetime.now())
            fname = fname.split(" ")
            while True:
                try:
                    os.mkdir(fname[0])
                    os.chdir("./"+fname[0])
                    break
                except Exception as EXC:
                    #print(EXC)
                    try:
                        os.mkdir(fname[0]+" #"+str(file_index))
                        os.chdir("./"+fname[0]+" #"+str(file_index))
                        break
                    except Exception as EXC:
                        #print(EXC)
                        None
            
            scraper(dv, maindir, email)
            killb(dv)