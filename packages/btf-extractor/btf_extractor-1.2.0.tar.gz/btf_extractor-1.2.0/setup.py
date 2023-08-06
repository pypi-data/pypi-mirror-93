# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['btf_extractor']

package_data = \
{'': ['*'], 'btf_extractor': ['c_ext/*']}

install_requires = \
['Pillow>=7', 'nptyping>=1,<2', 'numpy>=1.19,<2.0']

setup_kwargs = {
    'name': 'btf-extractor',
    'version': '1.2.0',
    'description': 'Extract UBO BTF archive format(UBO2003, UBO2014).',
    'long_description': '# BTF Extractor\nExtract UBO BTF archive format([UBO2003](https://cg.cs.uni-bonn.de/en/projects/btfdbb/download/ubo2003/), [UBO2014](https://cg.cs.uni-bonn.de/en/projects/btfdbb/download/ubo2014/)).\n\nThis repository uses [zeroeffects/btf](https://github.com/zeroeffects/btf)\'s [btf.hh](https://github.com/zeroeffects/btf/blob/master/btf.hh).\n\nExtract to ndarray compatible with openCV(BGR, channels-last).\n\n\n## Build tested on\n- Windows 10 20H2 + MSVC v14.20\n- MacOS 11(Big Sur) + Homebrew GCC 10.2.0\n- Ubuntu 20.04 + GCC 9.3.0\n\n## Install\n```bash\npip install btf-extractor\n```\n\n## Example\n```python\n>>> from btf_extractor import Ubo2003, Ubo2014\n\n>>> btf = Ubo2003("UBO_CORDUROY256.zip")\n>>> angles_list = list(btf.angles_set)\n>>> image = btf.angles_to_image(*angles_list[0])\n>>> print(image.shape)\n(256, 256, 3)\n>>> print(angles_list[0])\n(0, 0, 0, 0)\n\n>>> btf = Ubo2014("carpet01_resampled_W400xH400_L151xV151.btf")\n>>> print(btf.img_shape)\n(400, 400, 3)\n>>> angles_list = list(btf.angles_set)\n>>> image = btf.angles_to_image(*angles_list[0])\n>>> print(image.shape)\n(400, 400, 3)\n>>> print(angles_list[0])\n(60.0, 270.0, 60.0, 135.0)\n```\n',
    'author': '2-propanol',
    'author_email': 'nuclear.fusion.247@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/2-propanol/btf_extractor',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
