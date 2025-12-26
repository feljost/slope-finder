from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed

import requests
from bs4 import BeautifulSoup


def scrape_snow_report(url: str) -> dict:
    """Scrape ski resort snow report from skiresort.info"""
    response = requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        },
    )
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    data = {"pistes_km": None, "lifts": None, "snow_depth_cm": None, "updated_on": None}

    resort_info = soup.find("div", class_="overview-resort-infos")
    if resort_info:
        for item in resort_info.find_all("div", class_="info-item-con"):
            info_text = item.find("div", class_="info-text")
            if not info_text:
                continue

            text = info_text.get_text(strip=True)

            if item.find("i", class_=lambda x: x and "skirun" in x):
                data["pistes_km"] = text
            elif item.find("i", class_=lambda x: x and "lift-icon" in x):
                data["lifts"] = text
            elif item.find("i", class_="fa fa-snowflake-o"):
                data["snow_depth_cm"] = text

    update_wrapper = soup.find("div", class_="update-wrapper")
    if update_wrapper:
        date_div = update_wrapper.find("div", id="snowreport-update-date")
        if date_div and date_div.get("date"):
            data["updated_on"] = date_div.get("date")

    return data


def scrape_snow_reports_batch(urls: list[str], max_workers: int = 5) -> dict[str, dict]:
    """
    Scrape multiple ski resort snow reports in parallel.

    Args:
        urls: List of URLs to scrape
        max_workers: Maximum number of parallel requests (default: 5)

    Returns:
        Dictionary mapping each URL to its scraped data or error information
    """
    results = {}

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_url = {executor.submit(scrape_snow_report, url): url for url in urls}

        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                data = future.result()
                results[url] = {"success": True, "data": data}
            except Exception as e:
                results[url] = {"success": False, "error": str(e)}

    return results


if __name__ == "__main__":
    # Single URL example
    url = "https://www.skiresort.info/ski-resort/adelboden-lenk/snow-report/"
    report = scrape_snow_report(url)
    print("Single report:")
    print(report)

    # Batch example
    urls = [
        "https://www.skiresort.info/ski-resort/adelboden-lenk/snow-report/",
        "https://www.skiresort.info/ski-resort/zermatt-matterhorn/snow-report/",
        "https://www.skiresort.info/ski-resort/verbier-4-vallees/snow-report/",
    ]
    print("\nBatch reports:")
    batch_results = scrape_snow_reports_batch(urls, max_workers=3)
    for url, result in batch_results.items():
        print(f"\n{url}:")
        print(result)
