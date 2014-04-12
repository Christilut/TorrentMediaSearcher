from torrentmediasearcher import TorrentMediaSearcher
from providers.base_api import MovieNotFound, EpisodeNotFound, ShowNotFound, QualityNotFound

def on_finished(results):
    for n in results:
        print repr(n), ':', results[n]


def test_tv():
    try:
        TorrentMediaSearcher().request_tv_magnets('eztv', 'big bang theory', 1, 10, callback=on_finished)
    except EpisodeNotFound as e:
        print e
    except ShowNotFound as e:
        print e
    except QualityNotFound as e:
        print e


def test_movie():
    try:
        TorrentMediaSearcher().request_movie_magnets('torrentpsefroject', 'iron man', callback=on_finished)
    except MovieNotFound as e:
        print e


import threading
threading.Thread(target=test_tv).start()

print 'Waiting for results...'