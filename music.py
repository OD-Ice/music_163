import execjs
import requests
from pprint import pprint
import prettytable as pt

class Music:
    def __init__(self):
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36 Maxthon/5.2.5.4000'
        }

    def get_enc(self, id=None, keyword=None):
        song_id = f'[{id}]'
        with open('encSecKey.js', 'r', encoding='utf-8') as f:
            js_data = f.read()
            if id:
                d = {"ids": song_id, "level": "standard", "encodeType": "aac", "csrf_token": ""}
            else:
                d = {"hlpretag": "<span class=\"s-fc7\">", "hlposttag": "</span>", "s": keyword, "type": "1", "offset": "0", "total": "true", "limit": "30", "csrf_token": ""}
            e = "010001"
            f = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
            g = "0CoJUm6Qyw8W8jud"
            data = execjs.compile(js_data).call('start', d, e, f, g)
            return data

    def get_id(self, name):
        url = 'https://music.163.com/weapi/cloudsearch/get/web?csrf_token='
        result = self.get_enc(keyword=name)
        data = {
            'params': result['encText'],
            'encSecKey': result['encSecKey']
        }
        res = requests.post(url, headers=self.headers, data=data).json()
        # pprint(res)
        tb = pt.PrettyTable()
        tb.field_names = ['序号', '歌名', '歌曲id', '歌手']
        song_list = res['result']['songs']
        n = 0
        song_dict = {}
        for each in song_list:
            n += 1
            song_num = n
            song_name = each['name']
            song_id = each['id']
            singer = each['ar'][0]['name']
            each_list = [song_num, song_name, song_id, singer]
            tb.add_row(each_list)
            song_dict[song_num] = [song_name, song_id]
        print(tb)
        return song_dict

    def main(self):
        name = input('请输入歌名：')
        song_dict = self.get_id(name)
        url = 'https://music.163.com/weapi/song/enhance/player/url/v1?csrf_token='
        num = input('请输入歌曲序号：')
        song_name = song_dict[int(num)][0]
        song_id = song_dict[int(num)][1]
        result = self.get_enc(id=song_id)
        # print(result)
        data = {
            'params': result['encText'],
            'encSecKey': result['encSecKey']
        }
        res = requests.post(url, headers=self.headers, data=data).json()
        # print('内容：', res)
        song_url = res['data'][0]['url']

        song = requests.get(song_url, headers=self.headers)
        with open(f'music/{song_name}.m4a', 'wb') as f:
            f.write(song.content)

if __name__ == '__main__':
    music = Music()
    music.main()
