import os
import invoke

import ubereats.ubereats.constants.shop as SC

RAWDATA_SHOPS_DIR = "rawdata/shops"


def get_crawl_command(base_file_name, station_type):
    data_path = RAWDATA_SHOPS_DIR + "/" + base_file_name

    return "cd ubereats && scrapy crawl shop -a station_type={} -o ../{}".format(
        station_type, data_path)


def remove_rawfile(file_name):
    file_path = os.path.join(RAWDATA_SHOPS_DIR, file_name)
    if os.path.exists(file_path):
        os.remove(file_path)


@invoke.task
def crawl_nakahara(c):
    base_file_name = "musashinakahara.csv"
    remove_rawfile(base_file_name)
    command = get_crawl_command(base_file_name, SC.STATION_TYPE_NAKAHARA)
    invoke.run(command)


@invoke.task
def crawl_shinjo(c):
    base_file_name = "musashishinjo.csv"
    remove_rawfile(base_file_name)
    command = get_crawl_command(base_file_name, SC.STATION_TYPE_SHINJO)
    invoke.run(command)


@invoke.task
def crawl_kosugi(c):
    base_file_name = "musashikosugi.csv"
    remove_rawfile(base_file_name)
    command = get_crawl_command(base_file_name, SC.STATION_TYPE_KOSUGI)
    invoke.run(command)


@invoke.task
def crawl_mizonokuchi(c):
    base_file_name = "musashimizonokuchi.csv"
    remove_rawfile(base_file_name)
    command = get_crawl_command(base_file_name, SC.STATION_TYPE_MIZONOKUCHI)
    invoke.run(command)


@invoke.task
def crawl_kawasaki(c):
    base_file_name = "kawasaki.csv"
    remove_rawfile(base_file_name)
    command = get_crawl_command(base_file_name, SC.STATION_TYPE_KAWASAKI)
    invoke.run(command)


@invoke.task
def crawl_jiyugaoka(c):
    base_file_name = "jiyugaoka.csv"
    remove_rawfile(base_file_name)
    command = get_crawl_command(base_file_name, SC.STATION_TYPE_JIYUGAOKA)
    invoke.run(command)


@invoke.task
def crawl_hiyoshi(c):
    base_file_name = "hiyoshi.csv"
    remove_rawfile(base_file_name)
    command = get_crawl_command(base_file_name, SC.STATION_TYPE_HIYOSHI)
    invoke.run(command)


@invoke.task
def crawl_miyazakidai(c):
    base_file_name = "miyazakidai.csv"
    remove_rawfile(base_file_name)
    command = get_crawl_command(base_file_name, SC.STATION_TYPE_MIYAZAKIDAI)
    invoke.run(command)


@invoke.task
def crawl_motosumiyoshi(c):
    base_file_name = "motosumiyoshi.csv"
    remove_rawfile(base_file_name)
    command = get_crawl_command(base_file_name, SC.STATION_TYPE_MOTOSUMIYOSHI)
    invoke.run(command)


@invoke.task
def crawl(c):
    crawl_nakahara(c)
    crawl_kosugi(c)
    crawl_shinjo(c)
    crawl_mizonokuchi(c)
    crawl_miyazakidai(c)
    crawl_motosumiyoshi(c)


# def crawl(c):
#     base_file_name = "all_stations.csv"
#     command1 = get_crawl_command(base_file_name, STATION_TYPE_ALL)
#     invoke.run(command1)

#     file_name = get_filename_prefix() + "_" + base_file_name
#     command2 = "python ubereats/utils/merge_shops.py {}".format(file_name)
#     invoke.run(command2)


@invoke.task
def post(c, url):
    command = "cd ubereats && rm -f ../rawdata/shops/shop.csv && scrapy crawl -a url={} post -o ../rawdata/shops/shop.csv".format(  # noqa
        url)  # noqa
    invoke.run(command)


@invoke.task
def trip(c, year, month, day):
    data_dir = "rawdata/trips"
    # now = datetime.now()
    # data_file = now.strftime('%y%m%d_%H%M%S') + "_trips.csv"
    data_file = "latest_trips.csv"
    data_path = data_dir + "/" + data_file

    if os.path.exists(data_path):
        os.remove(data_path)
    command = "cd ubereats && scrapy crawl -a year={} -a month={} -a day={} trip -o ../{} -t 'csv'".format(
        int(year), int(month), int(day), data_path)  # noqa
    invoke.run(command)


@invoke.task
def merge_trip(c):
    command = "python ubereats/utils/merge_trip.py"
    invoke.run(command)


@invoke.task
def merge_shops(c):
    command = "python ubereats/utils/merge_shops.py"
    invoke.run(command)


@invoke.task
def merge_shops_yokohama(c):
    command = "python ubereats/utils/merge_shops_yokohama.py"
    invoke.run(command)


@invoke.task
def merge_shop(c):
    command = "python ubereats/utils/merge_shop.py"
    invoke.run(command)


@invoke.task
def update_premerge(c):
    command = "python ubereats/utils/update_premerge_df.py"
    invoke.run(command)
    command = "python ubereats/utils/check_diff.py"
    invoke.run(command)


@invoke.task
def shell(c):
    command = "scrapy shell file://$PWD/tmp/target.html"
    invoke.run(command)


@invoke.task
def eval_trip(c):
    command_base = "jupyter nbconvert --to notebook --ExecutePreprocessor.timeout=-1 --execute --inplace --ExecutePreprocessor.kernel_name=python"
    file_path = os.path.join("notebooks", "trip_analysis.ipynb")
    command = " ".join([command_base, file_path])

    invoke.run(command)
