from setuptools import setup, find_packages

setup(
    name='GoogleLens',
    version='0.1.0',
    packages=find_packages(),
    author='Abol',
    author_email='abaqry8686@gmail.com',
    description='A library for interacting with the Aparat API',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/AbolDev/GoogleLens',
    license='MIT',
    install_requires=[
        'requests',
        'beautifulsoup4',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires='>=3.6',
    keywords = [
        'python', 'library', 'Google', 'Google-api', 'GoogleLens-api',
        'GoogleLens-lib', 'Google-lib', 'GoogleLens-python', 'Google-python'
    ],
    project_urls={
        'Bug Tracker': 'https://github.com/AbolDev/GoogleLens/issues',
        'Source Code': 'https://github.com/AbolDev/GoogleLens',
    },
)
