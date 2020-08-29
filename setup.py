"""
:copyright: Copyright (c) 2020 Jeremiah Ikosin (@ziord)
:license: MIT, see LICENSE for more details
"""

from setuptools import setup, find_packages
import info

data = info.get_info()


setup(
    name=data["name"]+'.py',
    version=data["version"],
    description=data["description"],
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url=data["project_urls"]["Source Code"],
    author=data["author"],
    license=data["license"],
    keywords=data["keywords"],
    project_urls=data["project_urls"],
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'info': [*data['package_data'].values()]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
