You can install the package with pip:

```sh
pip install dist/Fabrication-utilities-1.10.0
```

Read more about python packages, `pyproject.toml`, and how to upload packages to PyPI
on the [PyPI documentation](https://packaging.python.org/en/latest/tutorials/packaging-projects/).


### Template update

We use cruft to update the project based on template changes. A `cruft-update.yml` is included in Github workflows to automatically check for updates and create pull requests to apply updates. Follow the [instructions](https://github.blog/changelog/2022-05-03-github-actions-prevent-github-actions-from-creating-and-approving-pull-requests/) on how to enable Github Actions to create pull requests.

To run the check for updates locally, follow the instructions on [`cruft` website](https://cruft.github.io/cruft/#updating-a-project).

## Description of the plugin

The plugin is intended as an extension of an oasis or a local instance of NOMAD. It could be useful to describe some critcal fabrication and characterization steps employed in micro and nano fabrication.
It is built with three main sections. The tests folder contains some scripts used to test some features
of the package. As an example you can find for the app that the test is run onto the the so
called "transapp" (for more details see the docs and the code in src/fabrication_utilities/apps/transapp.py). For the schema packages an example yaml file is defined in the tests/data folder and it is called by the testing module in the tests/schema_packages. Following the already defined method you can test all the features present in the plugin defining your own tests. Finally for what concerns the main module src/fabrication_utilities the reader is remainded to the readme present into that folder and for more information to the docs repository of the plugin.

## Main contributors
| Name | E-mail     |
|------|------------|
| Matteo Bontorno | [mbontorno@fbk.eu](mailto:mbontorno@fbk.eu)
