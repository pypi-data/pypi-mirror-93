from setuptools import setup, find_packages

setup(name="message_server_tchka",
      version="1.0.0",
      description="OneMore Message Server",
      author="Elena Nikolaeva",
      author_email="tchka777@gmail.com",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
