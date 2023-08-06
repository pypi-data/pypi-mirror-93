import fnmatch
from setuptools import setup, find_packages
from Cython.Build import cythonize
from setuptools.command.build_py import build_py as build_py_orig
from setuptools.extension import Extension

ext_params = {
    'force': True,
    'compiler_directives': {
        'language_level': 3,
        'warn.unreachable': False
    }
}

extensions = [Extension('lime.lime_base', ['lime/lime_base.py']), Extension('lime.lime_tabular', ['lime/lime_tabular.py']), Extension('lime.lime_text', ['lime/lime_text.py']), Extension('lime.lime_image', ['lime/lime_image.py'])]

def not_cythonized(tup):
    (package, module, filepath) = tup
    return not any(
        fnmatch.fnmatchcase(filepath, pat=pattern) for ext in extensions for pattern in ext.sources
    )

class build_py(build_py_orig):
    def find_modules(self):
        modules = super().find_modules()
        return list(filter(not_cythonized, modules))

    def find_package_modules(self, package, package_dir):
        modules = super().find_package_modules(package, package_dir)
        return list(filter(not_cythonized, modules))


setup(name='lime',
      version='0.1.1.33',
      description='Local Interpretable Model-Agnostic Explanations for machine learning classifiers',
      url='http://github.com/marcotcr/lime',
      author='Marco Tulio Ribeiro',
      author_email='marcotcr@gmail.com',
      license='BSD',
      packages=find_packages(exclude=['js', 'node_modules', 'tests']),
      install_requires=[
          'numpy',
          'scipy',
          'scikit-learn>=0.18',
          'scikit-image>=0.12',
          'nltk'
      ],
      include_package_data=True,
      ext_modules=cythonize(extensions, **ext_params),
      cmdclass={'build_py': build_py})
