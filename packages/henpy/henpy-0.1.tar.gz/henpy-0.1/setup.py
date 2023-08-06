""" Henpy setup """

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup  # pylint: disable=E0611,F0401


setup(
    name='henpy',
    version=0.1,
    install_requires=[],
    packages=['henpy'],
    author='Werner Van Geit',
    author_email='werner.vangeit@gmail.com',
    entry_points={'console_scripts': ['henpy=henpy.henpy:main'], },
    license="LGPLv3",
    keywords=(),
    classifiers=[
        'Development Status :: 4 - Beta'])
