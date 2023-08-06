# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bumblebee',
 'bumblebee.bases',
 'bumblebee.datasets',
 'bumblebee.datasets.batch',
 'bumblebee.effects',
 'bumblebee.managers',
 'bumblebee.misc',
 'bumblebee.sources']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.19.0,<2.0.0', 'opencv-python>=4.4.0,<5.0.0']

entry_points = \
{'console_scripts': ['hi = hello:hello']}

setup_kwargs = {
    'name': 'eyecu-bumblebee',
    'version': '0.5.7',
    'description': 'Advanced pipelines for video datasets',
    'long_description': '# Bumblebee\n[![PyPI](https://img.shields.io/pypi/v/eyecu_bumblebee.svg)](https://pypi.python.org/pypi/eyecu_bumblebee)\n[![Downloads](https://pepy.tech/badge/eyecu-bumblebee/week)](https://pepy.tech/project/eyecu-bumblebee) \\\n![Bumblebee image](./docs/bumblebee.png)\n\nBumblebee provides high level components to construct training pipelines for videos conveniently.\n\n\n- [Install](#install)\n- [Motivation](#motto)\n- [Our Websites](#our-websites)\n- [Examples](#examples)\n    - [A pipeline with basic elements](#a-pipeline-with-basic-elements)\n    - [Using Manager API](#using-manager-api)\n    - [Read limited section of video](#read--limited-section-of-video)\n    - [Iterate frames with frame numbers](#iterate-frames-with-frame-numbers)\n    - [Iterate frames in batches](#iterate-frames-in-batches)\n- [Team](#team)\n- [License](#license)\n\n\n\n## Install\n\n```\npip install eyecu_bumblebee\n```\n\n## Motivation\n\nEverything should be made as simple as possible, but no simpler. - Albert Einstein\n\n## Our Websites\n\n[EyeCU Vision](https://eyecuvision.com/) \\\n[EyeCU Future](https://eyecufuture.com/) \n\n\n## Examples\n\n### A pipeline with basic elements\n\n```python\nfrom bumblebee import *\n\n\nif __name__ == "__main__":\n    \n    video_path = "/path/to/video.mp4"\n\n    # Create a source\n    file_stream = sources.FileStream(video_path)\n\n    # Add an effect\n    goto = effects.GoTo(file_stream)\n\n    END_OF_VIDEO = file_stream.get_duration()\n    goto(END_OF_VIDEO)\n\n    # Create a dataset\n    single_frame = datasets.Single(file_stream)\n\n    last_frame = single_frame.read()\n\n```\n\n### Using Manager API\n\n```python\nfrom bumblebee import *\n\n\nif __name__ == "__main__":\n    \n    # Create a training manager\n    manager = managers.BinaryClassification(\n        ["path/to/video_dir","path/to/another_dir"],\n        ["path/to/labels"]\n    )\n\n    number_of_epochs = 300\n    \n    for epoch,(frame_no,frame,prob) in manager(number_of_epochs):\n        # Use data stuff\n        ...    \n\n```\n\n\n### Read  limited section of video\n```python\nfrom bumblebee import *\n\n\nif __name__ == "__main__":\n  \n    video_path = "/path/to/video.mp4"\n    start_frame = 35\n    end_frame = 40\n    \n    file_stream = sources.FileStream(video_path)\n    \n    limited_stream = effects.Start(file_stream,start_frame)\n    limited_stream = effects.End(limited_stream,end_frame)\n\n    single_frame = datasets.Single(file_stream)\n\n    for frame in single_frame:\n        ...  \n\n```\n\n### Iterate frames with frame numbers\n```python\nfrom bumblebee import *\n\n\nif __name__ == "__main__":\n  \n    video_path = "/path/to/video.mp4"\n    \n    file_stream = sources.FileStream(video_path)\n    \n    single_frame = datasets.Single(file_stream)\n    current_frame = effects.CurrentFrame(file_stream)\n    \n    \n    for frame_ind,frame in zip(current_frame,single_frame):\n        ...  \n\n``` \n\n\n\n### Iterate frames in batches\n\n```python\nfrom bumblebee import *\n\n\nif __name__ == "__main__":\n  \n    video_path = "/path/to/video.mp4"\n    batch_size = 64\n    \n    file_stream = sources.FileStream(video_path)\n    \n    batch = datasets.Batch(file_stream)\n    \n    for frames in batch:\n        ...  \n\n``` \n\n## Team\nThis project is currently developed and maintained by [ovuruska](https://github.com/ovuruska).\n\n\n## License\nBumblebee has MIT license. You can find further details in [LICENSE](LICENSE).\n\n',
    'author': 'Oguz Vuruskaner',
    'author_email': 'ovuruska@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Eye-C-U/bumblebee/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
