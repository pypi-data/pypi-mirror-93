import setuptools

setuptools.setup(
    name="easy-host",
    version="0.0.2",
    author="toor",
    author_email="sh9901@163.com",
    description="",
    long_description="",
    url="https://pypi.org/project/ease-host/",
    packages=['src'],
    include_package_data=True,
    data_files=[('files', ['resources/auto-test-demo.zip',
                           'resources/httprunner2-demo.zip',
                           'resources/pytest-data-extract.zip',
                           'resources/apidoc-example.zip',
                           'resources/cmder.zip'])],
    install_requires=[],
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
