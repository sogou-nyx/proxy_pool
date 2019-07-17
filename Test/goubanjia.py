import time

from apscheduler.schedulers.background import BackgroundScheduler

from Util.utilFunction import getHtmlTree
from lxml import html

def freeProxyFifth():
    """
    guobanjia http://www.goubanjia.com/
    :return:
    """
    url = "http://www.goubanjia.com/"
    tree = getHtmlTree(url)
    etree = html.etree
    proxy_list = tree.xpath('//td[@class="ip"]')
    # 此网站有隐藏的数字干扰，或抓取到多余的数字或.符号
    # 需要过滤掉<p style="display:none;">的内容
    xpath_str = """.//*[not(contains(@style, 'display: none'))
                                    and not(contains(@style, 'display:none'))
                                    and not(contains(@class, 'port'))
                                    ]/text()
                           """

    for each_proxy in proxy_list:
        print(etree.tostring(each_proxy))
        try:
            # :符号裸放在td下，其他放在div span p中，先分割找出ip，再找port
            ip_addr = ''.join(each_proxy.xpath(xpath_str))
            # HTML中的port是随机数，真正的端口编码在class后面的字母中。
            # 比如这个：
            # <span class="port CFACE">9054</span>
            # CFACE解码后对应的是3128。

            port = 0
            for _ in each_proxy.xpath(".//span[contains(@class, 'port')]"
                                      "/attribute::class")[0].replace("port ", ""):
                port *= 10
                port += (ord(_) - ord('A'))
            port /= 8

            print('{}:{}'.format(ip_addr, int(port)))
        except Exception as e:
            print(e)


def job():
    print('job 3s')
    time.sleep(5)


if __name__ == '__main__':
    sched = BackgroundScheduler(timezone='MST', job_defaults=job_defaults)
    sched.add_job(job, 'interval', id='3_second_job', seconds=3)
    sched.start()

    while True:
        print('main 1s')
        time.sleep(1)
