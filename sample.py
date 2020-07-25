import super_driver

driver = super_driver.get()

try:
    driver.get('https://www.google.com')
    driver.ss().print_url().print_title()
finally:
    driver.quit()
