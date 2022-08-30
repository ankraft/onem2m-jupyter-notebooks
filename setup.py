from setuptools import setup, find_packages

setup(
	name='oneM2M-jupyter-notebooks',
	version='1.3.0',
	url='https://github.com/ankraft/onem2m-jupyter-notebooks',
	author='Andreas Kraft',
	author_email='an.kraft@gmail.com',
	description='A couple of Jupyter notebooks to explain how to create, access and manage oneM2M resources',
	packages=find_packages(),
	install_requires=[
		'jupyter',
		'jupyterlab',
		'cbor2',
		'flask',
		'InquirerPy',
		'isodate', 
		'paho-mqtt',
		'plotext',
		'requests', 
		'rich', 
		'tinydb'
	 ]
)
