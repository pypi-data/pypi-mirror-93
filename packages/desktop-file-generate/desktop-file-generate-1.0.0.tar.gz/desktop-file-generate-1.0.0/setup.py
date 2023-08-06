from setuptools import setup, find_packages

setup(
    name='desktop-file-generate',
    version='1.0.0',
    author='fncong',
    author_email='fncong@outlook.com',
    packages=find_packages(),
    description='生成.desktop文件',
    url='https://github.com/fncong',
    entry_points={'console_scripts': ['desktop-file = desktop_file.desktop_file:main']}
)
