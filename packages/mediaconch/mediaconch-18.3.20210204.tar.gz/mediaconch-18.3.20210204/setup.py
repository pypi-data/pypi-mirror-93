import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mediaconch",
    version="18.03.20210204",
    license='BSD-2-Clause',
    author="MediaArea.Net",
    author_email="info@mediaarea.net",
    description="A python ctypes wrapper for mediaconch library.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MediaArea/MediaConch_SourceCode",
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha",
        "Operating System :: POSIX :: Linux",
        "Topic :: Multimedia"
    ],
    packages=['mediaconch'],
    package_data={
        'mediaconch': [
            'linux/x86_32/libmediaconch.so.0',
            'linux/x86_64/libmediaconch.so.0'
        ]
    },
    python_requires='>=3.0',
    include_package_data=True
)
