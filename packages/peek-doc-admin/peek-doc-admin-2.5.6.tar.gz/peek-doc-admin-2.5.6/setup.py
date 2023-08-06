import os
import shutil
import subprocess
from subprocess import CalledProcessError

from setuptools import setup, find_packages

pip_package_name = "peek-doc-admin"
py_package_name = "peek_doc_admin"

package_version = '2.5.6'

egg_info = "%s.egg-info" % pip_package_name
if os.path.isdir(egg_info):
    shutil.rmtree(egg_info)

if os.path.isfile('MANIFEST'):
    os.remove('MANIFEST')

excludePathContains = ('__pycache__', 'node_modules', 'platforms', 'dist',
                       'doc_link', 'doc_dist', 'doc_dist_latex')
excludeFilesEndWith = ('.pyc', '.js', '.js.map', '.lastHash')
excludeFilesStartWith = ('peek_plugin',)


def find_package_files():
    paths = []
    for (path, directories, filenames) in os.walk(py_package_name):
        if [e for e in excludePathContains if e in path]:
            continue

        for filename in filenames:
            if [e for e in excludeFilesEndWith if filename.endswith(e)]:
                continue

            if [e for e in excludeFilesStartWith if filename.startswith(e)]:
                continue

            relPath = os.path.join(path, filename)
            try:
                subprocess.check_call(['git', 'check-ignore', '-q', relPath])

            except CalledProcessError:
                paths.append(relPath[len(py_package_name) + 1:])

    return paths


package_files = find_package_files()

requirements = [
    "sphinx",
    "sphinx-autobuild",
    "sphinx-rtd-theme"
]

setup(
    name=pip_package_name,
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    package_data={'': package_files},
    install_requires=requirements,
    zip_safe=False,
    version=package_version,
    description='Peek Platform - Admin Documentation (Frontend)',
    author='Synerty',
    author_email='contact@synerty.com',
    url='https://github.com/Synerty/%s' % pip_package_name,
    download_url='https://github.com/Synerty/%s/tarball/%s' % (
        pip_package_name, package_version),
    keywords=['Peek', 'Python', 'Platform', 'synerty'],
    classifiers=[
        "Programming Language :: Python :: 3.5",
    ],
)
