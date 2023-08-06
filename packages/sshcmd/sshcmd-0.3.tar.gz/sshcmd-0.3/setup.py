import setuptools
setuptools.setup(
    name="sshcmd", 
    packages=setuptools.find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    version="0.3",
    license='MIT',
    author="lxl",
    author_email="xliang.lee@qq.com",
    description="ssh cmd",
    long_description="ssh cmd",
    long_description_content_type="text/markdown",
    url="",
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
    ],
    keywords=['ssh', 'cmd'],
    python_requires='>=2.6',
    install_requires=[
        'paramiko',
    ],
 )

