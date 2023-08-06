from distutils.core import setup
setup(
  name = 'nextgentermux',
  packages = ['nextgentermux'],
  version = '1.2',
  license='gpl-3.0', 
  description = 'An one tap termux setup tool',
  author = 'Sowmik',              
  author_email = 'xowmik@gmail.com',     
  url = 'https://github.com/Ign0r3dH4x0r/NextGenTermux',
  download_url = 'https://github.com/smsowmik/NextGenTermux/archive/1.1.tar.gz',
  keywords = ['Xowmik', 'Ign0r3dH4x0r', 'Termux'],
  install_requires=[     
          'lolcat',
      ],
  classifiers=[
    'Development Status :: 5 - Production/Stable',    
    'Intended Audience :: Developers', 
    'Topic :: Adaptive Technologies',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Programming Language :: Unix Shell',  
  ],
)
