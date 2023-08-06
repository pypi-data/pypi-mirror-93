import json


__murd = r'{}'


class Murdi(dict):
    """ A murd item """
    region_sort_sep = "|||||"
    region_key = "REGION"
    sort_key = "SORT"

    required_keys = [
        region_key,  # This is the primary identifier of a Murdi
        sort_key     # This is a secondary identifier that can specify sorted Murdi region members
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for req_key in self.required_keys:
            if req_key not in self:
                raise Exception("{} must be defined".format(req_key))

        for key, value in self.items():
            self[key] = json.dumps(value) if not isinstance(value, str) \
                else value

    @classmethod
    def ze(cls, murdis: list) -> dict:
        """ Marshall a Murdi list into the Murd storage dictionary """
        return {cls.murdi_to_key(murdi): murdi for murdi in murdis}

    @classmethod
    def region_sort_to_key(cls, region, sort):
        return "{}{}{}".format(region, cls.region_sort_sep, sort)

    @classmethod
    def murdi_to_key(cls, murdi) -> str:
        return "{}{}{}".format(murdi[cls.region_key], cls.region_sort_sep, murdi[cls.sort_key])


def open_murd(filepath):
    global __murd
    with open(filepath, "r") as f:
        __murd = json.dumps(json.loads(f.read()))


def write_murd(filepath):
    with open(filepath, "w") as f:
        f.write(json.dumps(__murd))


def update(murdis):
    global __murd

    primed_murdis = Murdi.ze(murdis)
    print("Storing {} murdis".format(len(primed_murdis)))

    murd = json.loads(__murd)
    murd = dict(**murd, **primed_murdis)
    __murd = json.dumps(murd)
    print(murd)


def read(
    region,
    sort=None,
    min_sort=None,
    max_sort=None,
    limit=None
):
    loaded_murd = json.loads(__murd)

    matched = list(loaded_murd.keys())
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


def delete(murdis):
    global __murd
    murd = json.loads(__murd)
    primed_murdis = Murdi.ze(murdis)
    for key in primed_murdis.keys():
        if key not in murd:
            raise Exception("Murdi {} not found!".format(key))

    for key in primed_murdis.keys():
        murd.pop(key)

    __murd = json.dumps(murd)
