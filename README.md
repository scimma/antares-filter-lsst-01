# ANTARES Broker Filter for LSST Alerts to Cross-Match

A Python filter for the [ANTARES](https://antares.noirlab.edu/) broker that selects
high-quality LSST transient candidates for downstream cross-matching against the Gaia
catalog using [LSDB](https://lsdb.io/), running in [SCiMMA](https://scimma.org/)
infrastructure.

## Filter

`lsst_transient_quality_filter.py` implements `LsstTransientQualityFilterScimma`, a
`BaseFilter` subclass that runs inside ANTARES infrastructure. For each incoming LSST
alert it checks ten quality criteria against the latest alert's `lsst_diaSource_*`
properties. Alerts that pass all criteria are tagged `lsst_scimma_quality_transient`
and routed to the SCiMMA subscription topic for cross-matching.

**Selection criteria** — the latest alert must satisfy all of:

| Criterion | Condition |
|-----------|-----------|
| Signal-to-noise ratio | `lsst_diaSource_snr > 10` |
| Not a solar system object | `lsst_diaSource_ssObjectId in (0, None, "0")` |
| No PSF flux flag | `lsst_diaSource_psfFlux_flag` is falsy |
| No centroid flag | `lsst_diaSource_centroid_flag` is falsy |
| No shape flag | `lsst_diaSource_shape_flag` is falsy |
| Not a dipole | `lsst_diaSource_isDipole` is falsy |
| Not saturated | `lsst_diaSource_pixelFlags_saturated` is falsy |
| Not near image edge | `lsst_diaSource_pixelFlags_edge` is falsy |
| No cosmic ray flag | `lsst_diaSource_pixelFlags_cr` is falsy |
| No streak flag | `lsst_diaSource_pixelFlags_streak` is falsy |

If any required property is absent from the alert, ANTARES skips execution of the
filter automatically (via `REQUIRED_ALERT_PROPERTIES`).

## Test

`test_lsst_transient_quality_filter.py` is a standalone script that fetches a real
LSST locus from ANTARES by diaObject ID, runs it through the filter using the ANTARES
devkit `filter_report()` utility, and prints the result.

## Setup

Create and activate a Python virtual environment, then install the required packages:

```bash
python3 -m venv antares_env
source antares_env/bin/activate
pip install antares-client antares-devkit
```

## Running the Test

With the virtual environment active:

```bash
python test_lsst_transient_quality_filter.py
```

The script fetches locus `170055002004914266` from ANTARES, runs the filter, and
prints the `filter_report()` output along with a PASS or REJECT summary.

## References

- [ANTARES DevKit — Structure of a Filter](https://nsf-noirlab.gitlab.io/csdc/antares/devkit/learn/structure-of-a-filter/)
- [ANTARES DevKit — Testing Filters](https://nsf-noirlab.gitlab.io/csdc/antares/devkit/learn/testing-filters/)
