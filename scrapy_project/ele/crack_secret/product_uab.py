from selenium import webdriver


def product_uab():
    browser = webdriver.Chrome(executable_path='chromedriver')

    with open('tarantula/spiders/elem/crack_secret/x-uab-deocde.js', 'r') as f:
        js = f.read()
    uab = browser.execute_script(js)
    browser.close()
    return uab

def product_browser_js():
    browser = webdriver.Chrome(executable_path='chromedriver')
    with open('tarantula/spiders/elem/crack_secret/x-uab-deocde.js', 'r') as f:
        js = f.read()
    return browser,js



