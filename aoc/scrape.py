# AoC website scrapper

from typing import Optional, cast

import requests
from bs4 import BeautifulSoup, Tag
from markdownify import markdownify as md


def get_example(html_data: BeautifulSoup):
    main_el = cast(Optional[Tag], html_data.find("main"))
    if main_el is None:
        print("- Unable to find <main> element.")
        return
    first_pre = cast(Optional[Tag], main_el.find("code"))
    if first_pre is None:
        print("- Unable to find <code> element.")
        return
    return first_pre.text.strip()


def get_expect(html_data: BeautifulSoup):
    # The expected output is in the last <pre> element
    # after each <article> element

    # Iterate over the html_data children
    main_el = cast(Optional[Tag], html_data.find("main"))
    if main_el is None:
        print("- Unable to find <main> element.")
        return

    expectations: list[str] = []
    for article in main_el.find_all("article"):
        last_pre = None
        all_pre = article.find_all("code")
        if all_pre:
            last_pre = all_pre[-1]
        if last_pre is not None:
            expectations.append(last_pre.text.strip())
    if len(expectations) == 0:
        print("- Unable to find any <code> element.")
    return expectations


def get_day_page(day: int, year: int, session: str):
    r = requests.get(f"https://adventofcode.com/{year}/day/{day}", cookies={"session": session})
    r.raise_for_status()
    html_data = BeautifulSoup(r.text, "html.parser")
    examples = get_example(html_data)
    expects = get_expect(html_data)
    main_el = cast(Optional[Tag], html_data.find("main"))
    main_txt: Optional[str] = None
    if main_el is not None:
        main_txt = md(str(main_el))
    return examples, expects, main_txt
