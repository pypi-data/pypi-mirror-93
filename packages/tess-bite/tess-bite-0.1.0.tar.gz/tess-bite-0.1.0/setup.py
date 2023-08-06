# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['tess_bite']

package_data = \
{'': ['*']}

install_requires = \
['astropy>=4.0',
 'httpx>=0.16.1',
 'lightkurve>=1.11.3,<2.0.0',
 'numpy>=1.19',
 'tess-locator>=0.2.0,<0.3.0']

setup_kwargs = {
    'name': 'tess-bite',
    'version': '0.1.0',
    'description': 'Take a bite out of TESS Full Frame Images using HTTP range requests.',
    'long_description': 'tess-bite\n============\n\n**Take a quick bite out of TESS Full Frame Images using HTTP range requests.**\n\n|pypi|\n\n.. |pypi| image:: https://img.shields.io/pypi/v/tess-bite\n                :target: https://pypi.python.org/pypi/tess-bite\n\n\n`tess-bite` is a user-friendly package which provides fast access to sections of TESS Full-Frame Image (FFI) data.\nIt uses the HTTP range request mechanism to download only those parts of an FFI that are required\nto obtain a cut-out image.\n\nInstallation\n------------\n\n.. code-block:: bash\n\n    python -m pip install tess-bite\n\nExample use\n-----------\n\nObtain a Target Pixel File for a stationary object:\n\n.. code-block:: python\n\n    >>> from tess_bite import bite\n    >>> bite("Alpha Cen", shape=(10, 10))\n    TargetPixelFile("Alpha Cen")\n\n\nObtain a Target Pixel File centered on a moving asteroid:\n\n.. code-block:: python\n\n    >>> from tess_bite import bite_asteroid\n    >>> bite_asteroid("Vesta", start="2019-04-28", stop="2019-06-28)\n    TargetPixelFile("Vesta")\n\n\nObtain a cut-out image from a single FFI:\n\n.. code-block:: python\n\n    >>> from tess_bite import bite_ffi\n    >>> bite_ffi(url, col=50, row=20, shape=(20, 20))\n\n\nQuickly download the header of an FFI:\n\n.. code-block:: python\n\n    >>> from tess_bite import bite_header\n    >>> bite_header(url, ext=0)\n    FitsHeader\n\n\nWhat are HTTP range requests?\n-----------------------------\n\nTess-bite is powered by the `HTTP range request <https://developer.mozilla.org/en-US/docs/Web/HTTP/Range_requests>`_ protocol.\nThis is a mechanism which allows a client to request specific bytes from a file on a web server.\nFor example, downloading a 3-by-3 pixel square of 4-byte pixel values from a TESS image\ncan be done very quickly using a HTTP request as follows:\n\n.. code-block:: python\n\n    >>> import httpx\n    >>> url = "https://mast.stsci.edu/portal/Download/file?uri=mast:TESS/product/tess2019142115932-s0012-2-1-0144-s_ffic.fits"\n    >>> resp = httpx.get(url, headers={"Range": "bytes=80000-80012,80020-80032,80040-80052"})\n    >>> print(resp.text)\n\n    --00000000000000000103\n    Content-Type: application/octet-stream\n    Content-Range: bytes 80000-80012/35553600\n\n    D\x1aA@DLR½DW˜oD\n    --00000000000000000103\n    Content-Type: application/octet-stream\n    Content-Range: bytes 80020-80032/35553600\n\n    ³D\x0b.]D\x05ªJD\n    --00000000000000000103\n    Content-Type: application/octet-stream\n    Content-Range: bytes 80040-80052/35553600\n\n    D-aöD+W/D\x18R\x16D\n    --00000000000000000103--\n\nOf course the difficult part is to translate pixel coordinates to byte positions,\nand to convert bytes to pixel values.  Tess-bite takes care of these steps for you!\n\n\nDocumentation\n-------------\n\nComing soon!\n\n\nSimilar services\n----------------\n\n`TESScut <https://mast.stsci.edu/tesscut/>`_ is an excellent API service which allows cut outs\nto be obtained for stationary objects.  Tess-bite provides an alternative implementation of this\nservice by leveraging the `HTTP range requests <https://developer.mozilla.org/en-US/docs/Web/HTTP/Range_requests>`_\nmechanism to download pixel values directly from FFI files.\n\nCompared to TESScut, the goal of tess-bite is provide an alternative way to obtain cut-outs which\ndoes not require a central API service, but can instead be run on a local machine or in the cloud.\nAt this time tess-bite is an experiment, we recommend that you keep using TESScut for now!\n',
    'author': 'Geert Barentsen',
    'author_email': 'hello@geert.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/SSDataLab/tess-bite',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
