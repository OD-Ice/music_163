## music_163
## 网易云音乐异步爬虫

+ 使用**asyncio、aiohttp、aiofiles**实现协程异步音乐下载

+ 可以搜索网易云音乐上面的歌曲并生产列表  
  ![Image1](https://github.com/OD-Ice/music_163/blob/master/img/music.PNG)

  ![Image2](https://github.com/OD-Ice/music_163/blob/master/img/music-2.PNG)

+ 从列表中选择歌曲序号可进行下载
+ 版权受限不能听的音乐不支持下载

## 更新日志

### 2020.6.13

+ 增加批量下载功能
+ 支持异步下载
+ 增加翻页功能
+ 支持连续下载
+ 重新设定文件命名方式，避免同名歌曲覆盖(歌名+歌曲编号)

### 2020.10.9

+ 由于网页端一次只能显示20首歌曲，本项目翻页功能失效....

