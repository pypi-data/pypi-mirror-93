# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['plotdigitizer']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.5.3,<0.6.0',
 'matplotlib>=3.3.4,<4.0.0',
 'numpy>=1.19.5,<2.0.0',
 'opencv-python>=4.5.1,<5.0.0']

entry_points = \
{'console_scripts': ['plotdigitizer = plotdigitizer.plotdigitizer:main',
                     'plotdigitizer-locate = plotdigitizer.locate:main']}

setup_kwargs = {
    'name': 'plotdigitizer',
    'version': '0.1.3',
    'description': 'Extract raw data from plots images',
    'long_description': "![Python application](https://github.com/dilawar/PlotDigitizer/workflows/Python%20application/badge.svg) [![PyPI version](https://badge.fury.io/py/plotdigitizer.svg)](https://badge.fury.io/py/plotdigitizer) [![DOI](https://zenodo.org/badge/140683649.svg)](https://zenodo.org/badge/latestdoi/140683649)\n\nA Python3 utility to digitize plots. \n\n## Installation\n\n```\n$ python3 -m pip install plotdigitizer \n$ plotdigitizer --help\n```\n\n## Usage\n\nFirst, remove all text from the image, leave only axis and the plot. I use\n`gthumb` utility. You can also use imagemagick or gimp.\n\nFollowing image is from MacFadden and Koshland, PNAS 1990 after trimming. One\ncan also remove top and right axis.\n\n![Trimmed image](./figures/trimmed.png)\n\n__Run the utility__\n\n```\nplotdigitizer ./figures/trimmed.png -p 0,0 -p 10,0 -p 0,1\n```\n\nWe need three points (`-p` option) to map axes onto the images.  In the example\nabove, these are `0,0` (where x-axis and y-axis intesect) , `20,0` (a point on\nx-axis) and `0,1` (a point on y-axis). To map these points on the image, you\nwill be asked to click on these points on the image. _Make sure to click in\nthe same order and click on the points as precisely as you could. Any error in\nthis step will propagate._\n\nThe data-points will be dumped to a csv file e.g., __`--output\n/path/to/file.csv`__. \n\nIf `--plot output.png` is passed, a plot of the extracted data-points will be\nsaved to `output.png`. This requires `matplotlib`.\n\n![](./figures/traj.png)\n\nNotice the errors near the boxes; since we have not trimmed them.\n\n## Using in batch mode\n\nYou can pass the coordinates of points in the image at the command prompt.\nThis allows to run in the batch mode without any need for the user to click on\nthe image.\n\n```bash\nplotdigitizer ./figures/trimmed.png -p 0,0 -p 20,0 -p 0,1 -l 22,295 -l 142,295 -l 22,215 --plot output.png\n```\n\n### How to find coordinates for these points\n\nIn the example above, point `0,0` is mapped to coordinate `22,295` i.e., the\ndata point `0,0` is on the 22nd row and 295th column _assuming that bottom left\nof the image is first row, first column `(0,0)`. We have provide a utility\n`plotdigitizer-locate` (script `plotdigitizer/locate.py`) which you can use on\nthe image to find the coordinates.\n\nIf you have installed the utility using `pip install`\n\n```bash\n$ plotdigitizer-locate figures/trimmed.png     \n```\n\nor, from the source,\n\n```bash\n$ python3 plotdigitizer/locate.py figures/trimmed.png\n```\n\nThis open a windows, you can click on the desired point and its coordinate will\nbe written on the image itself. Note them down.\n\n![](./figures/trimmed_locate.png)\n\n\n# Examples\n\n![original](./figures/graphs_1.png)\n\n```bash\nplotdigitizer figures/graphs_1.png \\\n\t\t-p 1,0 -p 6,0 -p 0,3 \\\n\t\t-l 165,160 -l 599,160 -l 85,60 \\\n\t\t--plot figures/graphs_1.result.png \\\n\t\t--preprocess\n```\n\n![reconstructed](./figures/graphs_1.result.png)\n\n\n![original](./figures/ECGImage.png)\n\n```\nplotdigitizer  figures/ECGImage.png \\\n\t\t-p 1,0 -p 5,0 -p 0,1 -l 290,337 \\\n\t\t-l 1306,338 -l 106,83 \\\n\t\t--plot figures/ECGImage.result.png\n```\n\n![reconstructed](./figures/ECGImage.result.png)\n\n# Limitations\n\nCurrently this script has following limitations:\n\n- Background must not be transparent. It might work with transparent background but\n  I've not tested it.\n- Only b/w images are supported for now. Color images will be converted to grayscale upon reading.\n- One image should have only one trajectory.\n\n## Related projects by others\n\n1.  [WebPlotDigitizer](https://automeris.io/WebPlotDigitizer/) by Ankit\nRohatagi is very versatile.\n",
    'author': 'Dilawar Singh',
    'author_email': 'dilawar.s.rajput@gmail.com',
    'maintainer': 'Dilawar Singh',
    'maintainer_email': 'dilawar.s.rajput@gmail.com',
    'url': 'https://github.com/dilawar/PlotDigitizer',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
