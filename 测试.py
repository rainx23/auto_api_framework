import requests

url = 'http://api.lemonban.com/futureloan/member/register'
data = {
    'mobile_phone': 15233861777,
    'pwd': '12345678',
    'type': 0,
    'reg_name': 'zlf7'
}
print(type(data))
headers = {
    'X-Lemonban-Media-Type': 'lemonban.v1'
}
response = requests.post(url=url, json=data, headers=headers)
print(response.url)
print(response.json())


def send_http_request(url, method='get', **kwargs):
    """
    发送http请求
    :param url: 接口url
    :param method: http请求方法
    :param kwargs: 接受requests原生请求的关键字参数
    :return: 响应对象
    """
    # 把方法名统一小写化     requests.get()
    method = method.lower()
    print(getattr(requests, method)(url, **kwargs))
    return getattr(requests, method)(url, **kwargs)


if __name__ == '__main__':
    print(send_http_request(url, 'post', data=data, headers=headers))
