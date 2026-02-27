"""
Standalone test script for LsstTransientQualityFilterScimma.

Fetches a real LSST locus from ANTARES and runs it through the filter,
printing the filter report.

Run with:
    python test_lsst_transient_quality_filter.py

Requires the ANTARES devkit environment (e.g., NOIRLab DataLab
with the "Python 3 (ANTARES)" kernel, or a local install of
antares-client and antares-devkit).
"""

import pprint

from antares_client import search
from antares_devkit.models import DevKitLocus
from antares_devkit.utils import filter_report

from lsst_transient_quality_filter import LsstTransientQualityFilterScimma

LSST_DIA_OBJECT_ID = "170055002004914266"

print(f"Fetching locus for LSST diaObject ID: {LSST_DIA_OBJECT_ID}")
client_locus = search.get_by_lsst_dia_object_id(LSST_DIA_OBJECT_ID)

if client_locus is None:
    print("ERROR: Locus not found. Check the diaObject ID and your ANTARES credentials.")
    raise SystemExit(1)

print(f"  Locus ID : {client_locus.locus_id}")
print(f"  RA       : {client_locus.ra}")
print(f"  Dec      : {client_locus.dec}")
print(f"  Alerts   : {len(client_locus.alerts)}")
print()

locus_dict = client_locus.to_devkit()
locus = DevKitLocus.model_validate(locus_dict)

filter_instance = LsstTransientQualityFilterScimma()

print("Running filter...")
report = filter_report(filter_instance, locus)

print()
print("Filter report:")
pprint.pprint(report)

if LsstTransientQualityFilterScimma.OUTPUT_TAG in report.get("new_tags", []):
    print()
    print(f"PASS: locus tagged '{LsstTransientQualityFilterScimma.OUTPUT_TAG}'")
else:
    print()
    print("REJECT: locus was not tagged")
