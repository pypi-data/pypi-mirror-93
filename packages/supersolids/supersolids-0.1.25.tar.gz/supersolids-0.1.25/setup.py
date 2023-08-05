from setuptools import setup
# from Cython.Build import cythonize
# To compile: python setup.py build_ext --inplace

# create a source distribution and a wheel with python setup.py sdist bdist_wheel
# To upload to TestPyPi python -m twine upload --repository testpypi dist/*

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="supersolids",
    version="0.1.25",
    packages=["", "supersolids"],
    package_data={"supersolids": []},
    url="https://github.com/Scheiermann/supersolids",
    license="MIT",
    author="Scheiermann",
    author_email="daniel.scheiermann@stud.uni-hannover.de",
    install_requires=["ffmpeg-python",
                      "matplotlib",
                      "numpy",
                      "mayavi",
                      "psutil",
                      "scipy",
                      "sphinx-autoapi",
                      "sphinx-rtd-theme",
                      ],
    # ext_modules=cythonize("*.pyx", language_level=3),
    python_requires=">=3.6",
    description="simulate and animate supersolids.",
    long_description=long_description,
    long_description_content_type="text/markdown"
)
