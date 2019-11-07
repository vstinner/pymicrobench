def main():
    from setuptools import setup

    options = {
        'name': 'pymicrobench',
        'version': '0.0',
        'license': 'MIT license',
        'description': 'CPython microbenchmarks',
        'url': 'https://github.com/vstinner/pymicrobench',
        'author': 'Victor Stinner',
        'author_email': 'victor.stinner@gmail.com',
        'install_requires': ["pyperf"],
    }
    setup(**options)


if __name__ == '__main__':
    main()
