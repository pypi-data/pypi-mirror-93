from setuptools import setup
import os
base_dir = os.path.dirname(__file__)
with open(os.path.join(base_dir, "README.md")) as f:
    long_description = f.read()




setup(name='function_optimization' , version = '0.3'
        ,description = 'Optimize functions.Newton and Gradient descent methods', packages = ['optimization'], zip_safe = False,
        author = 'Mark Eltsefon', author_email = 'meltsefon1@gmail.com',long_description=long_description)
