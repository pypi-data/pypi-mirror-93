from setuptools import setup

with open("/home/barbasan/Documents/bddkalpha/README.md","r") as mdfile:
    descr = mdfile.read()

setup(
    name="bddk",
    version="1.0",
    description="Bddk Veri",
    py_modules=["bddk"],
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
	"License :: OSI Approved :: MIT License",
	"Development Status :: 4 - Beta",
	"Operating System :: Microsoft :: Windows",
	"Operating System :: MacOS",
	"Operating System :: POSIX :: Linux",
	"Intended Audience :: Financial and Insurance Industry"
    ],
    long_description_content_type="text/markdown",
    long_description=descr,
    install_requires=[
        "pandas",
        "openpyxl",
        "selenium",
        "urllib3",
        "requests"
    ],
    url="https://github.com/barbasan/bddk",
    author="Ilyas Burak Hizarci",
    author_email="i.burakhizarci@gmail.com"
)
