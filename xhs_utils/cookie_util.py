def trans_cookies(cookies_str):
    if '; ' in cookies_str:
        ck = {i.split('=')[0]: '='.join(i.split('=')[1:]) for i in cookies_str.split('; ')}
    else:
        ck = {i.split('=')[0]: '='.join(i.split('=')[1:]) for i in cookies_str.split(';')}
    if 'a1' not in ck:
        raise ValueError("Cookie 格式不正确，请重新获取")
    return ck
