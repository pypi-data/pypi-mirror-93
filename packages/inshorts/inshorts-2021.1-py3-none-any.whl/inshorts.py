from colorama import init, Fore, Back, Style
import click
from scrapper import fetchNews

@click.command()
@click.option("--category",
              default="",
              type=click.Choice(["", "national", "business", "sports", "world",
                            "politics", "technology", "startup", "entertainment",
                            "miscellaneous", "hatke", "science", "automobile"]))
def inshorts(category):
    news = fetchNews(category)
    if news['success'] == False:
        print(Fore.RED + Style.BRIGHT + news["errorMessage"] + Style.RESET_ALL)
    else:
        for newsItem in news["data"]:
            print(Style.BRIGHT + newsItem["title"].replace("\n", "") +
                  Style.RESET_ALL + f" on {newsItem['date'].replace(',', ', ')} at {newsItem['time']}")
            print(newsItem["content"])
            print()


if __name__ == "__main__":
    init()
    inshorts()