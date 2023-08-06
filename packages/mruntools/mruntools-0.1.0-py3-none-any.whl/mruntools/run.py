import io
import sys
import json
import time
import uuid
import logging
import pathlib
import datetime

import ruamel.yaml
import numpy as np


logger = logging.getLogger("runtools")


def one_to_one(input_ds, idns, process_func, output_ds):

    t_start = time.time()
    t_hist = []
    results = []
    for n, idn in enumerate(idns, start=1):
        if len(t_hist):
            t_mean = np.mean(t_hist)
        else:
            t_mean = 1

        n_remaining = len(idns) - n
        t_remaining = t_mean * n_remaining
        logger.info(f"Procesing [{n}/{len(idns)}]: {idn}, {t_remaining:.2f}")

        t_pre = time.time()
        result = process_func(input_ds, idn, output_ds)
        results.append(result)
        t_hist.append(time.time() - t_pre)

    runstats = {
        "total_time": time.time() - t_start,
        "n_items": len(idns)
    }

    return results, runstats


def create_readme(config, runstats):
    yaml = ruamel.yaml.YAML()

    readme_dict = {
        "config": config.raw_config,
        "runstats": runstats
    }

    with io.StringIO() as f:
        yaml.dump(readme_dict, f)
        readme_content = f.getvalue()

    return readme_content


def run_process(spec_iter, measure_func, config):

    n_items = len(spec_iter)

    all_measures = []
    t_start = time.time()
    t_hist = []

    working_dirpath = pathlib.Path(config.working_dirpath)
    working_dirpath.mkdir(exist_ok=True, parents=True)

    for n, spec in enumerate(spec_iter, start=1):
        logger.info(f"Processing {spec}")

        t_pre = time.time()
        measures = measure_func(spec)
        t_hist.append(time.time() - t_pre)

        prefix = uuid.uuid4()
        data_fname = f"{prefix}.csv"

        metadata = {
            "spec": spec.__dict__,
            "data_fname": data_fname
        }
        with open(working_dirpath/f"{prefix}.json", "w") as fh:
            json.dump(metadata, fh, indent=2)
        measures.to_csv(working_dirpath/data_fname)

        time_string = f"Item {n}/{n_items}, {t_hist[-1]:.2f}s, total elapsed: {sum(t_hist):.2f}"

        if n > 0:
            t_mean = np.mean(t_hist)
            t_expected = (n_items -n) * t_mean
            dt_expected = datetime.datetime.now() + datetime.timedelta(0, int(t_expected))
            dt_expected_str = dt_expected.strftime("%H:%M")
            time_string += f" estimate {t_expected:.2f} remaining, ETA {dt_expected_str}"

        logger.info(time_string)

        all_measures.append(measures)

    return all_measures
