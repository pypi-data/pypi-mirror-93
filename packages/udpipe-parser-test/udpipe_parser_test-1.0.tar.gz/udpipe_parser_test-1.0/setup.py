import os
import setuptools

with open(r"C:\projects\udpipe_parser\README.txt") as readme_file:
    README = readme_file.read()

setuptools.setup(
     name='udpipe_parser_test',  
     version='1.0',
     license='MIT',
     author="Constantin Werner",
     author_email="const.werner@gmail.com",
     description="Analyzer brings Universal Dependencies trees in more practical form.",
     include_package_data=True,
     long_description=README,
     keywords=['analyzer', 'Universal Dependencies', 'NLP', 'russian','syntax'],
     url="https://github.com/constantin50/udpipe_analyzer",
     packages=setuptools.find_packages(),
     install_requires=["morpholog","conllu","separatrice","nltk"],
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )
