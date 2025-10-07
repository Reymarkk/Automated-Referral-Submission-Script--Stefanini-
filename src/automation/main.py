"""
Automated job application clicker for Stefanini site.
Now directly loads a jobdetails.asp link and clicks Apply.
"""

from __future__ import annotations

import os
import pathlib
import time
from dataclasses import dataclass

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@dataclass
class Settings:
    url: str
    username: str | None
    password: str | None
    email: str | None             # <-- added this line
    resume_file: pathlib.Path
    browser: str = "firefox"
    headless: bool = False

def get_settings() -> Settings:
    load_dotenv()
    url = os.getenv(
        "TARGET_URL",
        "https://jobs2.smartsearchonline.com/stefanini/jobs/jobdetails.asp?jo_num=61331&apply=yes&country=Phillip&proximity=25&",
    )
    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")
    email = os.getenv("EMAIL")  # <-- added this
    resume_file = pathlib.Path(os.getenv("RESUME_FILE", "data/resume.pdf")).expanduser().resolve()
    browser = os.getenv("BROWSER", "firefox").lower()
    headless = os.getenv("HEADLESS", "false").lower() == "true"
    return Settings(url, username, password, email, resume_file, browser, headless)



def create_driver(browser: str = "firefox", headless: bool = False):
    if browser == "chrome":
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
        return webdriver.Chrome(options=options)

    # Default to Firefox
    options = webdriver.FirefoxOptions()
    if headless:
        options.add_argument("-headless")
    return webdriver.Firefox(options=options)


def main() -> None:
    cfg = get_settings()

    if not cfg.resume_file.exists():
        raise SystemExit(f"Resume file not found: {cfg.resume_file}")

    driver = create_driver(cfg.browser, cfg.headless)
    driver.set_window_size(1280, 900)
    wait = WebDriverWait(driver, 20)

    try:
        # Step 1: Go directly to the job details page
        driver.get(cfg.url)

        # Step 2: Wait for and click Apply
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#cmdApply"))).click()

        # Step 3a: Fill in the email
        email_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#email")))
        email_input.clear()
        email_input.send_keys(cfg.email)
        if not cfg.email:
            raise SystemExit("EMAIL is not set in your .env. Add EMAIL=\"you@example.com\" and try again.")


        # Step 3b: Check the "Apply as guest" checkbox
        guest_checkbox = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#asguest")))
        if not guest_checkbox.is_selected():
            guest_checkbox.click()

        # Step 3c: Click the Continue button
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#creataccountbutton"))).click()

        # Keep window open briefly in non-headless mode
        time.sleep(3)

        print("✅ Apply flow completed: email filled, guest checked, continued.")
    finally:
        driver.quit()




if __name__ == "__main__":
    main()
