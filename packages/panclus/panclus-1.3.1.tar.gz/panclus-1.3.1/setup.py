import setuptools
from setuptools import setup 

# reading long description from file 
with open('README.md') as file: 
	long_description = file.read() 


# specify requirements of your package here 
REQUIREMENTS = ['ephem','wikipedia','pyttsx3','datetime','pyperclip','translate'] 

# some more details 
CLASSIFIERS = [ 
	'Development Status :: 4 - Beta', 
	'Intended Audience :: Developers', 
	'Topic :: Internet', 
	'License :: OSI Approved :: MIT License', 
	'Programming Language :: Python', 
	'Programming Language :: Python :: 3', 
	'Programming Language :: Python :: 3.3', 
	'Programming Language :: Python :: 3.4', 
	'Programming Language :: Python :: 3.5', 
	] 

# calling the setup function 
setup(name='panclus', 
	version='1.3.1', 
	description='A useful module to convert speech to text calculating solar and lunar eclipse as well as translating text in very short lines of code.', 
	long_description=long_description, 
	url='https://github.com/Ayush2007A/Code-master/blob/main/Panclus.py', 
	author='Ayush Moghe', 
	author_email='mogheayushgr8@gmail.com', 
	license='MIT',
        packages=setuptools.find_packages(),
        include_package_data=True,
	classifiers=CLASSIFIERS, 
	install_requires=REQUIREMENTS, 

	) 
