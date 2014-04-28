from setuptools import setup, find_packages

version = '0.3'

setup(
	name='ckanext-realtime',
	version=version,
	description="CKAN extension which enables CKAN to serve realtime data",
	long_description=open('README.rst').read(),
	classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
	keywords='',
	author='Justas Azna',
	author_email='justas.azna@gmail.dk',
	url='',
	license='AGPL',
	packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
	namespace_packages=['ckanext', 'ckanext.realtime'],
	include_package_data=True,
	zip_safe=False,
	tests_require=[
			'nose',
	],
	test_suite = 'nose.collector',
	install_requires=[
		# -*- Extra requirements: -*-
	],
	entry_points=\
	"""
        [ckan.plugins]
    realtime=ckanext.realtime.plugin:RealtimePlugin
	""",
)
