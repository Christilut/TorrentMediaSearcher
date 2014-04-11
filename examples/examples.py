from torrentmediasearcher import TorrentMediaSearcher

def on_finished(results):
    for n in results:
        print repr(n), ':', results[n]


def test_tv():
    TorrentMediaSearcher().request_tv_magnets('torrentproject', 'big bang theory', 1, 10, callback=on_finished)

    print 'Waiting for results...'


def test_movie():
    TorrentMediaSearcher().request_movie_magnets('torrentproject', 'iron man 3', callback=on_finished)

    print 'Waiting for results...'


test_movie()

# test_tv()
