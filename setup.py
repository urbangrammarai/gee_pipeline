from setuptools import setup

with open("peep/requirements.txt", "r") as f:
    REQUIRED_PACKAGES = f.read().splitlines()

setup(
    name="peep",
    version="1.0",
    description="Google Earth Engine Pipelines.",
    url="https://github.com/urbangrammarai/gee_pipeline/",
    author="Camila Rangel Smith, Andy Smith, based on code from https://github.com/alan-turing-institute/monitoring-ecosystem-resilience",
    license="MIT",
    include_package_data=True,
    packages=["peep", "peep.src", "peep.scripts", "peep.configs"],
    install_requires=REQUIRED_PACKAGES,
    scripts=["peep/scripts/batch_commands.sh"],
    entry_points={
        "console_scripts": [
            "peep_run_pipeline=peep.scripts.run_peep_pipeline:main",
            "peep_run_module=peep.scripts.run_peep_module:main",
            "peep_generate_config=peep.scripts.generate_config_file:main",
            "peep_run_pipeline_loop=peep.scripts.run_pipeline_loop:main",
        ]
    },
)
