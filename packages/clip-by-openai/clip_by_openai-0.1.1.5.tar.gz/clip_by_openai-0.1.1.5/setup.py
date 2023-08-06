#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages
from pathlib import Path

core_req = ['ftfy', 'regex', 'tqdm', 'torch==1.7.1', 'torchvision==0.8.2']
extras_require={
    'cuda': ['cudatoolkit==11.0'],
    'dev': ['pytest']
}
package_data = [str(x) for x in list(Path('clip').rglob("*.gz"))]
package_data.extend([str(x) for x in list(Path('clip').rglob("*.md"))])

setup(
    name='clip_by_openai',
    version='0.1.1.5',
    author="OpenAI",
    author_email="",
    description="CLIP by OpenAI",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    keywords="vector, embeddings, machinelearning, ai, artificialintelligence, nlp, pytorch, nearestneighbors, search, analytics, clustering, dimensionalityreduction",
    license="MIT",
    packages=find_packages(exclude=["tests*"]),
    package_data={'clip': package_data},
    include_package_data=True,
    python_requires=">=3",
    install_requires=core_req,
    extras_require=extras_require,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Financial and Insurance Industry",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Database",
        "Topic :: Internet :: WWW/HTTP :: Indexing/Search",
        "Topic :: Multimedia :: Sound/Audio :: Conversion",
        "Topic :: Multimedia :: Video :: Conversion",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Image Recognition",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Scientific/Engineering :: Visualization",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
    ],
)
