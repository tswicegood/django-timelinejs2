from distutils.core import setup
import os

# Stolen from django-registration
# Compile the list of packages available, because distutils doesn't have
# an easy way to do this.
packages, data_files = [], []
root_dir = os.path.dirname(__file__)
if root_dir:
    os.chdir(root_dir)

for dirpath, dirnames, filenames in os.walk('timelinejs'):
    # Ignore dirnames that start with '.'
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.'):
            del dirnames[i]
    if '__init__.py' in filenames:
        pkg = dirpath.replace(os.path.sep, '.')
        if os.path.altsep:
            pkg = pkg.replace(os.path.altsep, '.')
        packages.append(pkg)
    elif filenames:
        prefix = dirpath[len('timelinejs/'):]
        for f in filenames:
            data_files.append(os.path.join(prefix, f))


setup(
    name='django-timelinejs2',
    version='2.18.2alpha',
    description='Connecting Timeline.js v2.18 to Django',
    author='Travis Swicegood',
    author_email='development@domain51.com',
    url='https://github.com/tswicegood/django-timelinejs2/',
    install_requires=[
        'django-staticfiles-timelinejs_static==2.18',
        'python-dateutil>=1.5',
    ],
    packages=packages,
    package_data={'timelinejs': data_files},
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
)
