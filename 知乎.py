# https://www.zhihu.com/api/v4/search_v3?t=general&q=%E9%9D%A2%E8%AF%95&correction=1&offset=20&limit=20&lc_idx=27&show_all_topics=0&search_hash_id=7553dedda18c70cefbc31c687b59cd0a&vertical_info=1%2C1%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C1

# https://www.zhihu.com/api/v4/search_v3?t=general&q=%E9%9D%A2%E8%AF%95&correction=1&offset=40&limit=20&lc_idx=47&show_all_topics=0&search_hash_id=008a3b0180dc359682ea68048fd9f64c&vertical_info=1%2C1%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C1

# https://www.zhihu.com/api/v4/search_v3?t=general&q=%E9%9D%A2%E8%AF%95&correction=1&offset=60&limit=20&lc_idx=67&show_all_topics=0&search_hash_id=008a3b0180dc359682ea68048fd9f64c&vertical_info=1%2C1%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C1

# https://www.zhihu.com/api/v4/search_v3?t=general&q=%E9%9D%A2%E8%AF%95&correction=1&offset=80&limit=20&lc_idx=87&show_all_topics=0&search_hash_id=7553dedda18c70cefbc31c687b59cd0a&vertical_info=1%2C1%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C1
import requests
import json
import pymongo
from lxml import etree


def parse_html(url, kw, offset):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
        'cookie': '_zap=2fec85f3-573a-4a85-b689-7063e7a423c7; d_c0="ABAgeCOIchCPTvqzGLApZzHVEk1sA4d4ZNo=|1575344005"; _xsrf=c3R2uPfmXB69DrT45WEzIQFngDzLyLRA; capsion_ticket="2|1:0|10:1577450537|14:capsion_ticket|44:MTM4YWMxY2ExMTY3NDU4MzkxYzY4M2E5OGVmNjcwZDY=|371d8b1d933f08c2df90c116e3f89d4b148f0f76a9225af0790120d7e3a4b2d4"; z_c0="2|1:0|10:1577450603|4:z_c0|92:Mi4xcVhkUkJ3QUFBQUFBRUNCNEk0aHlFQ2NBQUFDRUFsVk5hb2t0WGdBUEtBSkUzcENrcHZ4NGY2T2V0Q0R1UWpBaVJn|76b38415af8ab6a0dd36ea59c3e238b312df633b03fe5d63f235bc9d64fca3fa"; tst=r; q_c1=958d43502fc74fd1943cdfcdef49c2f8|1577450717000|1577450717000; KLBRSID=b33d76655747159914ef8c32323d16fd|1577512596|1577512415; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1577497919,1577498043,1577503265,1577512858; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1577513387; tgw_l7_route=73af20938a97f63d9b695ad561c4c10c',
        'referer': 'https://www.zhihu.com/'}
    response = requests.get(url=url, headers=headers).content.decode('utf-8')
    # print(detail_response)
    response = json.loads(response)
    data_list = response['data']
    if data_list == []:
        flag = False
        return flag
    else:
        flag = True

    for data in data_list:
        if data.get('object').get('question'):
            # 搜索词
            kw = kw
            print(kw)
            # 搜索结果排序号
            rank = offset - 20 + data.get('index') + 1
            print(rank)
            # 问题链接
            url = data.get('object').get('url').replace('api', 'www').rsplit('/', 2)   # ['https://www.zhihu.com', 'answers', '424927405']
            q_type = data.get('object').get('question').get('type')
            q_id = data.get('object').get('question').get('id')
            print(q_type, q_id)
            full_url = url[0] + '/' + q_type + '/' + q_id + '/' + url[1].replace('answers', 'answer') + '/' + url[2]
            print(full_url)
            # 问题名
            q_name = data.get('object').get('question').get('name').replace('<em>', '').replace('</em>', '')
            print(q_name)
            # 回答排名第一的账号名称
            if rank == 1:
                a_name = data.get('object').get('author').get('name')
                # 回答排名第一的账号 ID
                a_id = data.get('object').get('author').get('id')
            else:
                url = f'https://www.zhihu.com/api/v4/search_v3?t=general&q={kw}&correction=1&offset=20&limit=20&lc_idx=27&show_all_topics=0&search_hash_id=7553dedda18c70cefbc31c687b59cd0a&vertical_info=1%2C1%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C1'
                response = json.loads(requests.get(url=url, headers=headers).content.decode('utf-8'))
                a_name = response['data'][0].get('object').get('author').get('name')
                a_id = response['data'][0].get('object').get('author').get('id')
            print(a_name, a_id)

            # 详情页
            session = requests.session()
            detail_response = session.get(url=full_url, headers=headers).content.decode('utf-8')
            tree = etree.HTML(detail_response)
            # 关注者数量
            noticer_num = tree.xpath('//div[@class="NumberBoard QuestionFollowStatus-counts NumberBoard--divider"]/button//strong/text()')[0]
            print(noticer_num)
            # 被浏览数量
            looked_num = tree.xpath('//div[@class="NumberBoard QuestionFollowStatus-counts NumberBoard--divider"]/div//strong/text()')[0]
            print(looked_num)
            # 4.插入
            collection.insert_one({'search_terms': kw, 'search_rank': rank, 'question_url': full_url,
                                   'question_title': q_name, 'question_follow_num': noticer_num, 'question_view_num': looked_num,
                                   'question_top_answer_username': a_name, 'question_top_answer_id': a_id})
    return flag


if __name__ == '__main__':
    # 1.连接客户端
    client = pymongo.MongoClient('127.0.0.1', 27017)
    # 2.创建数据库
    db = client['zhihu']
    # 3.创建集合
    collection = db['questions']

    kw_list = ['面试', '实习', '找工作', '简历']
    for kw in kw_list:
        offset = 0
        while True:
            offset += 20
            url = f'https://www.zhihu.com/api/v4/search_v3?t=general&q={kw}&correction=1&offset={offset}&limit=20&lc_idx={offset+7}&show_all_topics=0&search_hash_id=7553dedda18c70cefbc31c687b59cd0a&vertical_info=1%2C1%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C1'
            flag = parse_html(url, kw, offset)
            if flag == False:
                print('============================================')
                break

