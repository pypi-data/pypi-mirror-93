import os

from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as ld:
    long_description = ld.read()

with open(os.path.join(os.path.dirname(__file__), 'requirements.txt')) as f:
    lines = [line.strip() for line in f]
    requirements = [line for line in lines if line and not line.startswith('#')]

setup(
    name='bingwp',
    version='0.1.7',
    description='download bing.ioliu.cn wallpaper',
    author='heatdesert',
    author_email='wall.corner@outlook.com',
    url='https://github.com/Greatwallcorner/BingWallpaperDownload-ioliu/',
    packages=find_packages(),
    platforms='any',
    license='MIT',
    long_description=long_description,
    keywords='bing wallpaper download',
    install_requires=requirements,
    long_description_content_type='text/markdown',
    entry_points={'console_scripts': 'bingwp = ioliu.app:main'}

)
