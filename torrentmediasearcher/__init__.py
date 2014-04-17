__author__ = "Christiaan Maks (christiaanmaks@mylittlesky.net)"
__version__ = "1.0"
__copyright__ = "Copyright (c) 2014 Christiaan Maks"
__license__ = "GPLv2"

__all__ = ['TorrentMediaSearcher']

from .providers.eztv_api import EZTVAPI
from .providers.torrentproject_api import TorrentProjectAPI
from .providers.yify_api import YIFYAPI


class TorrentMediaSearcher():

    _PROVIDERS = {
        'eztv' : EZTVAPI,
        'torrentproject' : TorrentProjectAPI,
        'yify' : YIFYAPI,
        }

    @staticmethod
    def _print_results(results):
        for n in results:
            print(repr(n), ':', results[n])

    @staticmethod
    def request_movie_magnet(provider, movie, year=None, quality=None, callback=None):
        if provider in TorrentMediaSearcher._PROVIDERS:
            provider_class = TorrentMediaSearcher._PROVIDERS[provider]
        else:
            raise ValueError('No valid search provider selected, choose from: ' + str(TorrentMediaSearcher._PROVIDERS.keys()))

        if year is not None and 1000 > year > 9999:
            raise ValueError('Invalid year input, please use the yyyy format or do not use the year parameter (results will be less accurate)')

        if callback is None:
            print('No callback function specified, only printing results')
            callback = TorrentMediaSearcher._print_results

        search = provider_class(callback=callback)
        search.create_movie_request(movie=movie, year=year, quality=quality)

    @staticmethod
    def request_tv_magnet(provider, show, season, episode, quality=None, callback=None):
        if provider in TorrentMediaSearcher._PROVIDERS:
            provider_class = TorrentMediaSearcher._PROVIDERS[provider]
        else:
            raise ValueError('No valid search provider selected, choose from: ' + str(TorrentMediaSearcher._PROVIDERS.keys()))

        if callback is None:
            print('No callback function specified, only printing results')
            callback = TorrentMediaSearcher._print_results

        search = provider_class(callback=callback)
        search.create_tvshow_request(show=show, season=season, episode=episode, quality=quality)

