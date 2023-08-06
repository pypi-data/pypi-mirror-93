# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
"""PyBIDS tooling"""
import os
import json
from pathlib import Path
from collections import defaultdict

DEFAULT_TYPES = ["bold", "T1w", "T2w"]


def collect_bids_data(
    layout, participant_label=None, session=None, run=None, task=None, bids_type=None
):
    """Get files in dataset"""

    bids_type = bids_type or DEFAULT_TYPES
    if not isinstance(bids_type, (list, tuple)):
        bids_type = [bids_type]

    basequery = {
        "subject": participant_label,
        "session": session,
        "task": task,
        "run": run,
    }
    # Filter empty lists, strings, zero runs, and Nones
    basequery = {k: v for k, v in basequery.items() if v}

    # Start querying
    imaging_data = defaultdict(list, {})
    for btype in bids_type:
        imaging_data[btype] = layout.get(
            suffix=btype, return_type="file", extension=["nii", "nii.gz"], **basequery
        )

    return imaging_data


def write_bidsignore(deriv_dir):
    bids_ignore = (
        "*.html", "logs/",  # Reports
        "*_T1w.json", "*_T2w.json", "*_bold.json",  # Outputs are not yet standardized
    )
    ignore_file = Path(deriv_dir) / ".bidsignore"

    ignore_file.write_text("\n".join(bids_ignore) + "\n")


def write_derivative_description(bids_dir, deriv_dir):
    from ..__about__ import __version__, __download__

    bids_dir = Path(bids_dir)
    deriv_dir = Path(deriv_dir)
    desc = {
        'Name': 'MRIQC - MRI Quality Control',
        'BIDSVersion': '1.4.0',
        'DatasetType': 'derivative',
        'GeneratedBy': [{
            'Name': 'MRIQC',
            'Version': __version__,
            'CodeURL': __download__,
        }],
        'HowToAcknowledge':
            'Please cite our paper (https://doi.org/10.1371/journal.pone.0184661).',
    }

    # Keys that can only be set by environment
    # XXX: This currently has no effect, but is a stand-in to remind us to figure out
    # how to detect the container
    if 'MRIQC_DOCKER_TAG' in os.environ:
        desc['GeneratedBy'][0]['Container'] = {
            "Type": "docker",
            "Tag": f"poldracklab/mriqc:{os.environ['MRIQC_DOCKER_TAG']}"
        }
    if 'MRIQC_SINGULARITY_URL' in os.environ:
        desc['GeneratedBy'][0]['Container'] = {
            "Type": "singularity",
            "URI": os.getenv('MRIQC_SINGULARITY_URL')
        }

    # Keys deriving from source dataset
    orig_desc = {}
    fname = bids_dir / 'dataset_description.json'
    if fname.exists():
        orig_desc = json.loads(fname.read_text())

    if 'DatasetDOI' in orig_desc:
        desc['SourceDatasets'] = [{
            'URL': f'https://doi.org/{orig_desc["DatasetDOI"]}',
            'DOI': orig_desc['DatasetDOI']
        }]
    if 'License' in orig_desc:
        desc['License'] = orig_desc['License']

    Path.write_text(deriv_dir / 'dataset_description.json', json.dumps(desc, indent=4))
