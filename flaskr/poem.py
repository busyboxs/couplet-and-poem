# -*- coding:utf-8 -*-
from urllib.request import urlopen, Request
import json
import random

# 错误代码
ERROR_DICT = {
    '2': '后端连接超时请重试',
    '52001': '请求超时请重试',
    '52002': '系统错误请重试',
    '52003': '未授权用户',
    '52004': '输入解析失败',
    '52005': '输入字段有误',
    '52006': '输入文本长度不超过5',
    '52007': '输入文本包含政治&黄色内容',
    '52008': '后台服务返回错误请重试',
    '54003': '访问频率受限',
    '54100': '查询接口参数为空',
    '54102': '无写诗结果请重试'
}


# 获取 token
def get_token_key():
    token_key = ''
    # client_id 为官网获取的AK， client_secret 为官网获取的SK
    client_id = '【百度云应用的AK】'
    client_secret = '【百度云应用的SK】'

    host = f'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials' \
        f'&client_id={client_id}&client_secret={client_secret}'

    request = Request(host)
    request.add_header('Content-Type', 'application/json; charset=UTF-8')
    response = urlopen(request)
    token_content = response.read()
    if token_content:
        token_info = json.loads(token_content)
        token_key = token_info['access_token']
    return token_key


# 调用百度 AI 智能春联和智能写诗接口
def nlp_result(text, token_key, index=0, way='poem'):
    """
    调用该函数返回生成的春联或者七言诗
    :param text: 春联或诗的主题（官方限制不超过 5 个字符）
    :param token_key: 通过调用 get_token_key() 获取的 token
    :param index: 不同的 index 会输出不同的春联和诗
    :param way: 通过传入该参数确认是生成对联还是生成诗，“poem”为写七言诗，“couplets”为写春联
    :return: 获取的数据
    """
    assert way in ['poem', 'couplets'], 'type should be poem or couplet'
    request_url = f'https://aip.baidubce.com/rpc/2.0/nlp/v1/{way}'

    params_d = dict()
    params_d['text'] = text
    params_d['index'] = index
    params = json.dumps(params_d).encode('utf-8')
    access_token = token_key
    request_url = request_url + "?access_token=" + access_token
    request = Request(url=request_url, data=params)
    request.add_header('Content-Type', 'application/json')
    response = urlopen(request)
    content = response.read()
    if content:
        data = json.loads(content)
        return data


# 调用百度 AI 智能春联接口（用于测试）
def get_couplets(text, token_key, index=0):
    """
    调用百度AI智能春联接口，并生成横批、上联和下联
    :param text: 智能春联的主题（官方限制不超过5个字）
    :param token_key: 通过调用 get_token_key() 获取的 token
    :param index: 不同的 index 会生成不同的春联
    :return: 调用智能春联生成的数据
    """
    request_url = 'https://aip.baidubce.com/rpc/2.0/nlp/v1/couplets'
    params_d = dict()
    params_d['text'] = text
    params_d['index'] = index
    params = json.dumps(params_d).encode('utf-8')
    access_token = token_key
    request_url = request_url + "?access_token=" + access_token
    request = Request(url=request_url, data=params)
    request.add_header('Content-Type', 'application/json')
    response = urlopen(request)
    content = response.read()
    if content:
        data = json.loads(content)
        return data


# 解析生成的春联
def parse_couplets(data):
    """
    解析调用智能春联生成的数据
    :param data: 调用智能春联生成的有效数据
    :return: 横批（center）、上联（first）和下联（second）
    """
    center = data['couplets']['center']
    first = data['couplets']['first']
    second = data['couplets']['second']
    # print(f'上联：{first}')
    # print(f'下联：{second}')
    # print(f'横批：{center}')
    return center, first, second


# 调用百度 AI 智能写诗接口（用于测试）
def get_poem(text, token_key, index=0):
    """
    调用百度AI智能写诗接口，并生成七言诗
    :param text: 智能写诗的主题（官方限制不超过5个字）
    :param token_key: 通过调用 get_token_key() 获取的 token
    :param index: 不同的 index 会生成不同的七言诗
    :return: 调用智能写诗生成的数据
    """
    request_url = 'https://aip.baidubce.com/rpc/2.0/nlp/v1/poem'
    params_d = dict()
    params_d['text'] = text
    params_d['index'] = index
    params = json.dumps(params_d).encode('utf-8')
    access_token = token_key
    request_url = request_url + "?access_token=" + access_token
    request = Request(url=request_url, data=params)
    request.add_header('Content-Type', 'application/json')
    response = urlopen(request)
    content = response.read()
    if content:
        data = json.loads(content)
        return data


# 解析生成的诗句
def parse_poem(data):
    """
    解析调用智能写诗生成的数据
    :param data: 调用智能写诗生成的有效数据
    :return: 诗的题目（title）和诗的内容（content）
    """
    title = data['poem'][0]['title']
    poem = data['poem'][0]['content'].replace('\t', '\n')
    # print(title)
    # print(poem)
    return title, poem


# 解析是否调用接口错误，如果有返回对应的提示，没有返回None
def parse_error(data):
    """
    解析是否调用接口错误
    :param data: 调用接口生成的数据
    :return: 如果出错，返回对应的错误信息，否则返回None
    """
    if 'error_code' in data:
        code = data['error_code']
        error = ERROR_DICT[str(code)]
        return error
    return None


# 带有错误处理的调用智能写诗接口（样例）
def test_get_poem():
    token_key = '通过调用 get_token_key() 获取的 token'
    index = random.randint(0, 10)
    data = get_poem('春节建行卡建好了', token_key, index)
    error = parse_error(data)
    if error:
        print(f'错误：{error}')
    else:
        title, content = parse_poem(data)
        print(title)
        print(content)
