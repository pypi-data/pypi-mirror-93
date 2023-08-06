from distutils.core import setup

setup(
    name='os_s3_handler',  # How you named your package folder (MyLib)
    packages=['os_s3_handler'],  # Choose the same as "name"
    version='1.00',  # Start with a small number and increase it with every change you make
    license='MIT',  # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description='This module meant to provide intuitive functions to work with AWS\'s S3',  # Give a short description about your library
    author='Oz Shabat',  # Type in your name
    author_email='os-apps@admin.com',  # Type in your E-Mail
    url='https://github.com/osfunapps/os-s3-handler-py',  # Provide either the link to your github or to your website
    keywords=['python', 'osfunapps', 'files', 'tools', 'utils', 'aws', 's3'],  # Keywords that define your package best
    install_requires=['os_tools'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',  # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package

        'Intended Audience :: Developers',  # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',

        'License :: OSI Approved :: MIT License',  # Again, pick a license
        'Programming Language :: Python :: 3',  # Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
