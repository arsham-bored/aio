from bs4 import BeautifulSoup
import aiohttp

class RaiderScrapper:

    def __init__(self, link: str):
        self.link = link

    class Data:
        def __init__(self, bs: BeautifulSoup):
            self.bs: BeautifulSoup = bs

        @property
        def name(self):
            return self.bs.find("span", {"class": "rio-text-shadow--heavy"}).text

        @property
        def score(self):
            return self.bs.select_one("#content > div > div.slds-size--8-of-8 > div > div:nth-child(3) > section:nth-child(5) > div:nth-child(4) > div > div:nth-child(2) > table > thead > tr > th:nth-child(1) > span > span > span").text

    async def get_content(self):    
        """ Load website content """

        async with aiohttp.ClientSession() as session:
            async with session.get(self.link) as response:
                return await response.text()

    def parse(self, content):
        return self.Data(BeautifulSoup(content, "html.parser"))


if __name__ == "__main__":
    
    import asyncio

    async def main():
        scrapper = RaiderScrapper("https://raider.io/characters/eu/draenor/Wickedrose")
        content = await scrapper.get_content()

        print("name ->", scrapper.parse(content).name)
        print("score ->", scrapper.parse(content).score)

    loop = asyncio.get_event_loop()

    loop.run_until_complete(main())