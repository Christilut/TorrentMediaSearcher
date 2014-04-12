import re


class BaseAPI():

    _URL = None

    _QUALITY_SPECIFIERS = {
        'normal tv' : 'HDTV',
        'normal movie' : 'XVID',
        'hd' : '720p',
        'fullhd' : '1080p',
    }

    _TV_INDEX_SPECIFIERS = [
            r'S(\d+)E(\d+)',            # Regex for S??E??
            r'(\D+\d{2})x(\d{2}\D+)',   # Regex for ??x?? and makes sure before and after are no numbers or it could match a resolution (1024x768)
        ]

    _LANGUAGES = [                  # Common language keywords found in torrents, so we can filter them. Sorry, only English supported for now.
             'GERMAN',
             'FRENCH',
             'DUTCH',
             'NL',
             'ITALIAN',
             'SPANISH',
             'LATINO',
             'RUS',
             'HEBREW',
    ]

    _wanted_movie = None
    _wanted_show = None
    _wanted_season = None
    _wanted_episode = None

    _func_to_run = None

    def __init__(self, callback):
        self.callback = callback

        if self._URL is None:
            raise ValueError('URL has not been set')

    def create_tvshow_request(self, show, season, episode):
        self._wanted_show = show
        self._wanted_season = season
        self._wanted_episode = episode
        results = self._query_tvshow(show=self._wanted_show, season=self._wanted_season, episode=self._wanted_episode)
        self.callback(results)

    def create_movie_request(self, movie):
        self._wanted_movie = movie
        results = self._query_movie(movie=movie)
        self.callback(results)

    def _query_tvshow(self, show, season, episode):
        raise NotImplementedError('This method must be implemented')

    def _query_movie(self, movie):
        raise NotImplementedError('This method must be implemented')

    def _contains_language(self, title):
        for lan in self._LANGUAGES:
            if re.search(lan, title, re.IGNORECASE) is not None:    # If found
                return True
        return False

    def _contains_specifier(self, title):
        for s in self._TV_INDEX_SPECIFIERS:
            if re.search(s, title, re.IGNORECASE) is not None:
                return True
        return False

    def _contains_unwanted_quality_specifier(self, title, wanted_quality):
        for q in self._QUALITY_SPECIFIERS:
            if self._QUALITY_SPECIFIERS[q] == wanted_quality: continue         # Don't check the wanted quality
            if re.search(self._QUALITY_SPECIFIERS[q], title, re.IGNORECASE) is not None:    # If found
                return True
        return False

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
