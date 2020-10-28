import os
import json
import urllib.parse
import argparse
from mitmproxy import proxy, options
from mitmproxy.tools.dump import DumpMaster
from mitmproxy import http


class GetQuest:
    def __init__(self, f_value):
        self.f_value = f_value
        self.quest = {"fp": []}

    def response(self, flow: http.HTTPFlow) -> None:
        if flow.request.path.startswith("/getquest.ashx"):
            data = json.loads(flow.response.content)
            fp = data.get('fp')
            for f in fp:
                if f.get('f') == self.f_value:
                    if f not in self.quest['fp']:
                        self.quest['fp'].append(f)


def start(name, f_value, icon):
    addon = GetQuest(f_value)
    opts = options.Options()
    pconf = proxy.config.ProxyConfig(opts)
    m = DumpMaster(opts)
    m.server = proxy.server.ProxyServer(pconf)
    m.addons.add(addon)

    try:
        m.run()
    except KeyboardInterrupt:
        m.shutdown()

        gpx_name = f'<name>{name}</name><desc>{icon}</desc>'
        gpx_rtept = ''
        for q in addon.quest['fp']:
            gpx_rtept += f'''<rtept lat="{q['c']}" lon="{q['d']}"/>'''
        gpx_rte = f'<rte>{gpx_name}{gpx_rtept}</rte>'
        gpx = f'<?xml version="1.0" encoding="UTF-8"?><gpx version="1.1" creator="GPS JoyStick - gpsjoystick@gmail.com - https://www.facebook.com/gpsjoystick">{gpx_rte}</gpx>'

        with open(f'{name}.gpx', 'w') as _file:
            _file.write(gpx)


def main():
    # parser = argparse.ArgumentParser(description="獲取迷你龍任務座標")

    start("迷你龍任務座標", "7^147^^^Y^^^N", "https://twpkinfo.com/images/poke1/147.png")


if __name__ == '__main__':
    main()
