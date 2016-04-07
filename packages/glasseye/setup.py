from setuptools import setup

setup(
    name='lektor-glasseye',
    version='0.1',
    author=u'James Webber',
    author_email='jamestwebber@gmail.com',
    license='MIT',
    py_modules=['lektor_glasseye'],
    entry_points={
        'lektor.plugins': [
            'glasseye = lektor_glasseye:GlasseyePlugin',
        ]
    }
)
