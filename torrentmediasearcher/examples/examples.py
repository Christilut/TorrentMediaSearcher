from torrentmediasearcher import TorrentMediaSearcher
from torrentmediasearcher.providers.base_api import MovieNotFound, EpisodeNotFound, ShowNotFound, QualityNotFound


def on_finished(results):
    for n in results:
        print repr(n), ':', results[n]


def test_tv():
    try:
        TorrentMediaSearcher().request_tv_magnet(provider='eztv', show='big bang theory', season=1, episode=10, quality='normal', callback=on_finished)
    except EpisodeNotFound as e:
        print e
    except ShowNotFound as e:
        print e
    except QualityNotFound as e:
        print e


def test_movie():
    try:
        TorrentMediaSearcher().request_movie_magnet(provider='yify', movie='iron man', year=2008, quality='1080p', callback=on_finished)
    except MovieNotFound as e:
        print e
    except QualityNotFound as e:
        print e


import threading
threading.Thread(target=test_movie).start()    # Create the request in a thread, so it does not block the main thread

print 'Waiting for results...'