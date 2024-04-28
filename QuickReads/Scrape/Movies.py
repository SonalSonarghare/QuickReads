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
driver.get("https://theconversation.com/global/topics/film-1175")

# Wait for articles to load (if necessary)
wait = WebDriverWait(driver, 10)
section_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".clearfix.placed.analysis.published")))

# Open a CSV file for writing
with open('Movies_articles.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
    # Define CSV writer
    writer = csv.writer(csvfile)

    # Write header row
    writer.writerow(['Article_ID','Category','Title', 'Title_link', 'Image', 'Date', 'Summary', 'Content'])

    # Find all articles on the page
    articles = driver.find_elements(By.CSS_SELECTOR, ".clearfix.placed.analysis.published")
    article_id = 399
    # Iterate over each article
    for i in range(min(12, len(articles))):
        articles = driver.find_elements(By.CSS_SELECTOR, ".clearfix.placed.analysis.published")
        article = articles[i]  # Get current article

        # Extract title
        title = article.find_element(By.CSS_SELECTOR, ".article--header h2").text

        # Extract title link
        title_link= article.find_element(By.CSS_SELECTOR, ".article-link").get_attribute("href")
        # Scroll into view to ensure all images load
        driver.execute_script("arguments[0].scrollIntoView();",article)

        # Wait for images within the current article to load
        wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "img")))

        # Extract images within the current article
        image_div=article.find_element(By.CSS_SELECTOR, ".article-link")
        images = image_div.find_elements(By.TAG_NAME, "img")
        image_urls = [img.get_attribute("src") for img in images]
        # Remove brackets from image URL if available
        if image_urls:
            image_url = image_urls[0].strip("[]")
        else:
            image_url = "No image found"

        # Extract date
        date = article.find_element(By.CSS_SELECTOR, ".clearfix.placed.analysis.published time"   ).text

        # Extract summary
        summary = article.find_element(By.CSS_SELECTOR, ".content").text
        article_id += 1 
        driver.get(title_link)

        # Wait for the "READ MORE" link to be clickable
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "p")))   # Navigate to the next page
        #date = driver.find_element(By.CSS_SELECTOR, ".timestamps").text
        #li_elements = driver.find_elements(By.CSS_SELECTOR, ".article-body.css-d2znx6.undefined li")
        #extracted_li = [li_element.text for li_element in li_elements]

        # Extract text from paragraph elements within the article body
        p_elements = driver.find_elements(By.TAG_NAME, "p")
        extracted_texts = [p_element.text for p_element in p_elements]
        combined_text = ' '.join( extracted_texts)
        category='Movies'
        # Write data to CSV
        writer.writerow([article_id,category,title,title_link,image_url,date,summary,combined_text])
        driver.execute_script("window.history.go(-1)")
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,  ".clearfix.placed.analysis.published")))
        #articles = driver.find_elements(By.CSS_SELECTOR, ".css-18vzruc")

# Close the WebDriver
driver.quit()

print("Scraping completed. Data saved in 'Movies_articles.csv'")






