import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open('requirements.txt', 'r', encoding='utf-8') as f:
    string = f.read()
    reequirements = list(filter(None, string.split("\n")))


setuptools.setup(
    name='mysqlsheet',
    version='1.0.0',
    author='Sachin Chavan',
    author_email='sachinewx@gmail.com',
    description='Push Big XL sheet in MySQL database table',
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords='MySQL xlsheet xlsx BigFile',
    url="https://github.com/sachinchavan9/mysqlsheet",
    packages=setuptools.find_packages(),
    install_requires=reequirements,
    entry_points={
        'console_scripts': ['mysqlsheet=mysqlsheet.mysqlsheet:main'],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Information Technology",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Topic :: Database",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
    ],
    python_requires='>=3.7',
    include_package_data=True,
    zip_safe=False
)
