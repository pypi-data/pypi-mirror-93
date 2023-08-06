from setuptools import setup, find_packages

setup(name="mess_server_kindly",
      version="0.0.1",
      description="mess_server_proj",
      author="Eugene Filippov",
      author_email="kindlyhickory@gmail.com",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
