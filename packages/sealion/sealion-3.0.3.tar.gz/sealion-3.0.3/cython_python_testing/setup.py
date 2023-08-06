from Cython.Build import cythonize
from setuptools import setup, Extension
import numpy



'''Extension("cython_decision_tree_functions", ["cython_decision_tree_functions.pyx"],
              include_dirs =  [numpy.get_include()]),
    Extension("cython_tsne", ["cython_tsne.pyx"],
              include_dirs =  [numpy.get_include()]),
    Extension("cython_unsupervised_clustering", ["cython_unsupervised_clustering.pyx"],
              include_dirs =  [numpy.get_include()]),
    Extension("cython_naive_bayes", ["cython_naive_bayes.pyx"],
              include_dirs =  [numpy.get_include()]),
    Extension("cython_tsne", ["cython_tsne.pyx"],
              include_dirs =  [numpy.get_include()]),
    Extension("cython_knn", ["cython_knn.pyx"],
              include_dirs = [numpy.get_include()]),'''
extensions = [
    Extension("cython_ensemble_learning", ["/Users/anish/Documents/PycharmProjects/playProject/venv/sealion/cython_ensemble_learning.pyx"],
              include_dirs = [numpy.get_include()]),
]

setup(ext_modules=cythonize(extensions))
