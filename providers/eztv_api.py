import re
import requests
from bs4 import BeautifulSoup

from providers.base_api import BaseAPI, QualityNotFound, ShowNotFound, EpisodeNotFound


class EZTVAPI(BaseAPI):

    _URL = "http://eztv.it"

    def _query_tvshow(self, show, season, episode):
        show_id = self._get_show_id(show=show)

        results = dict()

        try:
            quality = self._QUALITY_SPECIFIERS['normal tv']
            results[quality] = self._get_magnet_tv(show_id=show_id, show=show, season=season, episode=episode, quality=quality)
        except QualityNotFound:     # Quality not found, just ignore it
            print 'Could not find anything matching the quality:', quality

        try:
            quality = self._QUALITY_SPECIFIERS['hd']
            results[quality] = self._get_magnet_tv(show_id=show_id, show=show, season=season, episode=episode, quality=quality)
        except QualityNotFound:
            print 'Could not find anything matching the quality:', quality

        try:
            quality = self._QUALITY_SPECIFIERS['fullhd']
            results[quality] = self._get_magnet_tv(show_id=show_id, show=show, season=season, episode=episode, quality=quality)
        except QualityNotFound:
            print 'Could not find anything matching the quality:', quality

        if len(results) == 0:   # No quality of any kind was found, most likely the episode does not exist.
            raise EpisodeNotFound('Could not find episode ' + str(episode) + ' of season ' + str(season) + ' of ' + show)

        return results

    def _query_movie(self, *args):
        raise RuntimeError('Movies are not supported in the EZTV provider')

    def _get_show_id(self, show):
        # all strings are in lowercase
        show = show.lower()
        terms = show.split(' ')

        try:
            req = requests.get(self._URL, timeout=5)
        except requests.ConnectionError:
            raise LookupError('Could not reach host')

        soup = BeautifulSoup(req.content, 'html.parser')

        tv_shows = str(
            soup('select', {'name': 'SearchString'})).split('</option>')
        for tv_show in tv_shows:
            tv_show = tv_show.lower()
            if all(x in tv_show for x in terms):
                show_id = re.search(r"\d+", tv_show).group()
                break
        else:
            raise ShowNotFound()

        return show_id


    def _get_magnet_tv(self, show_id, show, season, episode, quality):

        show_url = self._URL + '/shows/' + show_id + '/'

        try:
            req = requests.get(show_url, timeout=5)
        except requests.ConnectionError:
            raise LookupError('Could not reach host')

        soup = BeautifulSoup(req.content, 'html.parser')

        episodes = soup.find_all(class_='epinfo')

        wanted_episode = None

        for e in episodes:
            if re.search(show, e.text, re.IGNORECASE) is None: continue     # Skip if text does not contain show name
            if re.search(quality, e.text, re.IGNORECASE) is None: continue  # Skip if text does not contain wanted quality

            for s in self._TV_INDEX_SPECIFIERS:
                regex_result = re.search(s, e.text, re.IGNORECASE)
                if  regex_result is not None:
                    if int(regex_result.group(1)) == season and int(regex_result.group(2)) == episode:
                        wanted_episode = e
                        break

            if wanted_episode is not None:
                break

        if wanted_episode is None:
            raise QualityNotFound()

        return wanted_episode.parent.next_sibling.next_sibling.find(class_='magnet').get('href')



