from celery import shared_task
from .services.scraper.scraper_service import scrape_news
from .services.ai.ai_service import rewrite_entry_with_ai
from .serializers import BlogProcessedEntriesSerializer


@shared_task
def info_source_scraper():
    print("--- Initializing Scraper ---")
    # Scraping service
    raw_scraped_data = scrape_news()
    # Process raw data with IA
    for entry in raw_scraped_data:
        success = process_entry(entry)
        if not success:
            print(f"Skipping entry due to error: {entry.get('title')}")
    return f"{len(raw_scraped_data)} entries processed sequentially."


def process_entry(entry):
    data_for_ai = entry.copy()
    data_for_ai.pop('main_image_url', None)
    try:
        print(f"processing with AI [{data_for_ai.get('title')}]")
        processed = rewrite_entry_with_ai(data_for_ai)
        if processed:
            processed['main_image_url'] = entry.get('main_image_url')
            print(f"SUCCESS PROCESS: {processed['title']}")
            data_to_save = {"data": processed}
            serializer = BlogProcessedEntriesSerializer(data=data_to_save)
            if serializer.is_valid():
                serializer.save()
                print(f"SUCCESS SAVING: {processed['title']}")
            else:
                print(f"Error saving entry {entry.get('title')}: {serializer.errors}")
            return True
    except Exception as e:
        print(f"Error processing {entry.get('title')}: {e}")
        return False
