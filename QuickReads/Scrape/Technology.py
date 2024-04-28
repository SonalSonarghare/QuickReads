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
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(options=chrome_options)

# Navigate to the Healthline news page
driver.get("https://www.bbc.com/innovation")

# Wait for articles to load (if necessary)
wait = WebDriverWait(driver, 10)
section_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="liverpool-card"]')))

# Open a CSV file for writing
with open('Technology_articles.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
    # Define CSV writer
    writer = csv.writer(csvfile)
    
    # Write header row
    writer.writerow(['Article_ID','Category','Title', 'Title_link', 'Image', 'Date', 'Summary','Content'])
    
    # Find all articles on the page
    articles = driver.find_elements(By.CSS_SELECTOR, '[data-testid="liverpool-card"]')
    article_id = 199
    # Iterate over each article
    for i in range(min(13, len(articles))):
        articles = driver.find_elements(By.CSS_SELECTOR, '[data-testid="liverpool-card"]')
        article = articles[i]  # Get current article
        
        # Extract title
        title = article.find_element(By.CSS_SELECTOR, '[data-testid="card-headline"]').text
        
        # Extract title link
        title_link= article.find_element(By.CSS_SELECTOR, '[data-testid="internal-link"]').get_attribute("href")
        # Scroll into view to ensure all images load
        driver.execute_script("arguments[0].scrollIntoView();",article)
        
        # Wait for images within the current article to load
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".sc-a898728c-1.jWZsJP")))
        
        # Extract images within the current article
        image_div=article.find_element(By.CSS_SELECTOR, ".sc-a898728c-1.jWZsJP")
        images = image_div.find_elements(By.TAG_NAME, "img")  
        image_urls = [img.get_attribute("src") for img in images]  
        # Remove brackets from image URL if available
        if image_urls:
            image_url = image_urls[0].strip("[]")
        else:
            image_url = "No image found"
        
        # Extract date
        date = article.find_element(By.CSS_SELECTOR, '[data-testid="card-metadata-lastupdated"]').text
        
        # Extract summary
        summary = article.find_element(By.CSS_SELECTOR, '[data-testid="card-description"]').text
        
        article_id += 1 
        driver.get(title_link)   # Navigate to the next page
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "sc-e1853509-0.bmLndb")))
        
        # Extract text from paragraph elements within the article body
        p_elements = driver.find_elements(By.CLASS_NAME, "sc-e1853509-0.bmLndb")
        extracted_texts = [p_element.text for p_element in p_elements]

        # Combine all extracted text into a single string
        combined_text = ' '.join(extracted_texts)
        category='Technology'
        # Write data to CSV
        writer.writerow([article_id,category,title,title_link,image_url,date,summary,combined_text])
        driver.execute_script("window.history.go(-1)")
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[data-testid="liverpool-card"]')))
        #articles = driver.find_elements(By.CSS_SELECTOR, ".css-18vzruc")

# Close the WebDriver
driver.quit()

print("Scraping completed. Data saved in 'Technology_articles.csv'")






