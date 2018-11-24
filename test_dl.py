import urllib2

def dl():
    target_url = "http://www.youtube.com/get_video_info?video_id=ViFq1pE_cQM&el=embedded&ps=default&eurl=&gl=US&hl=en"
    resp = ""

    try:
        for line in urllib2.urlopen(target_url):
            resp = line
    except:
        print("woopsie")
        return

    parts = resp.split("&")

    the_map = {}

    for part in parts:
        do_a_split = part.split("=")
        the_map[do_a_split[0]] = do_a_split[1]

    streams = str(urllib2.unquote(the_map['url_encoded_fmt_stream_map']).decode('utf8')).split(",")

    final_streams = []

    for stream in streams:
        this_stream = {}
        stream_attrs = stream.split("&")

        for attr in stream_attrs:
            key,val = attr.split("=")
            this_stream[key] = str(urllib2.unquote(val).decode('utf8'))

        final_streams.append(this_stream)

    print final_streams

dl()