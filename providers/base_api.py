import threading


class BaseAPI(threading.Thread):

    _URL = None

    _NORMAL_SPECIFIER = 'HDTV'
    _HD_SPECIFIER = '720p'
    _FULLHD_SPECIFIER = '1080p'

    _TV_SPECIFIERS = [
            r"S(\d+)E(\d+)",        # Regex for S??E??
            r"(\d+)x(\d+)",         # Regex for ??x??
        ]

    _wanted_movie = None
    _wanted_show = None
    _wanted_season = None
    _wanted_episode = None

    _func_to_run = None

    def __init__(self, callback):
        threading.Thread.__init__(self)

        self.callback = callback

        if self._URL is None:
            raise ValueError('URL has not been set')

    def set_tv(self, show, season, episode):
        self._wanted_show = show
        self._wanted_season = season
        self._wanted_episode = episode

        self._func_to_run = self._create_tvshow_request
        self.start()

    def set_movie(self, movie):
        self._wanted_movie = movie

        self._func_to_run = self._create_movie_request
        self.start()

    def run(self):
        self._func_to_run()

    def _create_tvshow_request(self):
        try:
            results = self._query_tv_show(show=self._wanted_show, season=self._wanted_season, episode=self._wanted_episode)
            self.callback(results)
        except EpisodeNotFound:
            print 'No results found, maybe the season or episode does not exist?'
        except ShowNotFound:
            print 'No results for show', self._wanted_show, 'were found'

    def _create_movie_request(self):
        try:
            results = self._query_movie(movie=self._wanted_movie)
            self.callback(results)
        except MovieNotFound:
            print 'No results found for', self._wanted_movie

    def _query_tv_show(self, show, season, episode):
        raise NotImplementedError('This method must be implemented')

    def _query_movie(self, movie):
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

class EpisodeNotFound(ProviderException):
    """
        Raised when the specified episode is not found
    """

class QualityNotFound(ProviderException):
    """
        Raised when the specified quality is not found
    """

class MovieNotFound(ProviderException):
    """
        Raised when the specified movie is not found
    """
