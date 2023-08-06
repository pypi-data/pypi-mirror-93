Convert the string representation of a Python dictionary to JSON

You've got a Python dictionary that was printed to a log file.  You want to run it through JSON tools, like [jq](https://stedolan.github.io/jq/) but it's not actually JSON.

This command line tool allows you convert to JSON.


## Why?

If you're the owner of a python script that writes simply does `print(str(d))` you should consider changing it to use `print(json.dumps(d))` instead.
However, you're not always the owner of scripts you use and you can't always change the code.
Instead, convert from the python string representation of a dictionary to JSON.


## Examples

```
$ cat input.txt
{'example': {'number': 42, 'text': 'lorem ipsum', 'boolean': True}}
```

Let's convert it to JSON with:

```
$ cat input.txt | python3 -m pydict2json
{"example": {"number": 42, "text": "lorem ipsum", "boolean": true}}
```

That's hard to read, let's pretty print:

```
$ cat input.txt | python3 -m pydict2json --pretty
{
  "example": {
    "number": 42,
    "text": "lorem ipsum",
    "boolean": true
  }
}
```

Much better.

Now that it's JSON we can use all our favorite JSON tools like `jq`:

```
$ cat input.txt | python3 -m pydict2json | jq .example.number
42
```

The tool also supports input directly on the command line:

```
$ python3 -m pydict2json --literal "{'a': None}"
{"a": null}
```

