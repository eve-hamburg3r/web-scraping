1. Open terminal
2. Setting working directory at /HK01Scrapper/hk01/hk01/spiders
3. Enter `scrapy runspider hk01scrapy.py -o test.csv -a parse_num=<latest news id> -a days=<days of news>`
example: `scrapy runspider hk01scrapy.py -o test.csv -a parse_num=228242 -a days=1`

* You can see the sample result at /hk01/hk01/test.csv .
