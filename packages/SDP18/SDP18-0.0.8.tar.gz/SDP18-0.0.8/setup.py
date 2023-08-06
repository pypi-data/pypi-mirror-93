from setuptools import setup, find_packages

classifiers = [
	'Development Status :: 5 - Production/Stable',
	'Intended Audience :: Education',
	'Operating System :: Microsoft :: Windows :: Windows 10',
	'License :: OSI Approved :: MIT License',
	'Programming Language :: Python :: 3'
]

setup(
	name='SDP18',
	version='0.0.8',
	description='NUS SDP 18',
	long_description=open('README.md').read() + 'SA, GA, HCO, TS',
	url='https://github.com/lwq96/NewProject',
	author='SDP18',
	author_email='e0176071@u.nus.edu',
	license='MIT',
	classifiers=classifiers,
	keywords='metaheuristic, surgery, scheduling',
	packages=find_packages(),
	install_requires=['']
)