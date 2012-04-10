A quick and dirty implementation of pmap for Python


## Usage

Wherever you use map, you can use pmap:

    from pmap.threaded import pmap
    
    urls = ["http://www.google.com/",
            "http://www.facebook.com",
            "http://www.twitter.com/"]

    result = pmap(lambda url: urllib.urlopen(url).read(), urls)

