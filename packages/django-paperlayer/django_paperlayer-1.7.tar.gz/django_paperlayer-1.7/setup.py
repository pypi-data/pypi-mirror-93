from setuptools import setup, find_packages

setup(
  name = 'django_paperlayer',         # How you named your package folder (MyLib)
  packages = ['django_paperlayer',
              'django_paperlayer.api',
              'django_paperlayer.api.migrations',
              'django_paperlayer.api.models',
              'django_paperlayer.api.serializers',
              'django_paperlayer.api.views',
              'django_paperlayer.backend'
              ],   # Chose the same as "name"
  version = '1.7',      # Start with a small number and increase it with every change you make
  license= 'MIT License',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'An simple academic platform',   # Give a short description about your library
  author = 'Paperlayer Dev Team',                   # Type in your name
  author_email = 'bounswe2020group3@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/bounswe/bounswe2020group3',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/bounswe/bounswe2020group3/archive/2.2.1.tar.gz',    # I explain this later on
  python_requires='>=3.6',
  install_requires=[            # I get to this in a second
      'Django>=3.1.3',
      'bandit>=1.6.2',
      'djangorestframework>=3.12.2',
      'drf-yasg>=1.20.0',
      'django-password-reset>=2.0',
      'gunicorn>=20.0.4',
      'django-filter>=2.4.0',
      'django-cors-headers>=3.5.0',
      'Pillow>=8.0.1',
      'python-datamuse>=1.3.0'
      'django-storages>=1.11.1',
      'boto3>=1.16.43',
      'django-email-verification>=0.0.7',
      'django-notifications-hq>=1.6.0',
      'sendgrid>=6.4.8',
      'stream-python>=5.0.0',
      'scholarly>=1.0.3'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.9',
  ],
)