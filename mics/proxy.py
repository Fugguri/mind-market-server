import os


def set_proxy():
    os.environ["HTTP_PROXY"] = 'http://9gfWr9:g0LSUy@131.108.17.194:9799/'
    os.environ["HTTPS_PROXY"] = 'http://9gfWr9:g0LSUy@131.108.17.194:9799/'
    os.environ["FTP_PROXY"] = 'http://9gfWr9:g0LSUy@131.108.17.194:9799/'
    os.environ["http_proxy"] = 'http://9gfWr9:g0LSUy@131.108.17.194:9799/'
    os.environ["https_proxy"] = 'http://9gfWr9:g0LSUy@131.108.17.194:9799/'
    os.environ["frp_proxy"] = 'http://9gfWr9:g0LSUy@131.108.17.194:9799/'
