from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
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
driver.get("https://www.edutopia.org/topic/education-trends")

# Wait for articles to load (if necessary)
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".css-1abeq1d")))


# Find and click the "Close" button
#close_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, ".css-1q1lrcw")))
#close_button.click()

# Open a CSV file for writing
with open('Education_articles.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
    # Define CSV writer
    writer = csv.writer(csvfile)

    # Write header row
    writer.writerow(['Article_ID','Category', 'Title', 'Title_link', 'Image', 'Date', 'Summary', 'Content'])

    article_id =299   # Initialize article ID counter

    # Find all articles on the page
    articles = driver.find_elements(By.CSS_SELECTOR, ".css-18i7m94")

    # Iterate over each article
    for i in range(min(12, len(articles))):
        articles = driver.find_elements(By.CSS_SELECTOR, ".css-18i7m94")
        article = articles[i]  # Get current article

        # Extract title
        title = article.find_element(By.CSS_SELECTOR, ".css-gm5mek").text.strip()

        # Extract title link
        title_link = article.find_element(By.CSS_SELECTOR, ".css-13ygqr6").get_attribute("href")

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


        # Extract summary
        summary = article.find_element(By.CSS_SELECTOR, ".css-z84tn2").text.strip()

        article_id += 1 

        # Extract content from the article page
        # Find and click the "Close" button
        #close_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, ".css-1q1lrcw")))
        #close_button.click()
        driver.get(title_link)

        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,".article-wrap")))

        # Extract date
        #date = article.find_element(By.CSS_SELECTOR, ".date-text.css-m6gbk").text
        #Date = article.find_element(By.CSS_SELECTOR, ".date-text.css-m6gbk")
        #Date = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".date-text.css-m6gbk")))


        wait = WebDriverWait(driver, 10)  # Adjust the timeout as necessary

        try:
           Date = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".date-text.css-m6gbk"))).text  
        except:
           try:
              Date = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".date-text.css-1bxy5d4"))).text
           except:
              print("Element not found.")



        # Extract text from paragraph elements within the article body
        p_elements = driver.find_elements(By.CSS_SELECTOR, ".css-vll9ls.rich-text p")
        extracted_texts = [p_element.text for p_element in p_elements]

        # Combine all extracted text into a single string
        combined_text = ' '.join( extracted_texts)
        
        category='Education'
        # Write data to CSV
        writer.writerow([article_id,category, title, title_link, image_url, Date, summary, combined_text])

        # Navigate back to the news page and re-find the articles
        driver.execute_script("window.history.go(-1)")
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".css-1abeq1d")))
        #articles = driver.find_elements(By.CSS_SELECTOR, ".css-z1rm9k")

# Close the WebDriver
driver.quit()

print("Scraping completed. Data saved in 'Education_articles.csv'")