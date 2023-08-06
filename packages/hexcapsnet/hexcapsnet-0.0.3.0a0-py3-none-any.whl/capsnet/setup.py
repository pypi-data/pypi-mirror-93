from setuptools import setup, find_packages

setup(name='hexcapsnet',
      version='0.0.3.0-alpha',
      description='Libs capsnets',
      long_description='Libs capsnets',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6'
      ],
      keywords='capsnet ai classification',
      url='',
      author='Vladislav Ovchinnikov',
      author_email='vladovchinnikov950@gmail.com',
      license='MIT',
      packages=find_packages(),
      install_requires=[
          'tensorflow==2.3.0',
          'keras'
      ],
      include_package_data=True,
      zip_safe=False)