from collections import defaultdict
from dataclasses import dataclass
from functools import total_ordering
from itertools import groupby
from json import loads
from optparse import OptionParser
from sys import getdefaultencoding

from jsonpath_ng import parse
from tabulate import tabulate


@dataclass(order=True, frozen=True)
class Iter(object):
    size: int


@dataclass(order=True, frozen=True)
class Dict(object):
    size: int


def kv_flatten(obj):
    if isinstance(obj, dict):
        yield tuple(), Dict(len(obj))
        for prefix, sub in obj.items():
            for key, value in kv_flatten(sub):
                yield (prefix, *key), value
    elif isinstance(obj, (list, tuple, set)):
        yield tuple(), Iter(len(obj))
        for element in obj:
            for key, value in kv_flatten(element):
                yield ("*", *key), value
    else:
        yield tuple(), obj


def kv_diff(objs):
    objs = iter(objs)
    keys = set()
    keys.update(kv_flatten(next(objs)))
    for i, obj in enumerate(objs):
        i += 1
        news = set(kv_flatten(obj))
        for missing in keys - news:
            print(i, "missing", missing)
        for addition in news - keys:
            print(i, "addition", addition)
        if keys == news:
            print(i, "match")
        keys |= news


new_trie = lambda: defaultdict(new_trie)


def trie_insert(trie, key, value):
    curr = trie
    for part in key:
        curr = curr[part]
    if None not in curr:
        curr[None] = list()
    curr[None].append(value)


def trie_items(trie):
    for key in trie:
        if key is None:
            yield tuple(), trie[key]
            continue
        for test in trie_items(trie[key]):
            prefix, value = test
            yield (key, *prefix), value


@total_ordering
class MinType(object):
    def __le__(self, other):
        return True

    def __eq__(self, other):
        return self is other


Min = MinType()

min_sortkey = lambda x: (Min, Min) if x is None else (str(type(x)), x)


def json_path(key):
    path = ["$"]
    for part in key:
        if part == "*":
            path.append("[*]")
        else:
            path.append(f".{part}")
    return "".join(path)


def expand_path(path):
    expanded = []
    for part in path.split("."):
        if path == "$":
            pass
        elif part.startswith("[") and part.endswith("]"):
            expanded.append("*")
        else:
            expanded.append(part)
    return expanded


def analyze(obj, *, path="$"):
    root = new_trie()
    jp = parse(path)
    for match in jp.find(obj):
        for key, value in kv_flatten(match.value):
            prefix = expand_path(str(match.full_path))
            trie_insert(root, (*prefix, *key), value)
    results = []
    for key, values in trie_items(root):
        for i, (t, group) in enumerate(groupby(sorted(values, key=min_sortkey), type)):
            group = list(group)
            row = []
            if i == 0:
                row.append(json_path(key))
            else:
                row.append("")

            row.extend(
                [
                    t.__name__,
                    len(group),
                    len(set(group)),
                    min(group) if t is not type(None) else "",
                    max(group) if t is not type(None) else "",
                ]
            )
            results.append(row)
    print(
        tabulate(
            results,
            headers=["Key", "Type", "Values", "Distinct", "Min", "Max"],
            tablefmt="simple",
        )
    )


def main():
    parser = OptionParser(prog="json-analyze")
    parser.add_option(
        "-f", "--file", dest="filename", help="JSON file to analyze", metavar="FILE"
    )
    parser.add_option(
        "-e",
        "--encoding",
        dest="encoding",
        help="Text Encoding",
        metavar="CODEC",
        default=getdefaultencoding(),
    )
    parser.add_option(
        "-p",
        "--path",
        dest="path",
        help="JSON path applied before the analysis",
        metavar="PATH",
        default="$",
    )
    (options, args) = parser.parse_args()
    if options.filename:
        with open(options.filename, "r", encoding=options.encoding) as fh:
            analyze(loads(fh.read()), path=options.path)
