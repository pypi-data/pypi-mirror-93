from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Operating System :: POSIX :: Linux',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='ssm_mass_uploader',
    version='0.0.1',
    description='You pass in a encrypted file and kms key id, the package will decrypt the data, and upload the contents to aws ssm.',
    long_description=open('CHANGELOG.txt').read(),
    url='https://github.com/jayfry1077/ssm_mass_uploader',
    author='Jonathan Bradbury',
    author_email='jonathanabradbury@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='',
    packages=find_packages(),
    install_requires=['boto3']

)
