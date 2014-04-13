from providers.eztv_api import EZTVAPI
from providers.torrentproject_api import TorrentProjectAPI


class TorrentMediaSearcher():
                        # TODO search for complete season and if they have more seeds, prioritize them
                        # TODO check for PROPER / REPACK releases on eztv
                        # TODO add seeders so users can make an informed decision which torrent to use
                        # TODO add more providers, YFIY, others

    _PROVIDERS = {
        'eztv' : EZTVAPI,
        'torrentproject' : TorrentProjectAPI,
        }

    @staticmethod
    def _print_results(results):
        for n in results:
            print repr(n), ':', results[n]

    @staticmethod
    def request_movie_magnets(provider, movie, year=None, callback=None):
        if provider in TorrentMediaSearcher._PROVIDERS:
            provider_class = TorrentMediaSearcher._PROVIDERS[provider]
        else:
            raise ValueError('No valid search provider selected, choose from: ' + str(TorrentMediaSearcher._PROVIDERS.keys()))

        if year is not None and 1000 > year > 9999:
            raise ValueError('Invalid year input, please use the yyyy format or do not use the year parameter (results will be less accurate)')

        if callback is None:
            print 'No callback function specified, only printing results'
            callback = TorrentMediaSearcher._print_results

        search = provider_class(callback=callback)
        search.create_movie_request(movie=movie, year=year)

    @staticmethod
    def request_tv_magnets(provider, show, season, episode, callback=None):
        if provider in TorrentMediaSearcher._PROVIDERS:
            provider_class = TorrentMediaSearcher._PROVIDERS[provider]
        else:
            raise ValueError('No valid search provider selected, choose from: ' + str(TorrentMediaSearcher._PROVIDERS.keys()))

        if callback is None:
            print 'No callback function specified, only printing results'
            callback = TorrentMediaSearcher._print_results

        search = provider_class(callback=callback)
        search.create_tvshow_request(show=show, season=season, episode=episode)

