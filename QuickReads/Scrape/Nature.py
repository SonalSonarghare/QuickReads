from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('disable-notifications')
chrome_options.add_argument('--disable-infobars')
chrome_options.add_argument('start-maximized')
#chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(options=chrome_options)

# Navigate to the Lonely Planet articles page
driver.get("https://phys.org/earth-news/earth-sciences/")

# Wait for articles to load
wait = WebDriverWait(driver, 10)
section_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "sorted-article")))

# Open a CSV file for writing
with open('Nature_articles.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
    # Define CSV writer
    writer = csv.writer(csvfile)
    
    # Write header row
    writer.writerow(['Title', 'Title_link', 'Image', 'Date', 'Summary', 'Content'])
    
    # Find all articles on the page
    articles = driver.find_elements(By.CLASS_NAME, "sorted-article")
    
    # Iterate over each article
    for i in range(min(10, len(articles))):
        articles = driver.find_elements(By.CLASS_NAME, "sorted-article")
        article = articles[i]  # Get current article
        
        # Extract title
        title = article.find_element(By.CLASS_NAME, '.mb-1.mb-lg-2').text.strip()
        
        # Extract title link
        title_link = article.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
        
        writer.writerow([title, title_link])
        
  
        
        
driver.quit()

print("Scraping completed. Data saved in 'Nature_articles.csv'")
