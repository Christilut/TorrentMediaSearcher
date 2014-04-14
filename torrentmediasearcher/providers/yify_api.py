import simplejson
import requests
import urllib2

from base_api import BaseAPI, MovieNotFound, QualityNotFound


class YIFYAPI(BaseAPI):

    _URL = 'http://yts.re/api/'


    def _query_movie(self, movie, year, quality):
        query = 'keywords=' + movie.replace(' ', '%20')
        if year is not None: query += '%20' + str(year)

        result = self._get_magnet_movie(query=query, quality=quality)

        return result

    def _get_json(self, query):

        try:
            req = urllib2.Request(self._URL + 'list.json?' + query)
        except requests.ConnectionError:
            raise LookupError('Could not reach host')

        f = urllib2.build_opener().open(req)

        json = simplejson.load(f)

        return json

    def _get_magnet_movie(self, query, quality):

        json = self._get_json(query=query)
        if 'error' in json:
            if json['error'] == 'No movies found':
                raise MovieNotFound('No results found for movie: ' + self._wanted_movie)

        movie = None
        movielist = json['MovieList']

        if quality is None:     # If no quality specified, use first result.
            movie = movielist[0]
        else:
            for n in range(0, json['MovieCount']):
                if movielist[n]['Quality'] == quality:
                    movie = movielist[n]

        if movie is None:
            raise QualityNotFound('Could not find anything matching the quality: ' + str(quality))

        return { 'magnet': movie['TorrentMagnetUrl'], 'seeds': movie['TorrentSeeds'] }