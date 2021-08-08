import super_driver

url = "https://httpbin.org/ip"
driver = super_driver.get()

try:
  driver.get(url)
  body = driver.find_element_by_css_selector("body").text
  print(body)
except Exception as e:
  driver.ss().print_url().print_title()
  raise e
finally:
  driver.quit()
