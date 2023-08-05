# json-analyze

A small tool to check JSON data for structural and data inconsistencies.

Given this JSON object:
```json
{
  "a": [1,2,3,"hi"],
  "c": [
    123,
    2.34,
    "bye",
    [],
    {},
    {"a":  123},
    {"a":  null}
  ]
}
```

Executing `json-analyze -f example.json` will display:
```text
Key       Type        Values    Distinct  Min           Max
--------  --------  --------  ----------  ------------  ------------
$         Dict             1           1  Dict(size=2)  Dict(size=2)
$.a       Iter             1           1  Iter(size=4)  Iter(size=4)
$.a[*]    int              3           3  1             3
          str              1           1  hi            hi
$.c       Iter             1           1  Iter(size=7)  Iter(size=7)
$.c[*]    float            1           1  2.34          2.34
          int              1           1  123           123
          Dict             3           2  Dict(size=0)  Dict(size=1)
          Iter             1           1  Iter(size=0)  Iter(size=0)
          str              1           1  bye           bye
$.c[*].a  NoneType         1           1
          int              1           1  123           123
```


## Development
```shell
black .
rm -rv dist/
python setup.py sdist bdist_wheel
twine upload dist/*
```
