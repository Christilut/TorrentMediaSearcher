import threading


class BaseAPI(threading.Thread):

    _URL = None

    _NORMAL_SPECIFIER = 'HDTV'
    _HD_SPECIFIER = '720p'
    _FULLHD_SPECIFIER = '1080p'

    _SPECIFIERS = [
            r"S(\d+)E(\d+)",        # Matches SXXEYY (eg. S01E10)
            r"(\d+)x(\d+)",         # Matches SSxYY (eg. 01x10)
        ]

    def __init__(self, callback, show, season, episode):
        threading.Thread.__init__(self)

        self.callback = callback

        self.show = show
        self.season = season
        self.episode = episode

        if self._URL is None:
            raise ValueError('URL has not been set')

    def run(self):
        self.tv_show(show=self.show, season=self.season, episode=self.episode)

    def tv_show(self, show, season, episode):
        results = None

        try:
            results = self._query_tv_show(show=show, season=season, episode=episode)
        except EpisodeNotFound:
            print 'No results found, maybe the episode does not exist?'
        except SeasonNotFound:
            raise NotImplementedError
        except ShowNotFound:
            print 'No results for show', self.show, 'were found'

        self.callback(results)

    def movie(self, *args):
        raise NotImplementedError('This method must be implemented')

    def _query_tv_show(self, show, season, episode):
        raise NotImplementedError('This method must be implemented')

    def _query_movie(self, *args):
        raise NotImplementedError('This method must be implemented')



"""
    Exceptions
"""

class ProviderException(Exception):

    def __init__(self, message=None, errors=None):

        Exception.__init__(self, message)
        self.errors = errors

class ShowNotFound(ProviderException):
    """
        Raised when the specified show is not found
    """

class SeasonNotFound(ProviderException):
    """
        Raised when the specified season is not found
    """

class EpisodeNotFound(ProviderException):
    """
        Raised when the specified episode is not found
    """

class QualityNotFound(ProviderException):
    """
        Raised when the specified quality is not found
    """