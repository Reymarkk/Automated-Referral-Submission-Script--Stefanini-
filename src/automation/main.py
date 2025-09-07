"""
Minimal Selenium template for filling a web form and uploading a file.
Uses Selenium Manager (built into Selenium 4.6+) to auto-manage drivers.
Works with Firefox (default) or Chrome/Chromium if installed.

Before running:
  1) Create a virtualenv and install requirements (see README.md)
  2) Copy .env.example to .env and edit values
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
    resume_file: pathlib.Path
    browser: str = "firefox"  # "firefox" or "chrome"
    headless: bool = False


def get_settings() -> Settings:
    load_dotenv()
    url = os.getenv("TARGET_URL", "https://example.com/form")
    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")
    resume_file = pathlib.Path(os.getenv("RESUME_FILE", "data/resume.pdf")).expanduser().resolve()
    browser = os.getenv("BROWSER", "firefox").lower()
    headless = os.getenv("HEADLESS", "false").lower() == "true"
    return Settings(url, username, password, resume_file, browser, headless)


def create_driver(browser: str = "firefox", headless: bool = False):
    if browser == "chrome":
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
        # For Wayland sessions on Linux, you can uncomment the next line if needed
        # options.add_argument("--ozone-platform=wayland")
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
        driver.get(cfg.url)

        # Wait for the "Job Details" button and click it
        wait.until(EC.element_to_be_clickable((By.XPATH, "//a[text()='Job Details']"))).click()

        # Example: wait for a field and type into it
        # Adjust selectors to match your target site!
        # name_input = wait.until(EC.element_to_be_clickable((By.NAME, "full_name")))
        # name_input.send_keys("Jane Doe")

        # Example: file upload via <input type="file">
        # file_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']")))
        # file_input.send_keys(str(cfg.resume_file))

        # Example: click submit
        # submit_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
        # submit_btn.click()

        # Keep the window for a short while for inspection in non-headless mode
        time.sleep(2)

        print("✅ Script finished (template). Edit selectors to suit your form.")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
