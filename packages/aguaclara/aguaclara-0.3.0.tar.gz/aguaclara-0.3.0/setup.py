from setuptools import setup, find_packages

setup(
    name = 'aguaclara',
    version = '0.3.0',
    description = (
        'An open-source Python package for designing and performing research '
        'on AguaClara water treatment plants.'
    ),
    url = 'https://github.com/AguaClara/aguaclara',
    author = 'AguaClara Cornell',
    author_email = 'aguaclara@cornell.edu',
    license = 'MIT',
    packages = find_packages(),

    # Ensure that this matches Pipfile > [packages]
    install_requires = [
        'matplotlib',
        'urllib3',
        'pint',
        'pandas',
        'scipy',
        'onshape_client',
    ],

    python_requires='>=3.8',
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    include_package_data=True,
    test_suite="tests",
    zip_safe=False
)
# test
