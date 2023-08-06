import os
from setuptools import setup, find_packages

version = '1.8'

try:
    readme = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()
    readme = readme.replace('.. code-block:: none', '.. code-block::')
    screenshots = open(
        os.path.join(os.path.dirname(__file__), 'SCREENSHOTS.rst')
    ).read()
    screenshots = screenshots.replace(
        '.. image:: _static',
        '.. figure:: https://github.com/barseghyanartur/django-admin-timeline'
        '/raw/master/docs/_static')
except:
    readme = ''
    screenshots = ''

template_dir = "src/admin_timeline/templates/admin_timeline"
templates = [os.path.join(template_dir, f) for f in os.listdir(template_dir)]

static_dir = "src/admin_timeline/static"
static_files = [os.path.join(static_dir, f) for f in os.listdir(static_dir)]

setup(
    name='django-admin-timeline',
    version=version,
    description="Facebook-like timeline for Django admin",
    long_description="{0}{1}".format(readme, screenshots),
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "License :: OSI Approved :: GNU Lesser General Public License v2 or "
        "later (LGPLv2+)",
    ],
    keywords='django-admin-timeline, django, app, python',
    author='Artur Barseghyan',
    author_email='artur.barseghyan@gmail.com',
    url='https://github.com/barseghyanartur/django-admin-timeline',
    package_dir={'': 'src'},
    packages=find_packages(where='./src'),
    license='GPL-2.0-only OR LGPL-2.1-or-later',
    package_data={
        'admin_timeline': templates + static_files
    },
    include_package_data=True,
    install_requires=[
        'six>=1.7.3',
        'django-nine>=0.1.10'
    ],
    tests_require=[
        'factory_boy',
        'fake-factory',
        'pytest',
        'pytest-django',
        'radar>=0.3',
    ],
)
