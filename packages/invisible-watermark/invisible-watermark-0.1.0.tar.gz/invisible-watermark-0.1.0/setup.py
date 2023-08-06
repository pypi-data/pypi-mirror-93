import setuptools


with open('README.md', 'r') as f:
  long_description = f.read()

setuptools.setup(
  name='invisible-watermark',
  version='0.1.0',
  author='Qingquan Wang',
  description='The library for creating and decoding invisible image watermarks',
  long_description=long_description,
  long_description_content_type='text/markdown',
  url='https://github.com/ShiedMnt/invisible-watermark',
  packages=setuptools.find_packages(),
  install_requires=[
      'opencv-python>=4.1.0.25',
      'torch==1.0.1.post2',
      'torch-dct==0.1.5',
      'pandas>=0.25,<0.26',
      'numpy>=1.17.3,<2',
      'Pillow>=6.0.0',
      'PyWavelets>=1.1.1',
      'numpy>=1.17.0'
  ],
  scripts=['invisible-watermark'],
  classifiers=[
      'Programming Language :: Python :: 3',
      'License :: OSI Approved :: MIT License',
      'Operating System :: POSIX :: Linux',
  ],
  # Python 3.6 tested in Ubuntu 18.04 LTS.
  python_requires='>=3.6',
)
