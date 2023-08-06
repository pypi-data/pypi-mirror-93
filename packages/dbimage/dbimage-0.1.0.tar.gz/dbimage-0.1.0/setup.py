from setuptools import setup

setup(name='dbimage',
      version='0.1.0',
      description='dtoolbioimage image format',
      packages=['dbimage'],
      url='https://github.com/JIC-Image-Analysis/dbimage',
      author='Matthew Hartley',
      author_email='Matthew.Hartley@jic.ac.uk',
      license='MIT',
      install_requires=[
	      "click",
        "numpy",
        "blosc",
        "tifffile"
      ],
      entry_points='''
        [console_scripts]
        tiff2dbim=dbimage.convert:convert_tif_image
        dbim_info=dbimage.info:dbim_info
      ''',
      zip_safe=False)
