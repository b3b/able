import os
from pathlib import Path
from setuptools import setup, convert_path
from setuptools.command.install import install


main_ns = {}
with open(convert_path('able/version.py')) as ver_file:
    exec(ver_file.read(), main_ns)

with open(convert_path('README.rst')) as readme_file:
    long_description = readme_file.read()



class PathParser():

    @property
    def javaclass_dir(self):
        path = self.build_dir / 'javaclasses'
        if not path.exists():
            raise Exception(
                'Java classes directory is not found. '
                'Please report issue to: https://github.com/b3b/able/issues'
            )
        path = path / self.distribution_name
        path.mkdir(parents=True, exist_ok=True)
        return path

    @property
    def distribution_name(self):
        path = self.python_path
        while path.parent.name != 'python-installs':
            if len(path.parts) <= 1:
                raise Exception(
                    'Distribution name is not found. '
                    'Please report issue to: https://github.com/b3b/able/issues'
                    )
            path = path.parent
        return path.name

    @property
    def build_dir(self):
        return self.python_installs_dir.parent

    @property
    def python_installs_dir(self):
        path = self.python_path.parent
        while path.name != 'python-installs':
            if len(path.parts) <= 1:
                raise Exception(
                    'Python installs directory is not found. '
                    'Please report issue to: https://github.com/b3b/able/issues'
                    )
            path = path.parent
        return path

    @property
    def python_path(self):
        return Path(os.environ['PYTHONPATH'].split(':')[-1])



class InstallRecipe(install):
    """Command to install `able` recipe,
    copies Java files to distribution `javaclass` directory."""

    def run(self):
        if 'ANDROIDAPI' not in os.environ:
            raise Exception(
                'This recipe should not be installed directly, '
                'only with the buildozer tool.'
            )

        # Find Java classes target directory from the environment
        javaclass_dir = str(PathParser().javaclass_dir)

        self.distribution.data_files = [
            (javaclass_dir, [
                'able/src/org/able/BLE.java',
                'able/src/org/able/BLEAdvertiser.java',
                'able/src/org/able/PythonBluetooth.java',
                'able/src/org/able/PythonBluetoothAdvertiser.java',
            ]),
        ]

        install.run(self)


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
    project_urls={
        'Changelog': 'https://github.com/b3b/able/blob/master/CHANGELOG.rst',
    },
    # https://pypi.org/classifiers/
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Android',
        'Topic :: System :: Networking',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    keywords='android ble bluetooth kivy',
    license='MIT',
    zip_safe=False,
    cmdclass={
        'install': InstallRecipe,
    },
)
