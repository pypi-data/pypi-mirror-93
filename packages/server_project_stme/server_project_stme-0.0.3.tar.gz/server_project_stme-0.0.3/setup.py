from setuptools import setup, find_packages

setup(name="server_project_stme",
      version="0.0.3",
      description="mess_server_proj",
      author="Aleksey Prygin",
      author_email="jc@bu.ddha",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
