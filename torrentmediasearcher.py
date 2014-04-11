from providers.eztv_api import EZTVAPI
from providers.torrentproject_api import TorrentProjectAPI


class TorrentMediaSearcher():
                        # TODO search for complete season and if they have more seeds, prioritize them
                        # TODO check for PROPER releases (and other keywords)

    _PROVIDERS = {
        'eztv' : EZTVAPI,
        'torrentproject' : TorrentProjectAPI,
        }

    @staticmethod
    def _print_results(results):
        print results

    @staticmethod
    def request_movie_magnets(provider, movie, callback=None):
        provider_class = None

        if provider in TorrentMediaSearcher._PROVIDERS:
            provider_class = TorrentMediaSearcher._PROVIDERS[provider]
        else:
            raise ValueError('No valid search provider selected, choose from: ' + str(TorrentMediaSearcher._PROVIDERS.keys()))

        if callback is None:
            print 'No callback function specified, only printing results'
            callback = TorrentMediaSearcher._print_results

        search = provider_class(callback=callback)
        search.set_movie(movie=movie)

    @staticmethod
    def request_tv_magnets(provider, show, season, episode, callback=None):
        provider_class = None

        if provider in TorrentMediaSearcher._PROVIDERS:
            provider_class = TorrentMediaSearcher._PROVIDERS[provider]
        else:
            raise ValueError('No valid search provider selected, choose from: ' + str(TorrentMediaSearcher._PROVIDERS.keys()))

        if callback is None:
            print 'No callback function specified, only printing results'
            callback = TorrentMediaSearcher._print_results

        search = provider_class(callback=callback)
        search.set_tv(show=show, season=season, episode=episode)

