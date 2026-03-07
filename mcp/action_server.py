import os
import time
from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager


load_dotenv()


def post_to_linkedin(content):

    linkedin_email = os.getenv("LINKEDIN_EMAIL")
    linkedin_password = os.getenv("LINKEDIN_PASSWORD")

    if not linkedin_email or not linkedin_password:
        print("❌ LinkedIn credentials missing in .env")
        return

    print("🔗 Opening LinkedIn...")

    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install())
    )

    wait = WebDriverWait(driver, 20)

    try:

        # ------------------------
        # OPEN LOGIN PAGE
        # ------------------------

        driver.get("https://www.linkedin.com/login")

        email_input = wait.until(
            EC.presence_of_element_located((By.NAME, "session_key"))
        )

        password_input = driver.find_element(By.NAME, "session_password")

        email_input.send_keys(linkedin_email)
        password_input.send_keys(linkedin_password)
        password_input.send_keys(Keys.RETURN)

        print("🔐 Logging into LinkedIn...")

        # ------------------------
        # WAIT FOR FEED
        # ------------------------

        wait.until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'share-box-feed-entry')]"))
        )

        print("✅ Login successful")

        time.sleep(3)

        # ------------------------
        # CLICK START POST
        # ------------------------

        try:
            start_post = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Start a post')]"))
            )
        except:
            start_post = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//div[contains(@class,'share-box-feed-entry__trigger')]"))
            )

        start_post.click()

        print("✍️ Opening post editor...")

        # ------------------------
        # FIND POST BOX
        # ------------------------

        post_box = wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//div[@role='textbox']"
                )
            )
        )

        post_box.send_keys(content)

        time.sleep(2)

        # ------------------------
        # CLICK POST BUTTON
        # ------------------------

        post_button = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(@class,'share-actions__primary-action')]")
            )
        )

        post_button.click()

        print("🚀 LinkedIn post published successfully!")

        time.sleep(5)

    except Exception as e:
        print(f"⚠️ LinkedIn automation error: {e}")

    finally:
        driver.quit()