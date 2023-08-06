from setuptools import setup, find_packages

setup(name="mess_server_amk",
      version="0.0.1",
      description="mess_server_amk",
      author="Kolotov Alexander",
      author_email="amk@yandex.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
