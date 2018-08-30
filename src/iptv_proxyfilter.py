import os
import requests
from flask import Flask, Response
from werkzeug.contrib.cache import SimpleCache
from parse_channels import parse_channels

app = Flask(__name__)
app.debug = os.getenv('DEBUG', True)
cache = SimpleCache()


@app.route('/')
def index():
    url = os.getenv('IPTV_PROXYFILTER_URL', None)
    if url is None:
        return 'Error: Please set IPTV_PROXYFILTER_URL env variable.'

    raw_data = cache.get('raw_data')
    if raw_data is None:
        raw_data = requests.get(url).text
        cache.set('raw_data', raw_data, timeout=5*60)

    channels = parse_channels(raw_data)

    # name filter
    name_filter = os.getenv('IPTV_PROXYFILTER_NAME', None)
    if name_filter is not None:
        channels = [x for x in channels if name_filter in x.tvg_name]

    # id notnull filter
    id_notnull_filter = os.getenv('IPTV_PROXYFILTER_ID_NOTNULL', False)
    if id_notnull_filter:
        channels = [x for x in channels if len(x.tvg_id) > 0]

    # uniq id filter
    id_uniq_filter = os.getenv('IPTV_PROXYFILTER_ID_UNIQ', False)
    if id_notnull_filter and id_uniq_filter:
        uniq_channels = dict()
        for channel in channels:
            if channel.tvg_id not in uniq_channels:
                uniq_channels[channel.tvg_id] = channel
            elif channel > uniq_channels[channel.tvg_id]:
                uniq_channels[channel.tvg_id] = channel
        channels = uniq_channels.values()

    response = '#EXTM3U\n'
    for channel in channels:
        response += str(channel)
    return Response(response, mimetype='text/plain')


if __name__ == '__main__':
    app.run()
