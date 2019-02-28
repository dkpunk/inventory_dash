from selenium import webdriver
import time
import sys
server=sys.argv[1]
# Option 1 - with ChromeOptions
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox') # required when running as root user. otherwise you would get no sandbox errors. 
driver = webdriver.Chrome(chrome_options=chrome_options)
# Option 2 - with pyvirtualdisplay
from pyvirtualdisplay import Display 
display = Display(visible=0, size=(1024, 768)) 
display.start() 
driver = webdriver.Chrome(chrome_options=chrome_options)
#  service_args=['--verbose', '--log-path=/tmp/chromedriver.log'])
# Log path added via service_args to see errors if something goes wrong (always a good idea - many of the errors I encountered were described in the logs)
# And now you can add your website / app testing functionality: 
driver.get('http://velocity.support.envestnet.cloud/search-results?searchString='+server) 
time.sleep(10)
#print(driver.find_element_by_css_selector('#root'))a
print(str(driver.page_source.encode('utf-8')))
# driver.click...
driver.quit()
