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
driver.get("https://www.nature.org/en-us/magazine/magazine-articles/")

# Wait for articles to load (if necessary)
wait = WebDriverWait(driver, 10)
section_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".bs_col-12.bs_col-md-6.bs_col-sm-6.bs_col-lg-4.bs_d-flex.bs_align-items-stretch")))

# Open a CSV file for writing
with open('Nature_articles.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
    # Define CSV writer
    writer = csv.writer(csvfile)

    # Write header row
    writer.writerow(['Article_ID','Category','Title', 'Title_link', 'Image', 'Date', 'Summary', 'Content'])
    article_id =599  
    # Find all articles on the page
    articles = driver.find_elements(By.CSS_SELECTOR, ".bs_col-12.bs_col-md-6.bs_col-sm-6.bs_col-lg-4.bs_d-flex.bs_align-items-stretch")
    if not articles:
      print("No articles found using the CSS selector.")

    # Iterate over each article
    for i in range(min(12, len(articles))):
        articles = driver.find_elements(By.CSS_SELECTOR, ".bs_col-12.bs_col-md-6.bs_col-sm-6.bs_col-lg-4.bs_d-flex.bs_align-items-stretch")
        article = articles[i]  # Get current article

        # Extract title
        title = article.find_element(By.CSS_SELECTOR, ".fz-v12.lh-v15.c-cards-articles__title.family-serif").text

        # Extract title link
        title_link= article.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
        # Scroll into view to ensure all images load
        driver.execute_script("arguments[0].scrollIntoView();",article)

        # Wait for images within the current article to load
        wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "img")))

        # Extract images within the current article
        image_div=article.find_element(By.CSS_SELECTOR, ".c-cards-articles__card-container.border-primary")
        images = image_div.find_elements(By.TAG_NAME, "img")
        image_urls = [img.get_attribute("src") for img in images]
        # Remove brackets from image URL if available
        if image_urls:
            image_url = image_urls[0].strip("[]")
        else:
            image_url = "No image found"

        # Extract date
        #date = article.find_element(By.CSS_SELECTOR, ".family-sans.fw-v4.fz-v4.lh-v2.c-cards-articles__byline.txt-clr-g2" ).text
        date_element = article.find_element(By.CSS_SELECTOR, ".family-sans.fw-v4.fz-v4.lh-v2.c-cards-articles__byline.txt-clr-g2").text
        # Check if the date contains "By" and remove it
        if "By" in date_element:
            date_element = date_element.split("|")[1].strip()
        # Extract date in the format "Nov 09, 2023"
        date = date_element.split("|")[-1].strip()

        # Extract summary
        summary = article.find_element(By.CSS_SELECTOR, ".family-sans.fz-v7.lh-v9.c-cards-articles__excerpt.txt-clr-g2").text
        article_id += 1 
        driver.get(title_link)

        # Wait for the "READ MORE" link to be clickable
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".template-body-container")))   # Navigate to the next page
        #date = driver.find_element(By.CSS_SELECTOR, ".timestamps").text
        #li_elements = driver.find_elements(By.CSS_SELECTOR, ".article-body.css-d2znx6.undefined li")
        #extracted_li = [li_element.text for li_element in li_elements]
        #date = article.find_element(By.CSS_SELECTOR, ".text-uppercase.text-low" ).text

        # Extract text from paragraph elements within the article body
        p_elements = driver.find_elements(By.CSS_SELECTOR, ".rich-text-editor p")
        extracted_texts = [p_element.text for p_element in p_elements]
        combined_text = ' '.join( extracted_texts)
        category='Nature'
        # Write data to CSV
        writer.writerow([article_id,category,title,title_link,image_url,date,summary,combined_text])
        driver.execute_script("window.history.go(-1)")
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".bs_col-12.bs_col-md-6.bs_col-sm-6.bs_col-lg-4.bs_d-flex.bs_align-items-stretch")))
        #articles = driver.find_elements(By.CSS_SELECTOR, ".css-18vzruc")

# Close the WebDriver
driver.quit()

print("Scraping completed. Data saved in 'Nature_articles.csv'")






