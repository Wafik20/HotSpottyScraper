# HotspottyScraper
This Python script scrapes reward information for Helium hotspots from the Hotspotty website using Selenium and BeautifulSoup.

## Features

- Scrapes reward information for IoT, Mobile, and HNT platforms
- Extracts period and amount data for each platform
- Handles different reward display formats

## Requirements

- Python 3.6+
- Selenium
- BeautifulSoup4
- webdriver_manager

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/hotspot-rewards-scraper.git
   cd hotspot-rewards-scraper
   ```

2. Install the required packages:
   ```
   pip install selenium beautifulsoup4 webdriver-manager
   ```

3. Ensure you have Google Chrome installed on your system.

## Usage

1. Import the `get_hotspot_rewards` function from the script:
   ```python
   from hotspot_scraper import get_hotspot_rewards
   ```

2. Call the function with a hotspot ID:
   ```python
   hotspot_id = "your_hotspot_id_here"
   rewards = get_hotspot_rewards(hotspot_id)
   print(rewards)
   ```

## Function Details

### `get_hotspot_rewards(hotspot_id)`

This is the main function that orchestrates the scraping process.

Parameters:
- `hotspot_id` (str): The ID of the hotspot to scrape rewards for.

Returns:
- A list of dictionaries, each containing:
  - `platform` (str): The platform name ('iot', 'mobile', or 'hnt')
  - `rewards` (list): A list of tuples, each containing (period, amount)

## Helper Functions

### `extract_rewards(page_source)`

Extracts reward information from the page source using BeautifulSoup.

### `get_platform_rewards(driver, selector, platform)`

Navigates to a specific platform's rewards section and extracts the rewards.

## Notes
- Make sure you have the necessary permissions to scrape the Hotspotty website.
- The script may need updates if the website's structure changes.

## License

[MIT License](https://opensource.org/licenses/MIT)

## Contributing

Contributions, issues, and feature requests are welcome. Feel free to check [issues page](https://github.com/yourusername/hotspot-rewards-scraper/issues) if you want to contribute.

## Author

Wafik Tawfik @ July 30 2024
