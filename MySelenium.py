#
#https://sites.google.com/a/chromium.org/chromedriver/downloads
#

#top 100 unfiltered (and top 100 role)
#[rank, name, score, class, spec, role, covenant, faction, region, date, link](11)
#top100CurrentSpec
#[rank, name, score, covenant, faction, region, date](7)

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select 
from selenium.webdriver.common.action_chains import ActionChains
import time
from datetime import date

import SeleniumSQL
from SeleniumSQL import NewOverallRaiderioEntry
from SeleniumSQL import NewRoleRaiderioEntry
from SeleniumSQL import NewSpecRaiderioEntry

PATH = "C:\Program Files (x86)\chromedriver.exe"
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(PATH, options=options)
action = ActionChains(driver)



driver.get("https://raider.io/")
print(driver.title)



#clicking agree to cookies and tos
driver.set_window_size( 1000, 1200)
time.sleep(2)#sleep for time for cookies/tos to appear
cookiesButtonElement = driver.find_element_by_xpath('//*[@id="qc-cmp2-ui"]/div[2]/div/button[2]')
driver.execute_script("arguments[0].click();", cookiesButtonElement)
agreeTermsButton = driver.find_element_by_xpath('/html/body/div[2]/div/div[3]/div/div[2]/button')
agreeTermsButton.click()


#make drop menu for m+ class leaderboards appear
mainSiteDropDown = driver.find_element_by_xpath('//*[@id="application"]/div/div[1]/div[2]/div/div[2]')
driver.execute_script("arguments[0].style.display ='block';", mainSiteDropDown)
time.sleep(1)

#click drop down menu to open a sub menu
mPlusLeaderBoardsDropDown=driver.find_element_by_xpath('//*[@id="application"]/div/div[1]/div[2]/div/div[2]/div/div/h2[1]')
mPlusLeaderBoardsDropDown.click()
time.sleep(1)
#print("opened m+ menu")

#click link from sub menu for desired type of m+ leaderboards

classAndRoleLeaderboards = driver.find_element_by_xpath('//*[@id="application"]/div/div[1]/div[2]/div/div[2]/div/div/div[2]/ul/li[2]/ul/li[3]/span')
classAndRoleLeaderboards.click()
#print("clicked class/role leaderboards menu item")

#dismiss menu that was opened to get to leaderboards
driver.execute_script("arguments[0].style.display ='none';", mainSiteDropDown)
#print("closed main site drop down")
time.sleep(2)

#array to store stuff for commits
top100Array = [[None for i in range(11)] for j in range(100)]
top100RoleArray = [[[None for i in range(11)] for j in range(100)] for k in range(3)]
top100CurrentSpecArray = [[[None for i in range(7)] for j in range(100)] for k in range(36)]
specNameArray = ["death-knight blood", "death-knight frost", "death-knight unholy", "demon-hunter havoc", "demon-hunter vengeance", "druid balance", "druid feral", "druid guardian", "druid restoration",
"hunter beast-mastery", "hunter marksmanship", "hunter marksmanship", "mage arcane", "mage fire", "mage frost", "monk brewmaster", "monk windwalker", "monk mistweaver",
"paladin holy", "paladin protection", "paladin retribution", "priest discipline", "priest holy", "priest shadow", "rogue assassination", "rogue outlaw", "rogue subtlety",
"shaman elemental", "shaman enhancement", "shaman restoration", "warlock affliction", "warlock demonology", "warlock destruction", "warrior arms", "warrior fury", "warrior protection"]

#top 100 unfiltered role/class
for x in range(5):
    #grab table and elements in the table to print/store
    highScoreCurrentTable = driver.find_element_by_xpath('//*[@id="content"]/div/div/div/table/tbody')
    highScoreRows = highScoreCurrentTable.find_elements_by_tag_name("tr")
    for row in highScoreRows:
        #rank, name, score
        rowTDs = row.find_elements_by_tag_name("td")
        currentRank = (int(rowTDs[0].text))
        top100Array[currentRank-1][0] = rowTDs[0].text
        top100Array[currentRank-1][1] = rowTDs[1].find_element_by_tag_name("a").text
        top100Array[currentRank-1][2] =  rowTDs[3].text

        top100Array[currentRank-1][9] = date.today()
        
        #used to grab class or cov if cn or not respectively
        imgStr = rowTDs[1].find_element_by_tag_name("img").get_attribute("src")
        imgStr = imgStr.split('_')

        #turn (region) -> region
        regionStr = rowTDs[1].text.split()
        top100Array[currentRank-1][8] = regionStr[1].replace('(', '').replace(')', '')

        #get faction from class name in span for icon
        factionStr = rowTDs[4].find_element_by_tag_name("span").get_attribute("class")
        factionStr = factionStr.split()[3]
        top100Array[currentRank-1][7] = factionStr.split("-")[2]
        

        #setting cov/class combo based on region (b/c chinese have api limits)
        #pulling from a string so need to filter
        if  top100Array[currentRank-1][8] != "CN":
            top100Array[currentRank-1][10] = rowTDs[1].find_element_by_tag_name("a").get_attribute("href")#link for non cn
            try:
                imgStr = imgStr[2]
                imgStr = imgStr.replace('.jpg', '')
                top100Array[currentRank-1][6] = imgStr
            except:
                top100Array[currentRank-1][6] = "???"
        else:        
            imgStr = imgStr[1]
            imgStr = imgStr.replace('.png', '')
            imgStr = imgStr.capitalize()
            if imgStr == 'Demon-hunter':
                imgStr = 'Demon-Hunter'
            top100Array[currentRank-1][3] = imgStr
            top100Array[currentRank-1][4] = "?cn"
            top100Array[currentRank-1][5] = "?cn"
            top100Array[currentRank-1][6] = "?cn"

    #going to next page
    if 0 < x < 4:
        try:
            nextPageButton = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="content"]/div/div/div/div[2]/a[3]')))
            nextPageButton.click()
        except:
            print("error with next page button click")
    elif x == 0:
        try:
            nextPageButton = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="content"]/div/div/div/div[2]/a[1]')))
            nextPageButton.click()
        except:
            print("error with next page button click")
    time.sleep(2)

#fill in gaps for class/spec/cov for non cn, and fill in some dps for cn
for x in range(100):
    if top100Array[x][8] != 'CN':
        #open new page for character
        driver.get(top100Array[x][10])
        time.sleep(2)
        #grab info on new page for class/spec based on race and/or if d/dkh 
        charH3 = driver.find_element_by_xpath('//*[@id="application"]/div/div[2]/div[1]/div/div/div[1]/div/div/h1/div/div[2]/div[4]/h3')
        splitCharClassStr = charH3.text.split()
        if (splitCharClassStr[0] == "Blood") or (splitCharClassStr[0] == "Night") or (splitCharClassStr[0] == "Void") or (splitCharClassStr[0] == "Lightforged") or (splitCharClassStr[0] == "Kul") or (splitCharClassStr[0] == "Highmountain") or (splitCharClassStr[0] == "Mag'har") or (splitCharClassStr[0] == "Zandalari"):
            if splitCharClassStr[3] == "Demon":
                top100Array[x][3] = "Demon-Hunter"
                top100Array[x][4] = splitCharClassStr[2]
            elif splitCharClassStr[3] == "Death":
                top100Array[x][3] = "Death-Knight"
                top100Array[x][4] = splitCharClassStr[2]
            elif splitCharClassStr[2] == "Beast":
                top100Array[x][4] = "Beast-Mastery"
                top100Array[x][3] = "Hunter"
            else:    
                top100Array[x][3] = splitCharClassStr[3]
                top100Array[x][4] = splitCharClassStr[2]
        elif splitCharClassStr[0] == "Dark":
            if splitCharClassStr[4] == "Death":
                top100Array[x][3] = "Death-Knight"
            elif splitCharClassStr[3] == "Beast":
                    top100Array[x][4] = "Beast-Mastery"
                    top100Array[x][3] = "Hunter"
            else:
                top100Array[x][3] = splitCharClassStr[4]
                top100Array[x][4] = splitCharClassStr[3]
        else:
            if splitCharClassStr[2] == "Death":
                top100Array[x][3] = "Death-Knight"
            elif splitCharClassStr[1] == "Beast":
                    top100Array[x][4] = "Beast-Mastery"
                    top100Array[x][3] = "Hunter"
            else:
                top100Array[x][3] = splitCharClassStr[2]
                top100Array[x][4] = splitCharClassStr[1]
        #setting role based on spec
        if (top100Array[x][4] == "Protection") or (top100Array[x][4] == "Brewmaster") or (top100Array[x][4] == "Guardian") or (top100Array[x][4] == "Vengeance") or (top100Array[x][4] == "Blood"): #tanks
            top100Array[x][5] = 'Tank'
        elif (top100Array[x][4] == "Holy") or (top100Array[x][4] == "Discipline") or (top100Array[x][4] == "Restoration") or (top100Array[x][4] == "Mistweaver"): #healers
            top100Array[x][5] = 'Healer'
        else: #dps
            top100Array[x][5] = 'DPS'
    elif top100Array[x][7] == 'CN':
        #setting role based on class if can
        if top100Array[x][3] == ('Rogue' or 'Hunter' or 'Mage' or 'Warlock'):
            top100Array[x][5] = 'DPS(cn)'
        else:
            top100Array[x][5] = '?cn'


    #print result for checking      
    print(top100Array[x][0]+":\t", top100Array[x][1], top100Array[x][2], top100Array[x][3], top100Array[x][4], top100Array[x][5], top100Array[x][6], top100Array[x][7], top100Array[x][8])













#NAVIGATING TO ROLE LEADERBOARDS
#make drop menu for m+ class leaderboards appear
mainSiteDropDown = driver.find_element_by_xpath('//*[@id="application"]/div/div[1]/div[2]/div/div[2]')
driver.execute_script("arguments[0].style.display ='block';", mainSiteDropDown)
time.sleep(1)

#click drop down menu to open a sub menu
mPlusLeaderBoardsDropDown=driver.find_element_by_xpath('//*[@id="application"]/div/div[1]/div[2]/div/div[2]/div/div/h2[1]')
mPlusLeaderBoardsDropDown.click()
#mPlusLeaderBoardsDropDown.click() #if having issues with this step try 0, 1, or 2 clicks

#click link from sub menu for desired type of m+ leaderboards
specLeaderboards = driver.find_element_by_xpath('//*[@id="application"]/div/div[1]/div[2]/div/div[2]/div/div/div[2]/ul/li[2]/ul/li[3]/span')
specLeaderboards.click()
print("clicked role leaderboards menu item")

#dismiss menu that was opened to get to leaderboards
driver.execute_script("arguments[0].style.display ='none';", mainSiteDropDown)
print("closed main site drop down")
time.sleep(2)


#preparing for role leaderboards navigation
lbMenuSiteDropDown = driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div[1]/div/div/div[1]/div/div/div/ul/li[4]/div')
lbMenuSiteDropDown.click()
time.sleep(1)

currentRoleString = None
lbSubMenuList = driver.find_element_by_xpath('//*[@id="item_1$Menu"]')
lbSubMenuOptions = lbSubMenuList.find_elements_by_tag_name('li')


action.move_to_element(lbSubMenuOptions[0]).perform()
currentRoleString = lbSubMenuOptions[0].text
time.sleep(1)

roleSubMenuList = driver.find_element_by_xpath('//*[@id="character-submenu-items-classes-roles$Menu"]')
roleSubMenuOptions = roleSubMenuList.find_elements_by_tag_name('li')

#iterating through the role leaderboards
for y in range(len(roleSubMenuOptions))[2:]:
    lbMenuSiteDropDown = driver.find_element_by_xpath(
        '/html/body/div[2]/div/div[2]/div[1]/div/div/div[1]/div/div/div/ul/li[4]/div')
    lbMenuSiteDropDown.click()
    time.sleep(1)
    action.move_to_element(lbSubMenuOptions[0]).perform()
    time.sleep(1)
    print(roleSubMenuList.find_elements_by_tag_name('li')[y].text)
    roleSubMenuList.find_elements_by_tag_name('li')[y].click()
    time.sleep(4)

    #top 100 for current role
    for x in range(5):
        
        #grab table and elements in the table to print/store
        highScoreCurrentTable = driver.find_element_by_xpath('//*[@id="content"]/div/div/div/table/tbody')
        highScoreRows = highScoreCurrentTable.find_elements_by_tag_name("tr")
        for row in highScoreRows:
            #rank, name, score
            rowTDs = row.find_elements_by_tag_name("td")
            currentRank = (int(rowTDs[0].text))
            top100RoleArray[y-2][currentRank - 1][0] = rowTDs[0].text
            top100RoleArray[y-2][currentRank - 1][1] = rowTDs[1].find_element_by_tag_name("a").text
            top100RoleArray[y-2][currentRank - 1][2] = rowTDs[3].text

            top100RoleArray[y-2][currentRank-1][9] = date.today()


            #used to grab class or cov if cn or not respectively
            imgStr = rowTDs[1].find_element_by_tag_name("img").get_attribute("src")
            imgStr = imgStr.split('_')

            #turn (region) -> region
            regionStr = rowTDs[1].text.split()
            top100RoleArray[y-2][currentRank - 1][8] = regionStr[1].replace('(', '').replace(')', '')

            #get faction from class name in span for icon
            factionStr = rowTDs[4].find_element_by_tag_name("span").get_attribute("class")
            factionStr = factionStr.split()[3]
            top100RoleArray[y-2][currentRank-1][7] = factionStr.split("-")[2]

            #setting cov/class combo based on region (b/c chinese have api limits)
            #pulling from a string so need to filter
            if top100RoleArray[y-2][currentRank-1][8] != "CN":
                top100RoleArray[y-2][currentRank-1][10] = rowTDs[1].find_element_by_tag_name("a").get_attribute("href")  # link for non cn
                try:
                    imgStr = imgStr[2]
                    imgStr = imgStr.replace('.jpg', '')
                    top100RoleArray[y-2][currentRank-1][6] = imgStr
                except:
                    top100RoleArray[y-2][currentRank-1][6] = "???"
            else:
                imgStr = imgStr[1]
                imgStr = imgStr.replace('.png', '')
                imgStr = imgStr.capitalize()
                if imgStr == 'Demon-hunter':
                    imgStr = 'Demon-Hunter'
                top100RoleArray[y-2][currentRank-1][3] = imgStr
                top100RoleArray[y-2][currentRank-1][4] = "?cn"
                top100RoleArray[y-2][currentRank-1][5] = "?cn"
                top100RoleArray[y-2][currentRank-1][6] = "?cn"

        #going to next page
        if 0 < x < 4:
            try:
                nextPageButton = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="content"]/div/div/div/div[2]/a[3]')))
                nextPageButton.click()
            except:
                print("error with next page button click")
        elif x == 0:
            try:
                nextPageButton = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="content"]/div/div/div/div[2]/a[1]')))
                nextPageButton.click()
            except:
                print("error with next page button click")
        time.sleep(2)

    #reset to first rankings page for new role
    firstRankingsButton = driver.find_element_by_xpath('//*[@id="content"]/div/div/div/div[2]/a[1]/span')
    driver.execute_script("arguments[0].click()", firstRankingsButton)
    time.sleep(1)


#fill in gaps for class/spec/cov for non cn
for y in range(3):
    for x in range(100):
        if top100RoleArray[y][x][8] != 'CN':
            #open new page for character
            driver.get(top100RoleArray[y][x][10])
            time.sleep(2)
            #grab info on new page for class/spec based on race and filter for dh also
            charH3 = driver.find_element_by_xpath('//*[@id="application"]/div/div[2]/div[1]/div/div/div[1]/div/div/h1/div/div[2]/div[4]/h3')
            splitCharClassStr = charH3.text.split()
            if (splitCharClassStr[0] == "Blood") or (splitCharClassStr[0] == "Night") or (splitCharClassStr[0] == "Void") or (splitCharClassStr[0] == "Lightforged") or (splitCharClassStr[0] == "Kul") or (splitCharClassStr[0] == "Highmountain") or (splitCharClassStr[0] == "Mag'har") or (splitCharClassStr[0] == "Zandalari"):
                if splitCharClassStr[3] == "Demon":
                    top100RoleArray[y][x][3] = "Demon-Hunter"
                    top100RoleArray[y][x][4] = splitCharClassStr[2]
                elif splitCharClassStr[3] == "Death":
                    top100RoleArray[y][x][3] = "Death-Knight"
                    top100RoleArray[y][x][4] = splitCharClassStr[2]
                elif splitCharClassStr[2] == "Beast":
                    top100RoleArray[y][x][4] = "Beast-Mastery"
                    top100RoleArray[y][x][3] = "Hunter"
                else:    
                    top100RoleArray[y][x][3] = splitCharClassStr[3]
                    top100RoleArray[y][x][4] = splitCharClassStr[2]
            elif splitCharClassStr[0] == "Dark":
                if splitCharClassStr[4] == "Death":
                    top100RoleArray[y][x][3] = "Death-Knight"
                elif splitCharClassStr[3] == "Beast":
                    top100RoleArray[y][x][4] = "Beast-Mastery"
                    top100RoleArray[y][x][3] = "Hunter"
                else:
                    top100RoleArray[y][x][3] = splitCharClassStr[4]
                    top100RoleArray[y][x][4] = splitCharClassStr[3]
            else:    
                if splitCharClassStr[2] == "Death":
                    top100RoleArray[y][x][3] = "Death-Knight"
                elif splitCharClassStr[1] == "Beast":
                    top100RoleArray[y][x][4] = "Beast-Mastery"
                    top100RoleArray[y][x][3] = "Hunter"
                else:
                    top100RoleArray[y][x][3] = splitCharClassStr[2]
                    top100RoleArray[y][x][4] = splitCharClassStr[1]
            #setting role based on y
            if (y) == 0:
                top100RoleArray[y][x][5] = "Tank"
            elif (y) == 1:
                top100RoleArray[y][x][5] = "Healer"
            else:
                top100RoleArray[y][x][5] = "DPS"

        #print result for checking      
        print(top100RoleArray[y][x][0]+":\t", top100RoleArray[y][x][1], top100RoleArray[y][x][2], top100RoleArray[y][x][3], top100RoleArray[y][x][4], top100RoleArray[y][x][5], top100RoleArray[y][x][6], top100RoleArray[y][x][7], top100RoleArray[y][x][8])
        


  












#NAVIGATING TO SPEC LEADERBOARDS
driver.quit()
time.sleep(4)

#new browser b/c DOM issues #maybe not needed after other fixes added 
PATH = "C:\Program Files (x86)\chromedriver.exe"
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(PATH, options=options)
action = ActionChains(driver)
driver.get("https://raider.io/")
print(driver.title)


#clicking agree to cookies and tos
driver.set_window_size( 1000, 1200)
time.sleep(2)#sleep for time for cookies/tos to appear
cookiesButtonElement = driver.find_element_by_xpath('//*[@id="qc-cmp2-ui"]/div[2]/div/button[2]')
driver.execute_script("arguments[0].click();", cookiesButtonElement)
agreeTermsButton = driver.find_element_by_xpath('/html/body/div[2]/div/div[3]/div/div[2]/button')
agreeTermsButton.click()

#make drop menu for m+ class leaderboards appear
mainSiteDropDown = driver.find_element_by_xpath('//*[@id="application"]/div/div[1]/div[2]/div/div[2]')
driver.execute_script("arguments[0].style.display ='block';", mainSiteDropDown)
time.sleep(1)

#click drop down menu to open a sub menu
mPlusLeaderBoardsDropDown=driver.find_element_by_xpath('//*[@id="application"]/div/div[1]/div[2]/div/div[2]/div/div/h2[1]')
mPlusLeaderBoardsDropDown.click()
#mPlusLeaderBoardsDropDown.click() #if having issues with this step try 0, 1, or 2 clicks

#click link from sub menu for desired type of m+ leaderboards
specLeaderboards = driver.find_element_by_xpath('//*[@id="application"]/div/div[1]/div[2]/div/div[2]/div/div/div[2]/ul/li[2]/ul/li[4]/span')
specLeaderboards.click()
print("clicked spec leaderboards menu item")

#dismiss menu that was opened to get to leaderboards
driver.execute_script("arguments[0].style.display ='none';", mainSiteDropDown)
print("closed main site drop down")
time.sleep(10)


#preparing to navigate through each class
classMenuSiteDropDown = driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div[1]/div/div/div[1]/div/div/div/ul/li[4]/div')
classMenuSiteDropDown.click()
time.sleep(2)

currentClassString = None
classSubMenuList = driver.find_element_by_xpath('//*[@id="item_1$Menu"]')
classSubMenuOptions = classSubMenuList.find_elements_by_tag_name('li')
time.sleep(1)

currentSpecNumber = 0

#iteratively navigating through classes
for classOption in classSubMenuOptions:
    classMenuSiteDropDown = driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div[1]/div/div/div[1]/div/div/div/ul/li[4]/div')
    classMenuSiteDropDown.click()
    time.sleep(1)
    action.move_to_element(classOption).perform()#????
    currentClassString = classOption.find_element_by_tag_name("span").find_elements_by_tag_name("span")[1].text
    time.sleep(1)

    specSubMenuList = classOption.find_element_by_tag_name('ul')
    specSubMenuOptions = specSubMenuList.find_elements_by_tag_name('li')

    
    for y in range(len(specSubMenuOptions)):
        classMenuSiteDropDown = driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div[1]/div/div/div[1]/div/div/div/ul/li[4]/div')
        classMenuSiteDropDown.click()
        time.sleep(1)
        action.move_to_element(classOption).perform()
        time.sleep(1)
        print(specSubMenuList.find_elements_by_tag_name('li')[y].text, currentClassString)
        specSubMenuList.find_elements_by_tag_name('li')[y].click()
        time.sleep(1)
        print("current spec number:",currentSpecNumber)

        #loop through scores for current spec
        for x in range(5):
            #grab table and elements in the table to print/store
            #for specs: rank#, name#, score#, Covenant#, Faction#, Region#, Date
            driver.implicitly_wait(5)
            highScoreCurrentTable = driver.find_element_by_xpath('//*[@id="content"]/div/div/div/table/tbody')
            highScoreRows = highScoreCurrentTable.find_elements_by_tag_name("tr")

            for row in highScoreRows:
                rowTDs = row.find_elements_by_tag_name("td")

                #rank, name, score
                currentRank = (int(rowTDs[0].text))
                top100CurrentSpecArray[currentSpecNumber][currentRank-1][0] = rowTDs[0].text
                try:
                    top100CurrentSpecArray[currentSpecNumber][currentRank-1][1] = rowTDs[1].find_element_by_tag_name("a").text
                except:
                    top100CurrentSpecArray[currentSpecNumber][currentRank-1][1] = rowTDs[1].find_element_by_tag_name("span").text
                top100CurrentSpecArray[currentSpecNumber][currentRank-1][2] =  rowTDs[3].text

                top100CurrentSpecArray[currentSpecNumber][currentRank-1][6] = date.today()

                #region
                regionStr = rowTDs[1].text.split()
                top100CurrentSpecArray[currentSpecNumber][currentRank-1][5] = regionStr[1].replace('(', '').replace(')', '')

                #faction
                factionStr = rowTDs[4].find_element_by_tag_name("span").get_attribute("class")
                factionStr = factionStr.split()[3]
                top100CurrentSpecArray[currentSpecNumber][currentRank-1][4] = factionStr.split("-")[2]

                #used to grab class or cov if cn or not respectively
                imgStr = rowTDs[1].find_element_by_tag_name("img").get_attribute("src")
                imgStr = imgStr.split('_')

                #setting cov/class combo based on region (b/c chinese have api limits)
                #pulling from a string so need to filter
                if  top100CurrentSpecArray[currentSpecNumber][currentRank-1][5] != "CN":
                    try:
                        imgStr = imgStr[2]
                        imgStr = imgStr.replace('.jpg', '')
                        top100CurrentSpecArray[currentSpecNumber][currentRank-1][3] = imgStr
                    except:
                        top100CurrentSpecArray[currentSpecNumber][currentRank-1][3] = "?"
                else:        
                    top100CurrentSpecArray[currentSpecNumber][currentRank-1][3] = "?cn"

                
                print(top100CurrentSpecArray[currentSpecNumber][currentRank-1][0]+":\t", top100CurrentSpecArray[currentSpecNumber][currentRank-1][1], top100CurrentSpecArray[currentSpecNumber][currentRank-1][2], top100CurrentSpecArray[currentSpecNumber][currentRank-1][3], top100CurrentSpecArray[currentSpecNumber][currentRank-1][4], top100CurrentSpecArray[currentSpecNumber][currentRank-1][5])

            time.sleep(3)
            if 0 < x < 4:
                try:
                    nextPageButton = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="content"]/div/div/div/div[2]/a[3]')))
                    nextPageButton.click()
                except:
                    print("error with next page button click")
            elif x == 0:
                try:
                    nextPageButton = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="content"]/div/div/div/div[2]/a[1]')))
                    nextPageButton.click()
                except:
                    print("error with next page button click")        
            time.sleep(5)
            
        currentSpecNumber = currentSpecNumber + 1

        #going back to first page for next new section       
        firstRankingsButton = driver.find_element_by_xpath('//*[@id="content"]/div/div/div/div[2]/a[1]/span')
        driver.execute_script("arguments[0].click()", firstRankingsButton)
        time.sleep(1)

driver.quit()

#committing entries after successful scraping all done
NewOverallRaiderioEntry(top100Array, "top 100 overall")
NewRoleRaiderioEntry(top100RoleArray, "top 100 tanks", 0)
NewRoleRaiderioEntry(top100RoleArray, "top 100 healers", 1)
NewRoleRaiderioEntry(top100RoleArray, "top 100 dps", 2)
print("**finished generic commits**")

for y in range(36):
    NewSpecRaiderioEntry(top100CurrentSpecArray, "top 100 "+specNameArray[y], y)

print("**finished spec commits**")


print("done :)")
quit()


        








