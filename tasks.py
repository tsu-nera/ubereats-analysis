import invoke
from datetime import datetime


@invoke.task
def crawl(c):
    data_dir = "rawdata"
    now = datetime.datetime.now()
    data_file = now.strftime('%Y%m%d_%H%M%S') + "_musashinakahara.csv"
    data_path = data_dir + "/" + data_file

    command = 'cd ubereats && rm ../' + data_path + " && scrapy crawl feed -o ../" + data_path  # noqa
    invoke.run(command)
