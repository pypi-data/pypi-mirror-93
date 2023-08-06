import setuptools

INSTALL_REQUIRES = ["scrapinghub==2.3.1", "msgpack-python==0.5.6", "msgpack==1.0.2"]

setuptools.setup(
    name="flask-scrapinghub",
    version="0.0.6",
    author="chienaeae",
    authror_email="chienaeae@gmail.com",
    description="python-scrapinghub with flask",
    long_description=
    '''
    # ALPHA version
    
    python-scrapinghub with flask
    ''',
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=INSTALL_REQUIRES,
    python_requires='>=3.6',
)
