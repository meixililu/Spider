from ghost import Ghost

agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.103 Safari/537.36'
ghost = Ghost()
with ghost.start() as session:
    page, extra_resources = session.open("http://fanyi.baidu.com/?aldtype=16047#en/zh/hello")
    assert page.http_status == 200
    print  page.content