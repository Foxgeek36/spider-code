from selenium import webdriver
# import pickle
# from redis import Redis
# redis_cli = Redis()

browser = webdriver.Chrome(executable_path='chromedriver')

with open('x-uab-deocde.js', 'r') as f:
    js = f.read()

# redis_cli.set('chrome_browser_serialization',pickle.dumps(browser))



uab = browser.execute_script(js)
print(uab)
# print(browser.execute_script(js))



# browser = redis_cli.get('chrome_browser_serialization')
# browser = pickle.loads(browser)