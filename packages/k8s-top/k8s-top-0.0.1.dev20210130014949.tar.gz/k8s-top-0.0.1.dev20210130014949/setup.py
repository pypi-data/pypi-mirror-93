#!/usr/bin/env python
#   -*- coding: utf-8 -*-

from setuptools import setup
from setuptools.command.install import install as _install

class install(_install):
    def pre_install_script(self):
        pass

    def post_install_script(self):
        pass

    def run(self):
        self.pre_install_script()

        _install.run(self)

        self.post_install_script()

if __name__ == '__main__':
    setup(
        name = 'k8s-top',
        version = '0.0.1.dev20210130014949',
        description = 'K8S Top is a console dashboard and monitoring utility for Kubernetes',
        long_description = '# K8S Top - Console Dashboard and Monitoring Utility for Kubernetes\n\n[![Gitter](https://img.shields.io/gitter/room/karellen/lobby?logo=gitter)](https://gitter.im/karellen/lobby)\n\n[![K8STop Version](https://img.shields.io/pypi/v/k8s-top?logo=pypi)](https://pypi.org/project/k8s-top/)\n[![K8STop Python Versions](https://img.shields.io/pypi/pyversions/k8s-top?logo=pypi)](https://pypi.org/project/k8s-top/)\n[![K8STop Downloads Per Day](https://img.shields.io/pypi/dd/k8s-top?logo=pypi)](https://pypi.org/project/k8s-top/)\n[![K8STop Downloads Per Week](https://img.shields.io/pypi/dw/k8s-top?logo=pypi)](https://pypi.org/project/k8s-top/)\n[![K8STop Downloads Per Month](https://img.shields.io/pypi/dm/k8s-top?logo=pypi)](https://pypi.org/project/k8s-top/)\n\n',
        long_description_content_type = 'text/markdown',
        classifiers = [
            'License :: OSI Approved :: Apache Software License',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Operating System :: MacOS :: MacOS X',
            'Operating System :: POSIX',
            'Operating System :: POSIX :: Linux',
            'Environment :: Console',
            'Topic :: Utilities',
            'Topic :: System :: Monitoring',
            'Topic :: System :: Distributed Computing',
            'Topic :: System :: Clustering',
            'Topic :: System :: Networking',
            'Topic :: System :: Networking :: Monitoring',
            'Intended Audience :: System Administrators',
            'Intended Audience :: Developers',
            'Development Status :: 4 - Beta'
        ],
        keywords = 'kubernetes k8s kube top monitoring dashboard',

        author = 'Karellen, Inc.',
        author_email = 'supervisor@karellen.co',
        maintainer = 'Arcadiy Ivanov',
        maintainer_email = 'arcadiy@karellen.co',

        license = 'Apache License, Version 2.0',

        url = 'https://github.com/karellen/k8s-top',
        project_urls = {
            'Bug Tracker': 'https://github.com/karellen/k8s-top/issues',
            'Documentation': 'https://github.com/karellen/k8s-top/',
            'Source Code': 'https://github.com/karellen/k8s-top/'
        },

        scripts = [],
        packages = ['k8stop'],
        namespace_packages = [],
        py_modules = [],
        entry_points = {},
        data_files = [],
        package_data = {
            'k8stop': ['LICENSE']
        },
        install_requires = [
            'gevent>=21.1.2',
            'kubernetes~=12.0',
            'picotui~=1.1.2'
        ],
        dependency_links = [],
        zip_safe = True,
        cmdclass = {'install': install},
        python_requires = '>=3.6',
        obsoletes = [],
    )
