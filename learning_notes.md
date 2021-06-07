
## Jupyter

### Bugs

* Sometimes you have to have to add manual `<p>` markers to make a paragraph break with proper spacing in markdown sections.

## Pandas/Numpy

* Indexes for `data` and `series` have to be the same for you to do something like data[ series[series == blah]]. Check `data.index` and `foo.index` before assuming this will work. Would be really nice if we could capture this requirement in type signatures!
    - Particularly, make sure that you don't mix 1- and 0-indexed datasets. Check them when you read from csv; if you got a 0-indexed but need a 1-indexed data set, do `data.index += 1`.

* Quickest way to get slanted labels for x-axis: `fig.autofmt_xdate()`
* df[i] seems to get the i'th column, while df.loc[i] gets the i'th row
* Bokeh figure x_range and y_range have to be a list of strings; for a dataframe, use `df.index = df.index.map(str)` to make it so.
* doing `np.array([1,2,3])` gives a 1-d array, the transpose of which is another 1-d array, not a column vector! To create a column vector, take that 1-d array and pass it to `np.vstack()`. Or slice with `[np.newaxis]`. Then that thing can be transposed.
    - Was super confused because `X.T @ X` always gave a single value; 1-d arrays can only give dot products in this context, since they can't be transposed. Transposition requires 2 dimensions.

