"""
:copyright: Copyright (c) 2020 Jeremiah Ikosin (@ziord)
:license: MIT, see LICENSE for more details
"""

from setuptools import setup, find_packages
import info

data = info.get_info()
setup(
    name=data["name"],
    version=data["version"],
    description=data["description"],
    long_description=open('README.md').read(),
    author=data["author"],
    license=data["license"],
    keywords=data["keywords"],
    project_urls=data["project_urls"],
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'info': [*data['package_data'].values()]
    }
)
