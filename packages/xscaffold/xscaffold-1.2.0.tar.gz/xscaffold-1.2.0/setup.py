from setuptools import setup

setup(
    name="xscaffold",
    version="1.2.0",
    install_requires=[
        'PyYaml',
        'jinja2'
    ],
    author = "Dan Clayton",
    author_email = "dan@azwebmaster.com",
    description = "Used to scaffold a project.",
    license = "MIT",
    keywords = "scaffold",
    url = "https://github.com/azweb76/x-scaffold",
    packages=['xscaffold'],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'xscaffold=xscaffold.xscaffold:main',
        ],
    },
)
