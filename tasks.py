import invoke
from datetime import datetime

RAWDATA_SHOPS_DIR = "rawdata/shops"

STATION_TYPE_NAKAHARA = "MUSASHINAKAHARA"
STATION_TYPE_SHINJO = "MUSASHISHINJO"
STATION_TYPE_KOSUGI = "MUSASHIKOSUGI"
STATION_TYPE_MIZONOKUCHI = "MUSASHIMIZONOKUCHI"
STATION_TYPE_ALL = "ALL"


def get_filename_prefix():
    now = datetime.now()
    # return now.strftime('%y%m%d_%H%M%S')
    return now.strftime('%y%m%d')


def get_crawl_comand(base_file_name, station_type):
    file_name = get_filename_prefix() + "_" + base_file_name
    data_path = RAWDATA_SHOPS_DIR + "/" + file_name

    return "cd ubereats && scrapy crawl shop -a type={} -o ../{}".format(
        station_type, data_path)


@invoke.task
def crawl_musashinakahara(c):
    base_file_name = "musashinakahara.csv"
    command = get_crawl_comand(base_file_name, STATION_TYPE_NAKAHARA)
    invoke.run(command)


@invoke.task
def crawl_musashishinjo(c):
    base_file_name = "musashishinjo.csv"
    command = get_crawl_comand(base_file_name, STATION_TYPE_SHINJO)
    invoke.run(command)


@invoke.task
def crawl_musashikosugi(c):
    base_file_name = "musashikosugi.csv"
    command = get_crawl_comand(base_file_name, STATION_TYPE_KOSUGI)
    invoke.run(command)


@invoke.task
def crawl_musashimizonokuchi(c):
    base_file_name = "musashimizonokuchi.csv"
    command = get_crawl_comand(base_file_name, STATION_TYPE_MIZONOKUCHI)
    invoke.run(command)


@invoke.task
def crawl(c):
    base_file_name = "all_stations.csv"
    command = get_crawl_comand(base_file_name, STATION_TYPE_ALL)
    invoke.run(command)


@invoke.task
def post(c, url):
    command = "cd ubereats && rm ../rawdata/shops/shop.csv && scrapy crawl -a url={} post -o ../rawdata/shops/shop.csv".format(
        url)  # noqa
    invoke.run(command)


@invoke.task
def trip(c, year, month, day):
    data_dir = "rawdata/trips"
    # now = datetime.now()
    # data_file = now.strftime('%y%m%d_%H%M%S') + "_trips.csv"
    data_file = "latest_trips.csv"
    data_path = data_dir + "/" + data_file

    command = "cd ubereats && rm ../{} -f && scrapy crawl -a year={} -a month={} -a day={} trip -o ../{}".format(
        data_path, year, month, day, data_path)  # noqa
    invoke.run(command)


@invoke.task
def merge_trip(c):
    command = "python merge_trip.py"
    invoke.run(command)


@invoke.task
def shell(c):
    command = "scrapy shell file://$PWD/tmp/target.html"
    invoke.run(command)
