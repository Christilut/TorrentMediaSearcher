from distutils.core import setup

setup(
	name = 'TorrentMediaSearcher',
	packages = ['torrentmediasearcher', 'torrentmediasearcher.providers'],
	version = '1.0.2',
	description = 'Fetches TV and movie magnet links from various torrent providers',
	author = 'Christiaan Maks',
	author_email = 'christiaanmaks@mylittlesky.net',
	url = 'https://github.com/Christilut/TorrentMediaSearcher',
	keywords = ['torrent', 'magnet', 'eztv', 'yify', 'tv', 'movie'],
	classifiers = [
		'Programming Language :: Python',
		'Development Status :: 4 - Beta',
		'Intended Audience :: Developers',
		'Environment :: Other Environment',
		'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
		'Operating System :: OS Independent',
		'Topic :: Software Development :: Libraries :: Python Modules',
		'Topic :: Communications :: File Sharing',
		],		
)
	