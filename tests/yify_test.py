import unittest

from torrentmediasearcher.providers.yify_api import YIFYAPI


class YIFYTest(unittest.TestCase):

    def test_create_query(self):
        """
            _create_query should return a string with the movie title seperated by %20 instead of spaces and add the year if it is supplied
        """

        movie = 'iron man 3'
        year = 2013
        quality = '1080p'

        yify = YIFYAPI(None)

        query = yify._create_query(movie=movie, year=year)

        self.assertTrue(query.startswith('keywords='))
        self.assertFalse(' ' in query)

        split_movie = movie.split(' ')

        for term in split_movie:
            self.assertTrue(term in query)

    def test_get_json(self):
        """
            _get_json should return a valid json or raise a LookupError incase of network issues
        """
        pass

    def test_get_magnet_movie(self):
        """
            _get_magnet_movie should return a dict() with magnet and seeds key or raise an exception: MovieNotFound, QualityNotFound, LookupError
        """

        movie = 'iron man 3'
        year = 2013
        quality = '1080p'

        yify = YIFYAPI(None)
        yify._wanted_movie = movie

        query = yify._create_query(movie=movie, year=year)

        result = yify._get_magnet_movie(query=query, quality=quality, year=year)

        self.assertTrue('seeds' in result.keys())
        self.assertTrue('magnet' in result.keys())
        self.assertEqual(2, len(result))

        self.assertTrue(result['magnet'].startswith('magnet:?'))
        self.assertGreaterEqual(int(result['seeds']), 0)




if __name__ == "__main__":
    unittest.main()
