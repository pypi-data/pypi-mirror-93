# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['nutcracker',
 'nutcracker.chiper',
 'nutcracker.codex',
 'nutcracker.earwax',
 'nutcracker.graphics',
 'nutcracker.kernel',
 'nutcracker.smush',
 'nutcracker.sputm',
 'nutcracker.sputm.script',
 'nutcracker.utils']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=8.0.1,<9.0.0',
 'numpy>=1.19.1,<2.0.0',
 'parse>=1.18.0,<2.0.0',
 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['nutcracker = nutcracker.runner:app',
                     'smush = nutcracker.smush.runner:app']}

setup_kwargs = {
    'name': 'nutcracker',
    'version': '0.3.141',
    'description': 'Tools for editing resources in SCUMM games.',
    'long_description': '# NUTCracker\nTools for editing resources in SCUMM games.\n\n## NUT File Usage\n### Decoding\nDecode all NUT files in given directory DATADIR\n```\npython -m nutcracker.decode_san DATADIR/*.NUT --nut --target OUTDIR\n```\nCreates a font image file named chars.png in OUTDIR which can be edited using regular image editing software (e.g. GIMP)\n\n### Encoding\nEncode given font image (PNG_FILE) with given codec number (CODEC) using REF_NUT_FILE as reference\n```\npython -m nutcracker.encode_nut PNG_FILE --target NEW_NUT_FILE --ref REF_NUT_FILE --codec CODEC [--fake CODEC]\n```\nThis will convert font image file back to font file (NEW_NUT_FILE) which can be used in game.\n\nAvailable codecs: \n* 21 (FT + The Dig*)\n* 44 (COMI*)\n\n*FONT3.NUT and the fonts in The Dig was actually encoded using codec 21 method but marked as 44.\nIt can be achieved using `--codec 21 --fake 44`.\nsee examples in [test.bat](test.bat)\n',
    'author': 'BLooperZ',
    'author_email': 'blooperz@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
