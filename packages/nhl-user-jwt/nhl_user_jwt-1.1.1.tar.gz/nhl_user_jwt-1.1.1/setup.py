from setuptools import setup, find_packages

setup(
    name="nhl_user_jwt",
    version="1.1.1",
    author="ligo",
    author_email="ligocz@dingtalk.com",
    description="jwt生成和验签",
    url="https://www.nihuola.vip/",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=[
        'python-jose>=3.2.0',
        'passlib>=1.7.4',
        'redis>=3.5.2'
    ]
)


