
## Pandas/Numpy

* Indexes for `data` and `series` have to be the same for you to do something like data[ series[series == blah]]. Check `data.index` and `foo.index` before assuming this will work. Would be really nice if we could capture this requirement in type signatures!
    - Particularly, make sure that you don't mix 1- and 0-indexed datasets. Check them when you read from csv; if you got a 0-indexed but need a 1-indexed data set, do `data.index += 1`.
