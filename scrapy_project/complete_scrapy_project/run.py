from scrapy import cmdline
cmd = "scrapy crawl shops_baseinfo"
cmd = cmd.split()
cmdline.execute(cmd)