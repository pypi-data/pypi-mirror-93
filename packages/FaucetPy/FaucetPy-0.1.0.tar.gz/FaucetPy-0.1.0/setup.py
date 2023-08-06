from setuptools import setup

setup(
	name='FaucetPy',
	version='0.1.0',
	description='FaucetPay + Python = FaucetPy',
	url='https://github.com/HanzHaxors/FaucetPy',
	author='HanzHaxors',
	author_email='hanzhaxors@gmail.com',
	license='BSD 2-clause',
	packages=['FaucetPy'],
	install_requires=[
		'requests==2.25.1'
	],
	classifiers=[
		'License :: OSI Approved :: BSD License',
	        'Operating System :: POSIX :: Linux',
		'Intended Audience :: Developers',
		'Intended Audience :: Financial and Insurance Industry'
	]
)
