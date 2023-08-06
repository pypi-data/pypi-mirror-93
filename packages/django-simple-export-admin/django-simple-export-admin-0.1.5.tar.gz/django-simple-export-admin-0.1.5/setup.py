# -*- coding: utf-8 -*-
import os
from io import open
from setuptools import setup
from setuptools import find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, "README.md"), "r", encoding="utf-8") as fobj:
    long_description = fobj.read()

with open(os.path.join(here, "requirements.txt"), "r", encoding="utf-8") as fobj:
    requires = fobj.readlines()

setup(
    name="django-simple-export-admin",
    version="0.1.5",
    description="A simple django admin allow your export queryset to xlsx file.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="zencore",
    author_email="dobetter@zencore.cn",
    url="https://github.com/zencore-cn/zencore-issues",
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords=["django admin extentions", "django simple export admin"],
    install_requires=requires,
    packages=find_packages(".", exclude=["django_simple_export_admin_example", "django_simple_export_admin_example.migrations", "django_simple_export_admin_demo"]),
    py_modules=["django_simple_export_admin"],
    zip_safe=False,
    include_package_data=True,
)