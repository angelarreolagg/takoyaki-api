from bs4 import BeautifulSoup
import requests


def get_last_entries_urls(site_url, site_last_news_urls):
    response = requests.get(site_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        last_news_section = soup.find("div", class_="grid auto-rows-max gap-8")

        last_news_entries = last_news_section.select(
            "article > div > header > h3 > a",
        )

        for entry in last_news_entries:
            site_last_news_urls.append(entry.get("href"))
    else:
        print(
            f"There was an error making the http request, STATUS CODE: {response.status_code}"
        )


# Last News Objects in Set will have the following structure:
# """
# {
# main_image_url : string
# title : string
# subtitle : string
# info_subtitles : string
# info_data : string
# }
# """
def get_entry_data(entry_url):
    response = requests.get(entry_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        entry_title = soup.find(
            "h1",
            class_="text-lead font-semibold tracking-tight text-balance text-3xl sm:text-4xl sm:leading-tight md:text-5xl md:leading-tight",
        ).get_text()
        entry_subtitle = soup.find(
            "p",
            class_="text-gray-600 text-xl sm:text-2xl sm:leading-tight md:text-3xl md:leading-tight",
        ).get_text()
        entry_main_image = (
            soup.select_one(
                "figure > picture > source",
                class_="-mx-6 -mt-4 overflow-hidden sm:m-0 sm:rounded",
            )
            .get("srcset")
            .split(" ")[0]
        )

        entry_data_container = soup.find(
            "div", class_="entry md:text-lg md:leading-relaxed md:font-normal"
        )
        entry_data_p_array = entry_data_container.select("p")
        entry_data_h2_array = entry_data_container.select("h2")

        # Mix all the p tags and h2 tags in order to have all the entry information in two properties, subtitles and raw_info.
        entry_data_mix_info = entry_data_p_array[0].get_text()
        entry_data_subtitles = []

        for h2_tag in entry_data_h2_array:
            entry_data_subtitles.append(h2_tag.get_text())

        for p_tag in entry_data_p_array[1:]:
            entry_data_mix_info += f" /n{p_tag.get_text()}"

        return {
            "main_image_url": entry_main_image,
            "title": entry_title,
            "subtitle": entry_subtitle,
            "info_subtitles": entry_data_subtitles,
            "info_data": entry_data_mix_info,
        }
    else:
        print(
            f"Something wrong happened fetching the data of the entry with URL {entry_url}, STATUS CODE: {response.status_code}"
        )
    return None
