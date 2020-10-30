import os
import json
import urllib.parse
import argparse
from mitmproxy import proxy, options
from mitmproxy.tools.dump import DumpMaster
from mitmproxy import http

QUEST = 0
POKE = 1


def E(g, i): return pow(g, 1/i)-1
def bQ(i, g): return i[-4:]


class GetQuest:
    def __init__(self, f_value):
        self.f_value = f_value
        self.coord = {"fp": []}

    def response(self, flow: http.HTTPFlow) -> None:
        if flow.request.path.startswith("/getquest.ashx"):
            data = json.loads(flow.response.content)
            fp = data.get('fp')
            for f in fp:
                if f.get('f') == self.f_value:
                    if f not in self.coord['fp']:
                        self.coord['fp'].append(f)


class GetPoke:
    def __init__(self, f_value):
        self.f_value = f_value
        self.coord = {"fp": []}

    def response(self, flow: http.HTTPFlow) -> None:
        if flow.request.path.startswith("/fp1.ashx"):
            data = json.loads(flow.response.content)
            fp = data.get('fp')
            for f in fp:
                found = False
                if f.get('f') != "^^^^^^":
                    bc = f.get('f').split("^")
                    try:
                        if type(self.f_value) == int:
                            if float(bc[5]) >= self.f_value:
                                found = True
                        else:
                            if int(bc[0]) >= self.f_value[0] and \
                                int(bc[1]) >= self.f_value[1] and \
                                    int(bc[2]) >= self.f_value[2]:
                                found = True
                    except Exception as e:
                        print(e)
                    if found and f not in self.coord['fp']:
                        self.coord['fp'].append(f)


def start(name, f_value, _type, icon):
    if _type == QUEST:
        addon = GetQuest(f_value)
    else:
        addon = GetPoke(f_value)
    opts = options.Options()
    pconf = proxy.config.ProxyConfig(opts)
    m = DumpMaster(opts)
    m.server = proxy.server.ProxyServer(pconf)
    m.addons.add(addon)

    try:
        m.run()
    except KeyboardInterrupt:
        m.shutdown()

        count = len(addon.coord['fp'])
        if count == 0:
            print("[warn] 似乎沒有找到座標...")
        else:
            print(f"[info] 找到{count}個座標.")
            gpx_name = f'<name>{name}</name><desc>{icon}</desc>'
            gpx_rtept = ''
            for q in addon.coord['fp']:
                if _type == QUEST:
                    gpx_rtept += f'''<rtept lat="{q['c']}" lon="{q['d']}"/>'''
                else:
                    c = float(q["c"]) + E(3, 3) + E(int(bQ(q["b"], 4)[0:1]), 5)
                    d = float(q["d"]) + E(4, 4) - E(int(bQ(q["b"], 4)[0:1]), 6)
                    gpx_rtept += f'''<rtept lat="{c}" lon="{d}"/>'''

            gpx_rte = f'<rte>{gpx_name}{gpx_rtept}</rte>'
            gpx = f'<?xml version="1.0" encoding="UTF-8"?><gpx version="1.1" creator="GPS JoyStick - gpsjoystick@gmail.com - https://www.facebook.com/gpsjoystick">{gpx_rte}</gpx>'

            with open(f'{name}.gpx', 'w') as _file:
                _file.write(gpx)


def main():
    # parser = argparse.ArgumentParser(description="獲取迷你龍任務座標")

    start("迷你龍任務座標", "7^147^^^Y^^^N", QUEST, "https://twpkinfo.com/images/poke1/147.png")
    # start("攻-防-體-寶可夢座標", [10, 10, 10], POKE,
    #       "https://twpkinfo.com/images/ipoke.png")
    # start("攻-防-體-寶可夢座標", 90, POKE,
    #       "https://twpkinfo.com/images/ipoke.png")


if __name__ == '__main__':
    main()
