"""
Android Bluetooth Low Energy
"""
from pythonforandroid.recipe import PythonRecipe
from pythonforandroid.toolchain import current_directory, info, shprint
import sh
from os.path import join


class AbleRecipe(PythonRecipe):
    version = 'master'
    url = 'https://github.com/b3b/able/archive/{version}.zip'
    name = 'able'
    depends = [('python2', 'python3crystax'), 'setuptools', 'android']
    call_hostpython_via_targetpython = False
    install_in_hostpython = True

    def postbuild_arch(self, arch):
        super(AbleRecipe, self).postbuild_arch(arch)
        info('Copying able java class to classes build dir')
        with current_directory(self.get_build_dir(arch.arch)):
            shprint(sh.cp, '-a', join('able', 'src', 'org'),
                    self.ctx.javaclass_dir)


recipe = AbleRecipe()
