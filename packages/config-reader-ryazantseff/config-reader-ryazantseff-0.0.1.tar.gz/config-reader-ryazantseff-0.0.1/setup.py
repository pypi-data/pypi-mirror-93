import pathlib
import setuptools

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setuptools.setup(
    name="config-reader-ryazantseff",
    version="0.0.1",
    description="Json config reader and writer",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/ryazantseff/py-config-reader",
    author="Maxim Ryazantsev",
    author_email="maxim.ryazancev@gmail.com",
    license="MIT",
    keywords = ['JSON', 'Config'],   
    install_requires=[
        'pathlib',
    ],
    packages=setuptools.find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',      
        'Intended Audience :: Developers',      
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',   
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
