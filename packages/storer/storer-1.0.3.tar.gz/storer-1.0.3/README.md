# 1. Storer

- [1. Storer](#1-storer)
  - [1.1. Usage](#11-usage)
  - [1.2. Contribution](#12-contribution)
  - [License](#-license)

Minimalist storage class for any purpose. Created for internal needs. Feel free to use it and contribute (see [contribution section](#12-contribution)).



## 1.1. Usage

Installation:
`
pip3 install Storer
`

Easy to use.

1. Create an Storer instance: `s = Storer()`
2. Put something: `s.put(what=<what_ever_you_like>, name=<name_of_object>)`
3. Get something: `s.get(name=<name_of_object>)`
4. Look at objects: `s.show()` or `output = s.show(get_string=True)`


Few examples:

```
>>> from storer import Storer
>>> s = Storer()
>>> s.put(what="string", name="my_string")
>>> s.get(name="my_string")
'string'
>>> 
```

```
>>> from storer import Storer
>>> s = Storer(path_dumps="~/my_folder_for_dumps", dump_name="dumps", verbose=True)
[Storer v.0.9.0 [20]] is initialized!
Dump folder: [/Users/alexander/my_folder_for_dumps]
>>> s.load() # loading if dump exists
[Storer] /Users/alexander/my_folder_for_dumps loading...
[Storer] No data is available for loading...
{}
>>> s.put(what=[i for i in range(10)], name="my_range")
>>> s.put(what={v:v*2 for v in range(5)}, name="my_dict")
>>> s.dump()
[Storer] /Users/alexander/my_folder_for_dumps dumps dumping...
>>> s.load() # loading again
[Storer] /Users/alexander/my_folder_for_dumps loading...
{'my_range': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], 'my_dict': {0: 0, 1: 2, 2: 4, 3: 6, 4: 8}}
>>> 
```


## 1.2. Contribution

Feel free to contribute to the project, but please create initially an issue with detailed problem and way to resolve it. 

## License
----

MIT
