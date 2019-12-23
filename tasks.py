import invoke
from datetime import datetime


@invoke.task
def crawl(c):
    data_dir = "rawdata"
    now = datetime.now()
    # data_file = now.strftime('%y%m%d_%H%M%S') + "_musashinakahara.csv"
    data_file = now.strftime('%y%m%d_%H%M%S') + "_musashikosugi_search.csv"
    data_path = data_dir + "/" + data_file

    command = "cd ubereats && scrapy crawl feed -o ../" + data_path  # noqa
    invoke.run(command)
