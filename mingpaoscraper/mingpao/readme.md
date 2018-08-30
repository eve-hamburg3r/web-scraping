This scraper implement the use of scrapy-splash due to the javascript rendering.
Before using this code, pls install the docker and scrapy-splash.
You can refer it to `https://www.youtube.com/watch?v=VvFC93vAB7U`

1. Open terminal
2. Setting working directory at /mingpao/mingpao/spiders
3. Enter `scrapy runspider mingpaoscrapy.py -o output.csv -a days=30`
*Change the `days=` for the days of news you wanna scrape.

* You can see the sample result in /mingpao/mingpao/spiders
