from decouple import config
from .entries_management import get_last_entries_urls, get_entry_data

# News Entries Objects have the following structure:
# """
# {
#   main_image_url : string
#   title : string
#   subtitle : string
#   info_subtitles : string
#   info_data : string
# }
# """

def scrape_news():
    last_news_urls = []
    last_news_data = []
    
    print("Getting URLs from .env...")
    site_01_url = config("SITE_01_URL")

    print(f"Getting the most recent news from {site_01_url} ...")
    get_last_entries_urls(site_01_url, last_news_urls)
    print(f"{len(last_news_urls)} new entries obtained.")
    print(
        f"Getting the not repeated (not cached implemented yet) information from those {len(last_news_urls)} entries"
    )

    if len(last_news_urls) > 0:
        for url in last_news_urls:
            entry_data = get_entry_data(url)
            last_news_data.append(entry_data)
            print(f"Data from [{url}] successfully obtained.")
    print("Scraping process completed.")
    return last_news_data
