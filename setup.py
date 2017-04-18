from setuptools import setup, convert_path

main_ns = {}
ver_path = convert_path('able/version.py')
with open(ver_path) as ver_file:
    exec(ver_file.read(), main_ns)


setup(
    name='able',
    version=main_ns['__version__'],
    packages=['able', 'able.android'],
    description='Bluetooth Low Energy for Android',
    license='MIT',
)
