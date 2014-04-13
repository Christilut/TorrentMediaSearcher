from torrentmediasearcher import TorrentMediaSearcher
from providers.base_api import MovieNotFound, EpisodeNotFound, ShowNotFound, QualityNotFound

def on_finished(results):
    for n in results:
        print repr(n), ':', results[n]

    print ''
    if results.has_key('720p'):
        print '720p has', results['720p']['seeds'], 'seeds and the following magnet link:', results['720p']['magnet']


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
        TorrentMediaSearcher().request_movie_magnets('torrentproject', 'iron man', 2008, callback=on_finished)
    except MovieNotFound as e:
        print e


import threading
threading.Thread(target=test_tv).start()    # Create the request in a thread, so it does not block the main thread

print 'Waiting for results...'