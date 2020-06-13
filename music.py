import execjs
import requests
# from pprint import pprint
import prettytable as pt
import asyncio
import aiohttp
import aiofiles

class Music:
    def __init__(self):
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36 Maxthon/5.2.5.4000'
        }

    async def get_enc(self, id=None, keyword=None, song_name=None, n=None):
        song_id = f'[{id}]'
        async with aiofiles.open('encSecKey.js', 'r', encoding='utf-8') as f:
            js_data = await f.read()
            if id:
                d = {"ids": song_id, "level": "standard", "encodeType": "aac", "csrf_token": ""}
            else:
                d = {"hlpretag": "<span class=\"s-fc7\">", "hlposttag": "</span>", "s": keyword, "type": "1", "offset": n, "total": "true", "limit": "30", "csrf_token": ""}
            e = "010001"
            f = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
            g = "0CoJUm6Qyw8W8jud"
            data = execjs.compile(js_data).call('start', d, e, f, g)
            if song_name:
                return data, song_name, id
            return data

    def get_id(self, name, n):
        url = 'https://music.163.com/weapi/cloudsearch/get/web?csrf_token='
        c = self.get_enc(keyword=name , n=n)
        task = asyncio.ensure_future(c)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(task)
        result = task.result()
        data = {
            'params': result['encText'],
            'encSecKey': result['encSecKey']
        }
        res = requests.post(url, headers=self.headers, data=data).json()
        # pprint(res)
        tb = pt.PrettyTable()
        # tb.align = 'c'
        # tb.padding_width = 1
        tb.field_names = ['序号', '歌名', '歌曲id', '歌手']
        song_list = res['result']['songs']
        n = 0
        song_dict = {}
        for each in song_list:
            n += 1
            song_num = n
            song_name = each['name']
            song_id = each['id']
            singers = each['ar']
            singer = []
            for i in range(len(singers)):
                singer.append(singers[i]['name'])
            singer = '/'.join(singer)
            each_list = [song_num, song_name, song_id, singer]
            tb.add_row(each_list)
            song_dict[song_num] = [song_name, song_id]
        print(tb)
        print('='*40)
        return song_dict

    async def download(self, url, data, song_name, song_id):
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with await session.post(url, data=data) as res:
                res = await res.json(content_type='text/plain')
                song_url = res['data'][0]['url']

                # 去除名字中的特殊字符
                for each in r'? " > < / \ | * :'.split():
                    if each in song_name:
                        song_name = song_name.replace(each, ' ')

                try:
                    async with session.get(song_url) as song:
                        async with aiofiles.open(f'music/{song_name}{song_id}.m4a', 'wb') as f:
                            # .read()是无编码的格式，区别于requests的content
                            # 注意！两个await
                            await f.write(await song.read())
                            print(song_name, '下载完成！')
                except:
                    print(song_name, '不支持下载！')

    def main(self):
        name = input('请输入歌名：')
        # offset 代表页数 一次增加30
        n = 0
        flag = True

        # 判断是否继续下载
        while flag:
            while True:
                song_dict = self.get_id(name, n)
                url = 'https://music.163.com/weapi/song/enhance/player/url/v1?csrf_token='
                num = input('请输入歌曲序号\n多首以空格分隔\n"-"表示区间\n"all"表示全部下载\n翻页请输入"p"(前翻)或"n"(后翻)：')
                if num not in ['n', 'N', 'p', 'P']:
                    break
                else:
                    if num in ['n', 'N']:
                        n += 30
                    else:
                        n -= 30

            tasks1 = []
            tasks2 = []
            num_str = ''
            if num in ['all', 'All', 'ALL']:
                print('全部下载！')
                for i in range(1, len(song_dict)+1):
                    num_str += f' {i}'
            else:
                nums = num.strip(' ').split()
                for each in nums:
                    if '-' in each:
                        num_ran = each.split('-')
                        for i in range(int(num_ran[0]), int(num_ran[1])+1):
                            num_str += f' {i}'
                    else:
                        num_str += f' {each}'
            print('下载歌曲编号：', num_str)
            print('='*40)
            for each in num_str.strip(' ').split():
                song_name = song_dict[int(each)][0]
                song_id = song_dict[int(each)][1]
                c = self.get_enc(id=song_id, song_name=song_name)
                task1 = asyncio.ensure_future(c)
                tasks1.append(task1)
                loop1 = asyncio.get_event_loop()
                loop1.run_until_complete(asyncio.wait(tasks1))

            for task in tasks1:
                result, song_name, song_id = task.result()
                data = {
                    'params': result['encText'],
                    'encSecKey': result['encSecKey']
                }
                d = self.download(url, data, song_name, song_id)
                task2 = asyncio.ensure_future(d)
                tasks2.append(task2)

            loop2 = asyncio.get_event_loop()
            loop2.run_until_complete(asyncio.wait(tasks2))

            print('='*40)
            des = input('是否继续下载？(Y/N)')
            print('=' * 40)
            if des in ['Y', 'y']:
                flag = True
            else:
                flag = False

if __name__ == '__main__':
    music = Music()
    while True:
        music.main()
        des = input('是否继续搜索？(Y/N)')
        if des in ['Y', 'y']:
            print('=' * 40)
        else:
            break
