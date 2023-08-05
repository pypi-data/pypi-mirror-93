import setuptools

setuptools.setup(
    name="w3h",  # Replace with your own username
    version="0.0.7",
    packages=['w3h'],
    package_dir={'w3h': 'w3h'},
    package_data={'w3h': ['*.json']},
    python_requires='>=3.9',
    )
