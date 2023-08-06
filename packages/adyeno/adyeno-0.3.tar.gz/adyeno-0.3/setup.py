from setuptools import setup, find_packages


def readme():
    with open('README.md', 'r') as markdown:
        return markdown.read()


# Building the package

setup(
    name="adyeno",
    version='0.3',
    description='The adyeno is a live Adyen encryption lib.',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/DeveloperAdeel/adyeno',
    author='Adeel Khan',
    author_email='akodaos@gmail.com',
    keywords='adyeno, adk, exvous, palace, wrappers, automation',
    license='MIT',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    # package_data={'': ['adyeno/pytransform/*']},
    # include_package_data=True,
    zip_safe=False,
    install_requires=[
        'requests',
        'datetime',
        'pytz'
    ],
    python_requires='>=3.6',
)
