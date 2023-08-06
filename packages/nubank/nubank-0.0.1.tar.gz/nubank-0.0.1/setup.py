from setuptools import setup

with open('README.md','r') as file:
    long_description=file.read()
    
setup(
       name='nubank',
       version='0.0.1',
       description="This package provides some bank functions",
       py_modules=["deposit_amount","home_loan","personal_loan","vehicle_loan","withdraw_amount"],
       package_dir={'':'nubank'},
       

      classifers=[
                "Programming Language :: Python :: 3",
                "Programming Language :: Python :: 3.6",
                "Programming Language :: Python :: 3.7",
                "Programming Language :: Python :: 3.9",

                "License :: OSI Approved  :: GNU General Public License v2 or later (GPLv2+)",
                "Operating System :: OS Independent",

                
          ],

       long_description=long_description,
       long_description_content_type="text/markdown",


       install_requires=[

                  "django~=3.1.5",
                

           ],

       extras_requires={

                  "dev":['pytest>=3.7',
                        ],
           },

       url='https://github.com/naga99552/publish/nubank',
       author="Nagababu",
       author_email="nagababuupputuri52@gmail.com",
    )
