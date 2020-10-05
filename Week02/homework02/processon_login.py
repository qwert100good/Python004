# 使用 requests 或 Selenium 模拟登录石墨文档 https://shimo.im
# 登录 ProcessOn 石墨文档验证码未解决

import requests
from fake_useragent import UserAgent

s = requests.session()


class LoginFailed(Exception):
    def __init__(self, ErrorInfo):
        super().__init__(self, ErrorInfo)
        self.error_info = ErrorInfo

    def __str__(self):
        return self.error_info


def login(session):
    login_url = 'https://processon.com/login'

    ua = UserAgent(verify_ssl=False)

    headers = {
        'User-Agent': ua.chrome,
        'Referer': 'https://processon.com/login?f=index',
        'Host': 'processon.com'
    }

    email = 'xxxxxxxx@qq.com'
    password = 'xxxxxxxx'

    form_data = {
        'login_email': email,
        'login_password': password
    }
    try:
        resp = session.post(login_url, headers=headers, data=form_data)
    except Exception:
        print('网络异常')
    else:
        if '<title>ProcessOn - 我的文件</title>' not in resp.text:
            raise LoginFailed('用户名密码不正确')


# 登录
def main():
    try:
        login(s)
    except LoginFailed as e:
        print(e)
    else:
        print('登录成功')
    finally:
        s.close()


if __name__ == '__main__':
    main()
