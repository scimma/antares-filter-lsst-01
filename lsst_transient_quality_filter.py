"""
ANTARES filter for selecting high-quality LSST transient candidates
for cross matching against Gaia and other catalogs using LSDB
running in SCiMMA infrastructure. See https://scimma.org/

This filter runs inside ANTARES infrastructure. It evaluates each incoming
LSST alert against quality criteria and tags passing alerts for downstream
crossmatching against catalogs.
"""

from antares_devkit.models import BaseFilter


class LsstTransientQualityFilterScimma(BaseFilter):
    """
    This filter finds loci where the first alert has a SNR > 10 and the
    image is not saturated, near an image edge, not classified as a dipole,
    and excludes known solar system objects.
    """

    SLACK_CHANNEL = "#filter-scimma-lsst-quality"

    TRIGGERING_SURVEY = "lsst"

    REQUIRED_LOCUS_PROPERTIES = []

    REQUIRED_ALERT_PROPERTIES = [
        "lsst_diaSource_snr",
        "lsst_diaSource_ssObjectId",
        "lsst_diaSource_psfFlux_flag",
        "lsst_diaSource_centroid_flag",
        "lsst_diaSource_shape_flag",
        "lsst_diaSource_isDipole",
        "lsst_diaSource_pixelFlags_saturated",
        "lsst_diaSource_pixelFlags_edge",
        "lsst_diaSource_pixelFlags_cr",
        "lsst_diaSource_pixelFlags_streak",
    ]

    REQUIRED_TAGS = []

    REQUIRES_FILES = []

    OUTPUT_TAG = "lsst_scimma_quality_transient"

    OUTPUT_LOCUS_PROPERTIES = []

    OUTPUT_LOCUS_TAGS = [
        {
            "name": OUTPUT_TAG,
            "description": (
                "LSST alert passes quality cuts for transient candidate "
                "crossmatching by SCiMMA: SNR > 10, no quality flags, "
                "not a known solar system object."
            ),
        },
    ]

    def setup(self):
        pass

    def _run(self, locus):
        props = locus.alerts[-1].properties

        # SNR must be strictly greater than 10.
        if not props["lsst_diaSource_snr"] > 10:
            return

        # Exclude known solar system objects. The type of ssObjectId is
        # not yet confirmed, so check for integer 0, None, and string "0".
        if props["lsst_diaSource_ssObjectId"] not in (0, None, "0"):
            return

        # Quality flags must all be falsy.
        if props["lsst_diaSource_psfFlux_flag"]:
            return
        if props["lsst_diaSource_centroid_flag"]:
            return
        if props["lsst_diaSource_shape_flag"]:
            return
        if props["lsst_diaSource_isDipole"]:
            return
        if props["lsst_diaSource_pixelFlags_saturated"]:
            return
        if props["lsst_diaSource_pixelFlags_edge"]:
            return
        if props["lsst_diaSource_pixelFlags_cr"]:
            return
        if props["lsst_diaSource_pixelFlags_streak"]:
            return

        locus.tag(self.OUTPUT_TAG)
