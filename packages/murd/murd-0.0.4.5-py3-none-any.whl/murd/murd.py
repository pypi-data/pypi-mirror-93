import json


__murd = r'{}'


class Murdi(dict):
    """ A murd item """
    region_sort_sep = "|||||"
    region_key = "REGION"
    sort_key = "SORT"

    def __init__(self, REGION="MISC", SORT="_", **kwargs):
        kwargs = {**kwargs, "REGION": REGION, "SORT": SORT}
        super().__init__(**kwargs)

        for key, value in self.items():
            self[key] = json.dumps(value) if not isinstance(value, str) \
                else value

    def __call__(self):
        return {k: v for k, v in self.items() if k not in [self.region_key, self.sort_key]}

    @classmethod
    def ze(cls, murdis: list) -> dict:
        """ Marshall a Murdi list into the Murd storage dictionary """
        return {cls.murdi_to_key(murdi): murdi for murdi in murdis}

    @classmethod
    def region_sort_to_key(cls, region, sort):
        """ Format a region and a sort value into a Murd store key """
        return "{}{}{}".format(region, cls.region_sort_sep, sort)

    @classmethod
    def murdi_to_key(cls, murdi) -> str:
        """ Use a Murd item to create a Murd store key """
        murdi = Murdi(**murdi)
        return "{}{}{}".format(murdi[cls.region_key], cls.region_sort_sep, murdi[cls.sort_key])


def clear_murd():
    """ Reset murd to empty store """
    global __murd
    __murd = r'{}'


def open_murd(filepath):
    """ Open Murd store from file """
    global __murd
    with open(filepath, "r") as f:
        __murd = json.dumps(json.loads(f.read()))


def write_murd(filepath):
    """ Write Murd store out to file """
    with open(filepath, "w") as f:
        f.write(__murd)


def update(murdis):
    """ Create or modify an item in the Murd store """
    global __murd
    primed_murdis = Murdi.ze(murdis)
    murd = json.loads(__murd)
    murd = {**murd, **primed_murdis}
    __murd = json.dumps(murd)
    return len(primed_murdis)


def read(
    region,
    sort=None,
    min_sort=None,
    max_sort=None,
    limit=None
):
    """ Read items from the Murd store """
    loaded_murd = json.loads(__murd)

    matched = [key for key in loaded_murd.keys() if key[:len(region)] == region]
    if sort is not None:
        prefix = "{}{}{}".format(region, Murdi.region_sort_sep, sort)
        matched = [key for key in matched if prefix in key]

    if min_sort is not None:
        maximum = Murdi.region_sort_to_key(region, min_sort)
        matched = [key for key in matched if key < maximum]

    if max_sort is not None:
        minimum = Murdi.region_sort_to_key(region, max_sort)
        matched = [key for key in matched if key > minimum]

    results = [Murdi(**loaded_murd[key]) for key in matched]

    if limit is not None:
        results = results[:limit]

    return results


def read_first(
    region,
    sort=None,
    min_sort=None,
    max_sort=None,
    limit=None
):
    """ Utility method to simply return first result """
    try:
        return read(region, sort, min_sort, max_sort, limit)[0]
    except IndexError:
        raise KeyError(f"No results")


def delete(murdis):
    """ Delete one or more items from the Murd store """
    global __murd
    murd = json.loads(__murd)
    primed_murdis = Murdi.ze(murdis)
    for key in primed_murdis.keys():
        if key not in murd:
            raise Exception("Murdi {} not found!".format(key))

    for key in primed_murdis.keys():
        murd.pop(key)

    __murd = json.dumps(murd)
