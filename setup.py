from setuptools import setup, find_packages

setup(
    name='pyqt-file-list-widget',
    version='0.0.2',
    author='Jung Gyu Yoon',
    author_email='yjg30737@gmail.com',
    license='MIT',
    packages=find_packages(),
    description='PyQt QListWidget for files (being able to drop the files based on user-defined extensions)',
    url='https://github.com/yjg30737/pyqt-file-list-widget.git',
    install_requires=[
        'PyQt5>=5.8',
        'pyqt-show-long-text-as-tooltip-list-widget @ git+https://git@github.com/yjg30737/pyqt-show-long-text-as-tooltip-list-widget.git@main',
        'pyqt-files-already-exists-dialog @ git+https://git@github.com/yjg30737/pyqt-files-already-exists-dialog.git@main'
    ]
)