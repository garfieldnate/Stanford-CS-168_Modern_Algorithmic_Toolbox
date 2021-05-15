# TODO

* build target that outputs HTML for all notebooks
    - run jupyter nbconvert --to html on cs168/notebooks/*.ipynb
    - add to ignore
* build target that tests that the notebook output is still the same
    - py.test --nbval --workers 4 --dist loadscope

## Bugs

* Markdown cells with assignment div classes not formatted correctly on HTML output (okay in Jupyter lab view)
* Missing initial `<p>` in markdown cells, leading to first paragraph not breaking.
