# -*- encoding=utf-8 -*-
from flask import Flask
from flask import request, jsonify, send_from_directory

app = Flask(__name__)

APPSTORE = [
    {
        "id": 1,
        "name": u"百度",
        "type": "web",
        "package": "",
        "version": "v1.0.0",
        "icon": [{"size": "48x48", "link": "/1-48x48.png"},
                 {"size": "128x128", "link": "/1-128x128.png"}],
        "url": "http://www.baidu.com",
        "scheme": ""
    },
    {
        "id": 2,
        "name": u"微信",
        "type": "android",
        "package": "com.tencent.mm",
        "version": "v1.0.0",
        "icon": [{"size": "48x48", "link": "/2-48x48.png"},
                 {"size": "128x128", "link": "/2-128x128.png"}],
        "url": "",
        "scheme": "x-venus-a-2"
    },
    {
        "id": 3,
        "name": u"微信",
        "type": "ios",
        "package": "com.tencent.mm",
        "version": "v1.0.0",
        "icon": [{"size": "48x48", "link": "/2-48x48.png"},
                 {"size": "128x128", "link": "/2-128x128.png"}],
        "url": "",
        "scheme": "x-venus-i-3"
    },
    {
        "id": 4,
        "name": u"必应",
        "type": "web",
        "package": "",
        "version": "v1.0.0",
        "icon": [{"size": "48x48", "link": "/4-48x48.png"},
                 {"size": "128x128", "link": "/4-128x128.png"}],
        "url": "https://cn.bing.com",
        "scheme": ""
    },
]


@app.route("/")
def index():
    return "Hello, world!"


@app.route("/images/<path:image>")
def images(image):
    return send_from_directory("images", image)

@app.route("/apps/<string:platform>", methods=["GET"])
def list(platform):
    if platform not in ("ios", "android"):
        return jsonify({"message": "invalid platform(should be 'ios' or 'android')"}), 400
    images_root = request.url_root + "images"
    apps = []
    for a in APPSTORE:
        if a["type"] in ("web", platform):
            supported = dict(a)
            supported["icon"] = [dict(size=each["size"], link=images_root + each["link"])
                                 for each in supported["icon"]]
            apps.append(supported)

    page = request.args.get("page", default=0, type=int)
    size = request.args.get("size", default=20, type=int)
    if page < 0 or size <= 0:
        return jsonify({"message": "invalid page(should >= 0) or size(should > 0)"}), 400

    total_pages = 3
    paginate = {
        "page": page,
        "size": size,
        "first": page == 0,
        "last": page == total_pages - 1
    }

    start_idx = page * size
    content = []
    i = start_idx % len(apps)
    for c in range(0, size):
        t = dict(apps[i])
        t["id"] = start_idx + c
        content.append(t)
        i = (i + 1) % len(apps)
    paginate["content"] = content

    return jsonify(paginate)


if __name__ == '__main__':
    app.run()