import os
from os.path import dirname
from setuptools import setup, convert_path


main_ns = {}
with open(convert_path('able/version.py')) as ver_file:
    exec(ver_file.read(), main_ns)

with open(convert_path('README.rst')) as readme_file:
    long_description = readme_file.read()


if 'ANDROIDAPI' not in os.environ:
    raise Exception(
        'This recipe should not be installed directly, '
        'only with the buildozer tool.'
    )

# Find Java classes target directory from the environment
distribution_dir = os.environ['PYTHONPATH'].split(':')[-1]
distribution_name = distribution_dir.split('/')[-1]
javaclass_dir = os.path.join(dirname(dirname(distribution_dir)), 'javaclasses')

if not os.path.exists(javaclass_dir):
    raise Exception(
        'javaclasses directory is not found. '
        'Please report issue  to: https://github.com/b3b/able/issues'
    )

javaclass_dir = os.path.join(javaclass_dir, distribution_name, 'org', 'able')
if not os.path.exists(javaclass_dir):
    os.makedirs(javaclass_dir)


setup(
    name='able_recipe',
    version=main_ns['__version__'],
    packages=['able', 'able.android'],
    description='Bluetooth Low Energy for Android',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    author='b3b',
    author_email='ash.b3b@gmail.com',
    install_requires=[],
    url='https://github.com/b3b/able',
    # https://pypi.org/classifiers/
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Android',
        'Framework :: Kivy',
        'Topic :: System :: Networking',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    keywords='android ble bluetooth kivy',
    license='MIT',
    zip_safe=False,
    data_files=[
         (javaclass_dir, [
             'able/src/org/able/BLE.java',
             'able/src/org/able/PythonBluetooth.java',
         ]),
    ],
)
