import io

from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.readlines()

setup(
    name="depthai-gui",
    version="2.0.0",
    packages=['.'],
    entry_points={
        'console_scripts': [
            'depthai-gui = pipeline_editor:main',
            'depthai-gui-demo = demo:main'
        ]
    },
    author="Luxonis",
    long_description=io.open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author_email="support@luxonis.com",
    description="DepthAI Pipeline Visualizer GUI",
    keywords="depthai gui ide pipeline visualizer node",
    url="https://github.com/luxonis/depthai-gui",   # project home page
    project_urls={
        "Bug Tracker": "https://github.com/luxonis/depthai-gui/issues",
        "Documentation": "https://docs.luxonis.com/projects/gui/en/latest/",
        "Source Code": "https://github.com/luxonis/depthai-gui",
    },
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    install_requires=required,
)