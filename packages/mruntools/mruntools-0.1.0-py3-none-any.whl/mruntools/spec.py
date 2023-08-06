import json
import logging
import pathlib

import parse


from types import SimpleNamespace


logger = logging.getLogger(__name__)


class ItemSpec(SimpleNamespace):

    def template_repr(self, template):
        return template.format(**self.__dict__)

    def json_repr(self):
        return json.dumps(self.__dict__)

    def __hash__(self):
        return self.json_repr().__hash__()


def item_spec_from_fpath(fpath):
    with open(fpath) as fh:
        metadata = json.load(fh)

    return ItemSpec(**metadata["spec"])


def get_all_specs(dirpath):

    dirpath = pathlib.Path(dirpath)
    fpath_iter = dirpath.rglob("*.json")
    specs = [item_spec_from_fpath(fpath) for fpath in fpath_iter]

    return specs


def specs_from_fpath_metadata(dirpath, parse_templates):

    def metadata_from_fname(fname):
        for template in parse_templates:
            result = parse.parse(template, fname)
            if result is not None:
                return result.named

        return None

    fpath_iter = pathlib.Path(dirpath).iterdir()
    fname_iter = (fpath.name for fpath in fpath_iter)

    specs = []
    for fname in fname_iter:
        result = metadata_from_fname(fname)
        if result:
            specs.append(ItemSpec(**result))
        else:
            logger.warning(f"Couldn't parse {fname}")

    return specs
