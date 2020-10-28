## pokemongo任務座標

```py
pip3 install -r requirements.txt
python3 getquest.py
```

瀏覽器代理8080端口, 然後打開[https://twpkinfo.com/iquest.aspx](https://twpkinfo.com/iquest.aspx)

移動地圖讓你想領取的任務圖標顯示出來,找到合適多的圖標後,命令行窗口按`ctrl+c`取消進程,此時getquest.py 同級目錄會生成一個gpx文件,使用`adb push`命令或其他方式放入手機,手機的`gps joystick`程序導入gpx文件

## 視頻例子
[https://www.bilibili.com/video/BV1fK4y1f7zz/](https://www.bilibili.com/video/BV1fK4y1f7zz/)
[https://www.acfun.cn/v/ac19155558](https://www.acfun.cn/v/ac19155558)