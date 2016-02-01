from distutils.core import setup
import py2exe, sys, os
sys.setrecursionlimit(5000)
sys.argv.append('py2exe')

setup(windows=[{'script': 'nc_calculator_latex.py', "icon_resources": [(1, "latex.ico")]}], \
            options={"py2exe": {"includes": ["decimal", "Tkinter", \
            "tkFileDialog", "csv", "xml.dom.minidom", "os"], \
            'bundle_files': 1, 'compressed': False}}, \
            zipfile = None)