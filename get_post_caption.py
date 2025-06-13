from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

# You may need to install selenium-stealth and undetected-chromedriver for better stealth
# pip install selenium-stealth undetected-chromedriver


def get_linkedin_post_caption(post_url: str) -> str:
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--window-size=1920,1080')

    # For stealth, you can use undetected_chromedriver or selenium-stealth
    # Here is a basic example with selenium-stealth (if installed)
    try:
        from selenium_stealth import stealth
    except ImportError:
        stealth = None

    driver = webdriver.Chrome(options=options)
    if stealth:
        stealth(driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
                )

    try:
        driver.get(post_url)
        time.sleep(3)  # Wait for page to load, adjust as needed
        # LinkedIn post caption selector (may change, update as needed)
        # This is a best guess, may need to be updated for real LinkedIn posts
        caption = ""
        try:
            sign_in_button = driver.find_element(
                By.XPATH, '/html/body/div[4]/div/div/section/button')
            sign_in_button.click()
        except Exception:
            caption = "not a caption but Sign-in button not found."
        try:
            # Try to find the post caption
            element = driver.find_element(
                By.XPATH, '/html/body/main/section[1]/div/section/article/div[2]/p')
            caption = element.text
        except Exception:
            caption = "Could not extract caption. Selector may need update."
        return caption
    finally:
        driver.quit()


if __name__ == "__main__":
    from main import LinkedInRequest
    post_url = input("Enter LinkedIn post URL: ")
    caption = get_linkedin_post_caption(post_url)
    print(f"Caption: {caption}")
