# Copyright 2020 William José Moreno Reyes
# This file is part of open-marquesote.
#
#  Foobar is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Foobar is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with Foobar.  If not, see <https://www.gnu.org/licenses/>.
#
#  Contributors:
#   - William Moreno Reyes

from setuptools import setup
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    description = f.read()

setup(
    name="open-marquesote",
    version="1.0.1",
    author="William José Moreno Reyes",
    author_email="williamjmorenor@gmail.com",
    description="Minimal Web Browser",
    long_description=description,
    long_description_content_type='text/markdown',
    packages=["open_marquesote"],
    include_package_data=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable"
    ],
    install_requires=[
        "PyQtWebEngine",
        "waitress"
    ]
)
