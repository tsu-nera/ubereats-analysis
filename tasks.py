import invoke


@invoke.task
def crawl(c):
    data_dir = "rawdata"
    data_file = "musashinakahara.csv"
    data_path = data_dir + "/" + data_file

    command = 'cd ubereats && rm ../' + data_path + " && scrapy crawl feed -o ../" + data_path  # noqa
    invoke.run(command)
