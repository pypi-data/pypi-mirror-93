from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

setup_args = dict(
    name='shopcloud_metric',
    version='0.2.0',
    description='CLI tool for Metrics',
    long_description_content_type="text/markdown",
    long_description=README,
    license='MIT',
    packages=find_packages(),
    author='Konstantin Stoldt',
    author_email='konstantin.stoldt@talk-point.de',
    keywords=['CLI'],
    url='https://github.com/Talk-Point/shopcloud-infrastructure-cli',
    scripts=['./scripts/metric'],
)

install_requires = [
    'requests',
    'shopcloud_secrethub'
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)