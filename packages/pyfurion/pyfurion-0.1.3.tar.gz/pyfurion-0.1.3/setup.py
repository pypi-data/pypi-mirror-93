from setuptools import setup

'''
pip install wheel
python setup.py bdist_wheel
pip install twine
twine upload dist/*
'''

setup(
    # 以下为必需参数
    name='pyfurion',  # 模块名
    version='0.1.3',  # 当前版本
    description='A furion client for Python',  # 简短描述
    # py_modules=["pyfurion"],  # 单文件模块写法
    packages=['pyfurion'],

    # 以下均为可选参数
    long_description="",  # 长描述
    url='https://github.com',  # 主页链接
    author='zhangguanqun',  # 作者名
    author_email='zhanguanqunart@163.com',  # 作者邮箱
    classifiers=[
        "Development Status :: 5 - Production/Stable",

        'Intended Audience :: Developers',  # 模块适用人群
        'Topic :: Software Development :: Build Tools',  # 给模块加话题标签

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3.6',
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    keywords='furion client python',  # 模块的关键词，使用空格分割
    install_requires=['kazoo'],  # 依赖模块
    extras_require={  # 分组依赖模块，可使用pip install sampleproject[dev] 安装分组内的依赖
    },
    package_data={  # 模块所需的额外文件
    },
    data_files=[],  # 类似package_data, 但指定不在当前包目录下的文件
    project_urls={  # 项目相关的额外链接
        'Source': 'https://github.com',
    },
)
