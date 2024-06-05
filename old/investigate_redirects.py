# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.common.exceptions import NoSuchElementException
import time
# from selenium_stealth import stealth



# options = webdriver.ChromeOptions()
# options.add_argument("start-maximized")
# options.add_argument("--headless")
# options.add_experimental_option("excludeSwitches", ["enable-automation"])
# options.add_experimental_option('useAutomationExtension', False)
# driver = webdriver.Chrome(options=options)

# stealth(driver,
#     'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'
#     languages=["en-US", "en"],
#     vendor="Google Inc.",
#     platform="Win32",
#     webgl_vendor="Intel Inc.",
#     renderer="Intel Iris OpenGL Engine",
#     fix_hairline=True,
# )





# for i, url in list(enumerate(urls))[start_num:]:
#     driver.get(url)
#     driver.implicitly_wait(0.5)
#     try:
#         iframe = driver.find_element(By.ID, 'iframe')
#         id="all-open-roles-1"
#         new_url = iframe.get_attribute('src')
#         if new_url.startswith('http'):
#             driver.get(new_url)
#             driver.implicitly_wait(0.5)
        
#     except NoSuchElementException:
#         new_url = 'no new url'
#     except:
#         new_url = 'error'

#     try:
#         c_name = driver.title#find_element(By.TAG_NAME, 'h1').text
#     except:
#         c_name = 'no company name found'
#     print(i, url, new_url, c_name, sep=' ~ ', flush=True)
#     time.sleep(0.2)

# driver.quit()