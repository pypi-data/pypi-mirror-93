# coding=utf-8
from pathlib import Path
from setuptools import setup, find_packages
import os

# with open("README.md", "r",encoding='utf8') as fh:
#     long_description = fh.read()

# filepath = ((Path(__file__).parent / Path('README.md')).absolute()).as_posix()
filepath = 'README.md'
print(filepath)

install_requires = [
    'pymongo==3.5.1',
    'tomorrow3==1.1.0',
    'concurrent-log-handler==0.9.9',
    'elasticsearch',
    'kafka-python==1.4.6',
    'requests',
    'pika',
    'flask',
    'python-json-logger==0.1.10',
]

if os.name == 'nt':
    install_requires.append('pywin32')

setup(
    name='nb_log',  #
    version="4.2",
    description=(
        'very sharp color display,monkey patch bulitin print  and high-performance multiprocess safe roating file handler,other handlers includeing dintalk ,email,kafka,elastic and so on '
    ),
    keywords=("logging", "logger", "multiprocess file handler", "color handler"),
    # long_description=open('README.md', 'r',encoding='utf8').read(),
    long_description_content_type="text/markdown",
    long_description=open(filepath, 'r', encoding='utf8').read(),
    # data_files=[filepath],
    author='bfzs',
    author_email='ydf0509@sohu.com',
    maintainer='ydf',
    maintainer_email='ydf0509@sohu.com',
    license='BSD License',
    packages=find_packages(),
    include_package_data=True,
    platforms=["all"],
    url='',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries'
    ],
    install_requires=install_requires
)
"""
打包上传
python setup.py sdist upload -r pypi


python setup.py sdist & twine upload dist/nb_log-4.2.tar.gz
twine upload dist/*


python -m pip install nb_log --upgrade -i https://pypi.org/simple   # 及时的方式，不用等待 阿里云 豆瓣 同步
"""
