from setuptools import setup


with open('README.md') as readme_file:
    readme = readme_file.read()
    
    
setup(
      name="evpy", 
      version="1.0.3",
      description="A python package modeling electric power train components.",
      author="Dalton Chancellor",
      long_description=readme,
      license="MIT",
      packages=["evpy_"],
      include_package_data=True,
      install_requires=["numpy","scipy"],
      entry_points={
          "console_scripts": [
              "evpy.motor_pred=evpy_.evpy:motor_pred",
              ]
          },
      )

      
      
     