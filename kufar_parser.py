import aiohttp
from bs4 import BeautifulSoup
import re

BASE_URL = "https://www.kufar.by/l/r~minsk/bez-posrednikov/"

CATEGORIES = {

    "phones": {
        "slug": "telefony-i-planshety",
        "query": ""
    },

    "iphone": {
        "slug": "mobilnye-telefony",
        "query": "iphone"
    },

    "laptops": {
        "slug": "noutbuki",
        "query": ""
    },

    "games": {
        "slug": "igry-pristavki",
        "query": ""
    }
}


async def get_items(category, min_price, max_price, condition, search_query):
    if category == "search":

        url = (
            f"https://www.kufar.by/l/r~minsk"
            f"?ot=1"
            f"&query={search_query}"
            f"&cnd={condition}"
            f"&prc=r:{min_price * 100},{max_price * 100}"
            f"&sort=lst.d"
        )

    else:

        category_data = CATEGORIES[category]

        category_slug = category_data["slug"]
        query = category_data["query"]

        url = (
            f"https://www.kufar.by/l/r~minsk/bez-posrednikov/{category_slug}"
            f"?query={query}"
            f"&cnd={condition}"
            f"&prc=r:{min_price * 100},{max_price * 100}"
            f"&sort=lst.d"
        )
    print(f"\nПроверяем URL:\n{url}\n")

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        )
    }

    async with aiohttp.ClientSession(headers=headers) as session:

        async with session.get(url) as response:


            html = await response.text()

    soup = BeautifulSoup(html, "lxml")

    items = []

    # ТОЛЬКО ССЫЛКИ НА ТОВАРЫ
    product_links = soup.select('a[href*="/item/"]')

    for card in product_links:

        href = card.get("href")

        if not href:
            continue

        title = card.get_text(" ", strip=True)

        if not title:
            continue

        parent = card.parent

        if not parent:
            continue

        text = parent.get_text(" ", strip=True)

        # ИЩЕМ ЦЕНУ
        match = re.search(r"(\d+)\s*р", text.lower())

        if not match:
            continue

        try:
            price = int(match.group(1))
        except:
            continue

        # ДОП ПРОВЕРКА ЦЕНЫ
        if not (min_price <= price <= max_price):
            continue

        # УДАЛЯЕМ МУСОРНЫЕ QUERY PARAMS
        clean_href = href.split("?")[0]

        if clean_href.startswith("http"):
            item_url = clean_href
        else:
            item_url = BASE_URL + clean_href

        items.append({
            "title": title,
            "price": price,
            "url": item_url
        })

    print(f"Найдено товаров: {len(items)}")

    return items