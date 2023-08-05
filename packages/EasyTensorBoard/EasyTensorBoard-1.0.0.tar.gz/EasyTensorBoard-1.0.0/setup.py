import setuptools

with open('README.md', 'r', encoding='utf-8') as fp:
    long_description = fp.read()

setuptools.setup(
    # 环境依赖（版本、包、文件<包:匹配>）
    python_requires='>=3',
    install_requires=[
        'tensorboard>=1.8.0'
    ],

    # 打包配置
    packages=setuptools.find_packages(),
    include_package_data=True,

    # 作者资料
    author="zhmh",
    author_email="zhmhbest@gmail.com",

    # 模块信息
    name="EasyTensorBoard",
    version="1.0.0",
    description="",
    keywords="",
    # https://choosealicense.com/
    license="MIT",
    url="",
    long_description=long_description,
    long_description_content_type="text/markdown",

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)