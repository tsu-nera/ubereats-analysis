import invoke
from datetime import datetime


@invoke.task
def crawl(c):
    data_dir = "rawdata/shops"
    now = datetime.now()
    data_file = now.strftime('%y%m%d_%H%M%S') + "_musashinakahara.csv"
    # data_file = now.strftime('%y%m%d_%H%M%S') + "_musashikosugi_search.csv"
    data_path = data_dir + "/" + data_file

    command = "cd ubereats && scrapy crawl shop -o ../" + data_path  # noqa
    invoke.run(command)


@invoke.task
def post(c, url):
    command = "cd ubereats && rm ../rawdata/shops/shop.csv && scrapy crawl -a url={} post -o ../rawdata/shops/shop.csv".format(
        url)  # noqa
    invoke.run(command)


@invoke.task
def trip(c, year, month, day):
    data_dir = "rawdata/trips"
    now = datetime.now()
    data_file = now.strftime('%y%m%d_%H%M%S') + "_trips.csv"
    data_path = data_dir + "/" + data_file

    command = "cd ubereats && scrapy crawl -a year={} -a month={} -a day={} trip -o ../{}".format(
        year, month, day, data_path)  # noqa
    invoke.run(command)


@invoke.task
def shell(c):
    command = "scrapy shell file://$PWD/tmp/target.html"
    invoke.run(command)
