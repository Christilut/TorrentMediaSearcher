TorrentMediaSearcher
====================

Fetches magnet links from various torrent providers.

Allows specifying a movie or show name, season, episode and returns (if available) magnet links to the content of the requested quality.
Torrents with the most seeds are prioritized. Works with threads and a function can be specified to send the results to.

Features
===

- Very easy to use

- Returns a magnet link from the specified provider and lists seeds (if provider shows seeds)

- Provides exceptions

Torrent providers
===

- EZTV (tv)

- TorrentProject (tv/movies)

- YIFY (movies)

- More can be requested

Usage
===

For usage examples, see:

https://github.com/Christilut/TorrentMediaSearcher/blob/master/examples/examples.py

Installation
===

Windows users can run the .exe installer

Everyone can run:

python setup.py install

Dependencies
===

- requests

- beautifulsoup4

- simplejson