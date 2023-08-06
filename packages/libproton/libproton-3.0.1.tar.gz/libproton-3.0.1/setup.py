from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = f.read()

setup(
    name="libproton",
    version="3.0.1",
    url='https://github.com/PeterJCLaw/libproton',
    project_urls={
        'Issue tracker': 'https://github.com/PeterJCLaw/libproton/issues',
    },

    packages=find_packages(),

    description="Proton-compliant match scorer library.",
    long_description=long_description,
    long_description_content_type='text/markdown',

    author="Peter Law",
    author_email="PeterJCLaw@gmail.com",

    install_requires=[
        'PyYAML >=3.11, <5',
    ],
    license='MIT',

    tests_require=[
        'nose >=1.3, <2',
        'mock >=1.0.1, <2',
    ],
    test_suite='nose.collector',

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],

    zip_safe=True,
)
