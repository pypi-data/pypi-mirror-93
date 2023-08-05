from setuptools import setup, Extension

setup(
    name='isnude',
    version='0.0.1',
    description="Nudity detection with re-trained Tensorflow MobileNet Model http://nudity.canaydogan.net",
    long_description=open('README.rst').read(),
    long_description_content_type="text/markdown",
    author='Dyas Yaskur',
    author_email='canaydogan89@gmail.com',
    url='https://github.com/dyaskur/nudity',
    license='MIT',
    packages=['isnude'],
    include_package_data=True,
    package_dir={'isnude': 'isnude'},
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ],
    keywords="nude, nudity, detection, pornographic, inappropriate content",
    install_requires=['tensorflow'],
    python_requires='>=3',
    entry_points={'console_scripts': ['isnude = isnude:main']}
)
