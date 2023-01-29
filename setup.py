from setuptools import find_packages, setup

setup(
    name='heflow',
    use_scm_version=True,
    description='HEflow: A platform for the homomorphic encryption lifecycle',
    long_description_content_type='text/markdown',
    author='InAccel',
    author_email='info@inaccel.com',
    url='https://github.com/inaccel/heflow',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    license='Apache-2.0',
    platforms=[
        'Linux',
    ],
    install_requires=[
        'mlserver-mlflow',
        'tenseal',
    ],
    entry_points={
        'console_scripts': [
            'heflow-keygen = heflow.cli.keygen:command',
        ],
    },
    python_requires='>=3.8',
)
