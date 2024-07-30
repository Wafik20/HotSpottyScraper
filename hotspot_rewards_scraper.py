from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

def extract_rewards(page_source):
    soup = BeautifulSoup(page_source, 'html.parser')
    rewards = soup.find_all('div', class_='relative overflow-hidden rounded-lg bg-white shadow dark:bg-gray-800')

    results = []
    for reward in rewards:
        period_tag = reward.find('dt', class_='flex items-center justify-between truncate text-sm font-medium text-gray-500 dark:text-gray-300')
        if period_tag:
            period = period_tag.get_text(strip=True)
            amount = reward.find('dd', class_='mt-1 text-3xl font-semibold text-gray-900 dark:text-white').get_text(strip=True)
            results.append((period, amount))
        else:
            periods_and_amounts = reward.find_all('div', class_='px-4 py-5 sm:p-6')[0]
            dt_tags = periods_and_amounts.find_all('dt', class_='flex items-center truncate text-sm font-medium text-gray-500 dark:text-gray-300')
            dd_tags = periods_and_amounts.find_all('dd', class_='mt-1 pb-6 text-3xl font-semibold text-gray-900 dark:text-white')

            for dt, dd in zip(dt_tags, dd_tags):
                results.append((dt.get_text(strip=True), dd.get_text(strip=True)))

            lifetime_tag = periods_and_amounts.find('dt', string='Lifetime')
            if lifetime_tag:
                lifetime_amount = lifetime_tag.find_next('dd', class_='mt-1 text-3xl font-semibold text-gray-900 dark:text-white').get_text(strip=True)
                results.append(('Lifetime', lifetime_amount))

    return results

def get_platform_rewards(driver, selector, platform):
    wait = WebDriverWait(driver, 10)
    try:
        platform_element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
        platform_element.click()

        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.relative.overflow-hidden.rounded-lg.bg-white.shadow.dark\\:bg-gray-800')))
        
        page_source = driver.page_source
        rewards = extract_rewards(page_source)
        return platform, rewards
    except Exception as e:
        print(f"Error while getting rewards for platform {platform}: {e}")
        return platform, []

def get_hotspot_rewards(hotspot_id):
    chrome_options = Options()

    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.binary_location = "/usr/bin/google-chrome"

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    try:
        driver.get(f'https://app.hotspotty.net/hotspots/{hotspot_id}/rewards')
        
        platforms = {
            'iot': 'div.cursor-pointer.bg-hotspotty-100',
            'mobile': 'div.cursor-pointer.text-gray-500:nth-of-type(2)',
            'hnt': 'div.cursor-pointer.text-gray-500:nth-of-type(3)'
        }
        
        results = []
        
        for platform, selector in platforms.items():
            platform, rewards = get_platform_rewards(driver, selector, platform)
            results.append({
                'platform': platform,
                'rewards': rewards
            })
        
    finally:
        driver.quit()
        
    return results
