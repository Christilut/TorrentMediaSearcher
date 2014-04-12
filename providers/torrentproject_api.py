import urllib2
import re

import simplejson
from bs4 import BeautifulSoup
import requests

from providers.base_api import *


class TorrentProjectAPI(BaseAPI):

    _URL = 'http://torrentproject.com/'

    def _query_tvshow(self, show, season, episode):
        query_string = show.replace(' ', '+')
        specifier = 's%02d' % season + 'e%02d' % episode

        query = query_string + '+' + specifier

        # Before searching with specified quality, do a search without, to see if the show exists
        if self._get_json(query=query_string)['total_found'] == '0':
            raise ShowNotFound('No results were found for show: ' + show)

        results = dict()

        try:
            quality = self._QUALITY_SPECIFIERS['normal tv']
            results[quality] = self._get_magnet_tv(query=query, quality=quality)
        except QualityNotFound:
            print 'Could not find anything matching the quality:', quality

        try:
            quality = self._QUALITY_SPECIFIERS['hd']
            results[quality] = self._get_magnet_tv(query=query, quality=quality)
        except QualityNotFound:
            print 'Could not find anything matching the quality:', quality

        try:
            quality = self._QUALITY_SPECIFIERS['fullhd']
            results[quality] = self._get_magnet_tv(query=query, quality=quality)
        except QualityNotFound:
            print 'Could not find anything matching the quality:', quality

        if len(results) == 0:   # No quality of any kind was found, most likely the episode does not exist.
            raise EpisodeNotFound('Could not find episode ' + str(episode) + ' of season ' + str(season) + ' of ' + show)

        return results

    def _query_movie(self, movie):
        query = movie.replace(' ', '+')

        # Before searching with specified quality, do a search without, to see if the movie exists
        if self._get_json(query=query)['total_found'] == '0':
            raise MovieNotFound('No results found for movie: ' + movie)

        search_terms = self._wanted_movie.split(' ')            # Get the words in the movie
        for s in search_terms:
            for lan in self._LANGUAGES:                         # This removes languages that are in the search terms. Otherwise movies with search terms equal to a langauge would always be skipped
                if re.match(s, lan, re.IGNORECASE):
                    self._LANGUAGES.remove(lan)

        results = dict()

        try:        # Often movies with many seeders on TorrentProject do not have a quality tag. So quality is unknown.
            results['unknown quality'] = self._get_magnet_movie(query=query)    # Do not specify a quality
        except QualityNotFound:
            print 'Could not find anything without quality specifiers'

        try:
            quality = self._QUALITY_SPECIFIERS['normal movie']
            results[quality] = self._get_magnet_movie(query=query, quality=quality)
        except QualityNotFound:
            print 'Could not find anything matching the quality:', quality

        try:
            quality = self._QUALITY_SPECIFIERS['hd']
            results[quality] = self._get_magnet_movie(query=query, quality=quality)
        except QualityNotFound:
            print 'Could not find anything matching the quality:', quality

        try:
            quality = self._QUALITY_SPECIFIERS['fullhd']
            results[quality] = self._get_magnet_movie(query=query, quality=quality)
        except QualityNotFound:
            print 'Could not find anything matching the quality:', quality

        if len(results) == 0:   # No quality of any kind was found, most likely the movie  does not exist.
            raise MovieNotFound('No results found for movie: ' + self._wanted_movie)

        return results

    def _get_json(self, query, quality=None):
        if quality is not None:     # Allow None so a search can be performed without any quality string
            query += '+' + quality

        try:
            req = urllib2.Request('http://torrentproject.com/?s=' + query + '&out=json')
        except requests.ConnectionError:
            raise LookupError('Could not reach host')

        f = urllib2.build_opener().open(req)

        json = simplejson.load(f)
        return json

    def _get_magnet(self, torrent_hash):
        torrent_url = self._URL + torrent_hash

        try:
            req = requests.get(torrent_url)
        except requests.ConnectionError:
            raise LookupError('Could not reach host')

        soup = BeautifulSoup(req.text, 'html.parser')

        magnet = soup.find(name='a', text=re.compile('Magnet Link'))

        if magnet is None:
            raise ValueError('Could not find the magnet link, did the website change?')

        return magnet.get('href')

    def _get_magnet_tv(self, query, quality):
        """ Returns the URL to a torrent/magnet link of specified quality or raise error if not found """

        json = self._get_json(query, quality)

        best = None
        num_seeds = 0
        num_leechs = 0

        for n in json:
            entry = json[n]

            # Perform some checks
            if n == 'total_found': continue                                                     # TorrentProject adds a total_found that we must ignore
            if entry['category'] != 'tv': continue                                              # Ignore anything that is not from the TV category
            if re.search('season', entry['title'], re.IGNORECASE) is not None: continue         # If the regular expression outcome is None, the word was not found. In this case, we do not want Season or Complete in it as they indicate full seasons instead of episodes
            if re.search('complete', entry['title'], re.IGNORECASE) is not None: continue       # Same with the word complete

            for s in self._TV_INDEX_SPECIFIERS:
                regex_result = re.search(s, entry['title'], re.IGNORECASE)
                if regex_result is not None:
                    if int(regex_result.group(1)) == self._wanted_season and int(regex_result.group(2)) == self._wanted_episode:
                        if entry['seeds'] > num_seeds or (entry['seeds'] == num_seeds and entry['leechs'] > num_leechs):  # Take link with most seeds, if the same amount, take the one with most leechs
                            best = entry
                            num_seeds = entry['seeds']
                            num_leechs = entry['leechs']

        if best is None:
            raise QualityNotFound()

        return self._get_magnet(torrent_hash=best['torrent_hash'])

    def _get_magnet_movie(self, query, quality=None):
        """ Returns the URL to a torrent/magnet link of specified quality or raise error if not found """

        json = self._get_json(query, quality)

        movie_regex = self._wanted_movie.replace(' ', '\D?')      # e.g. Movie?Name?5
        # movie_regex += '..\D{1}'

        if quality is None: quality = ''

        best = None
        num_seeds = 0
        num_leechs = 0

        for n in json:
            entry = json[n]

            # Perform some checks
            if n == 'total_found': continue                                                     # TorrentProject adds a total_found that we must ignore
            # if entry['category'] != 'hdrip' and entry['category'] != 'tv': continue           # Ignore anything that is not from the HDRIP or TV category (TorrentProjects puts SD quality movies in TV)
            if re.search(movie_regex, entry['title'], re.IGNORECASE) is None: continue          # Check if movie name is in the title in any form
            if self._contains_language(title=entry['title']): continue                          # Check if movie title contains language terms that we dont want
            if self._contains_specifier(title=entry['title']): continue                         # Check if the torrent is really a movie and not a tv show
            if re.search(quality, entry['title'], re.IGNORECASE) is None: continue              # Check that the quality string is in the title
            if self._contains_unwanted_quality_specifier(title=entry['title'], wanted_quality=quality): continue # Skip files that contains wrong quality identifiers

            if entry['seeds'] > num_seeds or (entry['seeds'] == num_seeds and entry['leechs'] > num_leechs):  # Take link with most seeds, if the same amount, take the one with most leechs
                best = entry
                num_seeds = entry['seeds']
                num_leechs = entry['leechs']

        if best is None:
            raise QualityNotFound()

        return self._get_magnet(torrent_hash=best['torrent_hash'])










