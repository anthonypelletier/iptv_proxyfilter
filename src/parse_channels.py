from lxml import html


class Channel:
    def __init__(self, stream_url, tvg_id, tvg_name, tvg_logo, group_title):
        self.stream_url = stream_url
        self.tvg_id = tvg_id
        self.tvg_name = tvg_name
        self.tvg_logo = tvg_logo
        self.group_title = group_title

    def get_quality_weight(self):
        weights = {
            3: 'H265',
            2: 'FULL HD',
            1: 'HD',
        }
        for weight in weights:
            if weights[weight] in self.tvg_name:
                return weight
        return 0

    def __gt__(self, other_channel):
        return self.get_quality_weight() > other_channel.get_quality_weight()

    def __lt__(self, other_channel):
        return self.get_quality_weight() < other_channel.get_quality_weight()

    def __str__(self):
        return '#EXTINF:-1 ' + \
            'tvg-id="' + self.tvg_id + '" ' + \
            'tvg-name="' + self.tvg_name + '" ' + \
            'tvg-logo="' + self.tvg_logo + '" ' + \
            'group-title="' + self.group_title + '"' + \
            ',' + self.tvg_name + '\n' + self.stream_url + '\n'


def parse_channels(data):
    channels = list()
    attributes = None
    for line in data.splitlines():
        line = line.strip()  # delete the line break
        if line.startswith('http') and attributes:
            stream_url = line
            channels.append(Channel(
                stream_url=stream_url,
                tvg_id=attributes.get('tvg-id', ''),
                tvg_name=attributes.get('tvg-name', ''),
                tvg_logo=attributes.get('tvg-logo', ''),
                group_title=attributes.get('group-title', ''),
            ))
        elif line.startswith('#EXTINF:-1'):
            line = line.split('#EXTINF:-1')[1].split(',')[0]
            attributes = html.fromstring(
                '<p ' + line + '></p>').attrib  # very tricky hack to allow using lxml to extract attributes :D
    return channels
