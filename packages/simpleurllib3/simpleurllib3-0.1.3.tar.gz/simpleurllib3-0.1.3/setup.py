"""
setup.py
"""
import setuptools

setuptools.setup(
    name='simpleurllib3',
    version='0.1.3',
    author='TriC',
    py_modules=["simpleurllib3"],
    description='Easy to use urllib3 simplifier.',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>= 3.6',
    keywords=['urllib3', 'requests', 'simple', 'http'],
    include_package_data=True,
    install_requires=['urllib3', 'certifi', 'luddite']
)
