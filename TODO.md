# TODO

* build target that outputs HTML for all notebooks
    - run jupyter nbconvert --to html on cs168/notebooks/*.ipynb
    - add to ignore
* build target that tests that the notebook output is still the same
    - py.test --nbval --workers 4 --dist loadscope

* IF we were to learn to use tikz, then re-do the image from project 2 using Mathcha or something and include in the notebook using https://github.com/mkrphys/ipython-tikzmagic/blob/master/tikzmagic.py. To build everything, the environment would also require `pdflatex`, so we may need to dockerize the whole thing.
    - Could also use Assymptote: https://github.com/jrjohansson/ipython-asymptote

* Make repo public; put course materials and downloaded papers into a sub-repo.

## Bugs

* Markdown cells with assignment div classes not formatted correctly on HTML output (okay in Jupyter lab view)
* Missing initial `<p>` in markdown cells, leading to first paragraph not breaking.
* Markdown renders HTML comments!!! <!--

--> is put in the output. That is awful!
* $...$ then newline becomes new paragraph in output, regardless of whether there are 2 newlines!
* mini_project_4: very unclear pca_resolve should do exactly. What is a "coordinate" in this context?

## Wish List

* Magic functionality for markdown cells. I want the magics to be hidden in the output; I want this so that I can style cells with a some `%%mystyle% instead of surrounding each cell with a div, a style, and the required intervening newlines. This would probably have to written in JavaScript, like the rest of the markdown stuff.
* No clean way to add footnotes currently. https://github.com/jupyter/notebook/issues/1287#issuecomment-504491328

