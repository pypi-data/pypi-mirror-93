from setuptools import find_packages, setup
import covpipe.__version__ as vers

setup(
    name='covpipe',
    packages=find_packages(include=["covpipe", "covpipe_tools"]),
    version=vers.VERSION,
    description='Sars-Cov-2 NGS Pipline for generating consensus sequences',
    tests_require=["pytest","PyYAML", "pandas"],
    install_requires=[
        "snakemake>5.26",
        "strictyaml",
        "PyYAML",
        "biopython",
        "pysam",
        "pandas",
        "numpy"],
    entry_points={
        "console_scripts":[
            'covpipe = covpipe.ncov_minipipe:main',
            'ncov_minipipe = covpipe.ncov_minipipe:main', 
            'create_bedpe = covpipe_tools.create_bedpe:main',
            'create_pangolin = covpipe_tools.update_pangolin:main'
        ]},
    include_package_data = True,
    package_data={
        "covpipe":[
            "covpipe/ncov_minipipe.snake",
            "covpipe/ncov_minipipe.Rmd",
            "covpipe/ncov_minipipe.config",
            "covpipe/rules/*.smk",
            "covpipe/scripts/*",
            "covpipe_tools/*.py",
            "covpipe/data/*"]
        },
    #scripts=["scripts/swrap-quicksetup"],
    author='René Kmiecinski',
    author_email="r.w.kmiecinski@gmail.com",
    license='GPL-v3'
)


