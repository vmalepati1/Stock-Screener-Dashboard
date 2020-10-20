from selenium import webdriver
from selenium.webdriver.common.by import By

# creates new instance of chrome in incognito mode, need to change this to where your chrome driver is
# if you want to make this more efficient somehow then you can just do that
browser = webdriver.Chrome(executable_path='C:\\Users\\malep\\Downloads\\chromedriver_win32\\chromedriver.exe')

print('Started')
# taking the info off of yahoo in order to attain the information
browser.get("https://finance.yahoo.com/quote/FB?p=FB")

# wait up to 10 seconds for page to load or gg


# takes all the financial titles (like the part that is EPS:), seperate from the values
titles_element = browser.find_elements_by_xpath("//td[@class='C(black) W(51%)']")
titles = [x.text for x in titles_element]


print('titles:', titles)


# get all of the financial values themselves, seperate from the titles
values_element = browser.find_elements_by_xpath("//td[@class='Ta(end) Fw(600) Lh(14px)']")
values = [x.text for x in values_element] # basically the same thing as finding the titles, just the values
print('values:', values, '\n')
print()


# pair each title with its corresponding value using zip function and print each pair
# pairs the title with its corresponding value using the zip function (idk how this works I just looks this up)
for title, value in zip(titles, values):
    print(titles + ': ' + values)
