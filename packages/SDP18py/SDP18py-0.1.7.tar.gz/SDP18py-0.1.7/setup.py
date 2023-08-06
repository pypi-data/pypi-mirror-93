from setuptools import setup, find_packages
import os

classifiers = [
	'Development Status :: 5 - Production/Stable',
	'Intended Audience :: Education',
	'Operating System :: Microsoft :: Windows :: Windows 10',
	'License :: OSI Approved :: MIT License',
	'Programming Language :: Python :: 3'
]


thelibFolder = os.path.dirname(os.path.realpath(__file__))
requirementPath = thelibFolder + '/requirements.txt'
install_requires = [] # Examples: ["gunicorn", "docutils>=0.3", "lxml==0.5a7"]
if os.path.isfile(requirementPath):
    with open(requirementPath) as f:
        install_requires = f.read().splitlines()

setup(
	name='SDP18py',
	version='0.1.7',
	description='This package schedules surgeries using metaheurisitcs. It is a project done for in NUS for Systems Design Project (SDP):Metaheuristic Surgery Scheduling for Operating Theatre Scheduling',
	long_description=open('README.md').read(),
	url='https://github.com/lwq96/NewProject',
	author='SDP18',
	author_email='e0176071@u.nus.edu',
	license='MIT',
	classifiers=classifiers,
	keywords='metaheuristic, surgery, scheduling',
	packages=find_packages(),
	install_requires=install_requires
)