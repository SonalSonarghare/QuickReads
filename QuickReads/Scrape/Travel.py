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

# Navigate to the Lonely Planet articles page
driver.get("https://www.lonelyplanet.com/articles")

# Wait for articles to load
wait = WebDriverWait(driver, 10)
section_element = wait.until(EC.presence_of_element_located((By.ID, "article-search-results")))

# Open a CSV file for writing
with open('Travel_articles.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
    # Define CSV writer
    writer = csv.writer(csvfile)
    
    # Write header row
    writer.writerow(['Article_ID','Category','Title', 'Title_link', 'Image', 'Date', 'Summary', 'Content'])
    article_id =699 
    # Find all articles on the page
    articles = driver.find_elements(By.TAG_NAME, 'li')
    
    # Iterate over each article
    for i in range(min(12, len(articles))):
        articles = driver.find_elements(By.TAG_NAME, 'li')
        article = articles[i]  # Get current article
        
        # Extract title
        title = article.find_element(By.CSS_SELECTOR, 'a').text
        
        # Extract title link
        title_link = article.find_element(By.CSS_SELECTOR, 'a').get_attribute("href")
        
        # Scroll into view to ensure all images load
        driver.execute_script("arguments[0].scrollIntoView();", article)
        
        # Wait for images within the current article to load
        wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "img")))
        
        # Extract images within the current article
        images = article.find_elements(By.TAG_NAME, "img")  
        image_urls = [img.get_attribute("src") for img in images]  
        # Remove brackets from image URL if available
        if image_urls:
            image_url = image_urls[0].strip("[]")
        else:
            image_url = "No image found"
            
        # Extract date
        date_element = article.find_element(By.CSS_SELECTOR, 'p.text-black-400')
        date = date_element.text.split('•')[0].strip()  # Extract date and remove unnecessary text
        
        # Extract summary
        summary = article.find_element(By.CSS_SELECTOR, 'p.line-clamp-2').text
        
        article_id += 1 
        # Navigate to the next page
        driver.get(title_link)   
        
        # Wait for content to load
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'styles_article-body___AqUn')))
        
        # Extract content
        content_elements = driver.find_elements(By.CSS_SELECTOR, '.styles_article-body___AqUn p')
        extracted_texts = [content_element.text for content_element in content_elements]
        combined_text = ' '.join(extracted_texts)
        category='Travel'
        writer.writerow([article_id,category,title, title_link, image_url, date, summary, combined_text])
        
        # Go back to the articles page
        driver.execute_script("window.history.go(-1)")
        wait.until(EC.presence_of_element_located((By.TAG_NAME, 'li')))
        
driver.quit()

print("Scraping completed. Data saved in 'Travel_articles.csv'")
