import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name = "automl-lib",
    version = "0.0.1",
    author = "pig_zhu",
    author_email = "zhipeng875820@163.com",
    description = "automl fm dnn deepFM in config file",
    long_description = long_description,
    long_description_content_type='text/markdown',
    python_requires=">=3.6",
    packages = setuptools.find_packages(),
    
    install_requires = ["tensorflow==1.15.0", "pyyaml", "sklearn"],
    
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    
)

