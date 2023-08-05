from setuptools import setup, find_packages

setup(
    name="grpc-extensions",
    version="0.0.1",
    python_requires='>=3.7.9',
    description="python grpc library",
    long_description="python grpc library",
    license="MIT Licence",
    url="",
    author="haoyinqianzui",
    author_email="810909753@qq.com",
    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=["grpcio>=1.32.0"],
)
