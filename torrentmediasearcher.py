from providers.eztv_api import EZTVAPI
from providers.torrentproject_api import TorrentProjectAPI


class TorrentMediaSearcher():
                        # TODO search for complete season and if they have more seeds, prioritize them
                        # TODO check for PROPER releases (and other keywords)

    _PROVIDERS = {
        'eztv' : EZTVAPI,
        'torrentproject' : TorrentProjectAPI,
        }

    def __init__(self):
        pass

    def _print_results(self, results):
        print results

    def request_movie_magnets(self, callback, provider, movie, quality):
        pass

    def request_tv_magnets(self, provider, show, season, episode, callback=None):
        provider_class = None

        if provider in self._PROVIDERS:
            provider_class = self._PROVIDERS[provider]
        else:
            raise ValueError('No valid search provider selected, choose from: ' + str(self._PROVIDERS.keys()))

        if callback is None:
            print 'No callback function specified, only printing results'
            callback = self._print_results

        provider_class(callback=callback, show=show, season=season, episode=episode).start()

