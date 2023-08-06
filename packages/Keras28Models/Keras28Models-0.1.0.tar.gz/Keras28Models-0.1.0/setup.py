import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Keras28Models", # Replace with your own username
    version="0.1.0",
    license='MIT',
    author="Falahgs.G.Saleih",
    author_email="falahgs07@gmail.com",
    description="All Traditional Classification Models ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/falahgs/",
    packages=setuptools.find_packages(),
    keywords = ['Keras', 'Tensorflow', 'Classification'],   # Keywords that define your package best
    install_requires=[ 'keras','tensorflow==2.2.0','pandas','numpy' ],
    classifiers=["Programming Language :: Python :: 3","License :: OSI Approved :: MIT License","Operating System :: OS Independent",],
    python_requires='>=3.6',)