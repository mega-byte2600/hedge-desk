import json
import unittest
from datetime import date

from hedge_desk.data.global_public_feeds import (
    eurostat_hicp_inflation,
    imf_datamapper,
    nasa_eonet_events,
    oecd_composite_leading_indicator,
    usgs_material_earthquakes,
)


class GlobalPublicFeedTests(unittest.TestCase):
    def test_imf_datamapper_parses_allowlisted_indicator_and_entities(self):
        seen = []
        payload = json.dumps(
            {
                "values": {
                    "NGDP_RPCH": {
                        "USA": {"2025": 2.1, "2026": 2.0},
                        "CHN": {"2025": 4.8, "2026": 4.5},
                    }
                }
            }
        ).encode()

        def transport(url):
            seen.append(url)
            return 200, payload

        result = imf_datamapper(
            "NGDP_RPCH", ("USA", "CHN"), periods=(2025, 2026), transport=transport
        )
        self.assertEqual(result.provider_id, "imf-datamapper")
        self.assertEqual(result.row_count, 4)
        self.assertEqual(result.rows[0]["indicator"], "NGDP_RPCH")
        self.assertIn("/api/v2/NGDP_RPCH/USA/CHN", seen[0])
        self.assertIn("periods=2025%2C2026", seen[0])

    def test_imf_datamapper_fails_closed_on_unvetted_or_malformed_data(self):
        with self.assertRaisesRegex(ValueError, "unsupported IMF"):
            imf_datamapper("NOT_REAL", transport=lambda _url: (200, b"{}"))
        with self.assertRaisesRegex(ValueError, "entity"):
            imf_datamapper("NGDP_RPCH", ("XXX",), transport=lambda _url: (200, b"{}"))
        with self.assertRaisesRegex(ValueError, "requested indicator"):
            imf_datamapper(
                "NGDP_RPCH", ("USA",), transport=lambda _url: (200, b'{"values":{}}')
            )

    def test_oecd_cli_parses_csv_and_limits_output(self):
        seen = []
        payload = (
            "REF_AREA,TIME_PERIOD,OBS_VALUE,UNIT_MEASURE,MEASURE\n"
            "USA,2026-01,99.8,IX,LI\n"
            "USA,2026-02,100.1,IX,LI\n"
            "USA,2026-03,100.4,IX,LI\n"
        ).encode()

        def transport(url):
            seen.append(url)
            return 200, payload

        result = oecd_composite_leading_indicator(
            "USA", start_period="2026-01", limit=2, transport=transport
        )
        self.assertEqual(result.provider_id, "oecd-cli")
        self.assertEqual(result.row_count, 2)
        self.assertEqual(result.rows[-1]["time_period"], "2026-03")
        self.assertIn("USA.M.LI...AA...H", seen[0])
        self.assertIn("format=csvfilewithlabels", seen[0])

    def test_oecd_cli_rejects_bad_area_and_period(self):
        with self.assertRaisesRegex(ValueError, "reference area"):
            oecd_composite_leading_indicator("XXX", transport=lambda _url: (200, b"x"))
        with self.assertRaisesRegex(ValueError, "YYYY-MM"):
            oecd_composite_leading_indicator(
                "USA", start_period="26-01", transport=lambda _url: (200, b"x")
            )

    def test_eurostat_current_hicp_parses_jsonstat_values(self):
        seen = []
        payload = json.dumps(
            {
                "version": "2.0",
                "class": "dataset",
                "id": ["freq", "unit", "coicop", "geo", "time"],
                "size": [1, 1, 1, 1, 3],
                "dimension": {
                    "time": {
                        "category": {
                            "index": {"2026-06": 0, "2026-07": 1, "2026-08": 2}
                        }
                    }
                },
                "value": {"0": 2.5, "1": 2.9, "2": 3.3},
            }
        ).encode()

        def transport(url):
            seen.append(url)
            return 200, payload

        result = eurostat_hicp_inflation("EA20", periods=3, transport=transport)
        self.assertEqual(result.provider_id, "eurostat")
        self.assertEqual(result.dataset, "prc_hicp_minr")
        self.assertEqual(result.rows[-1]["time_period"], "2026-08")
        self.assertEqual(result.rows[-1]["value"], 3.3)
        self.assertIn("unit=RCH_A", seen[0])
        self.assertIn("coicop=CP00", seen[0])
        self.assertIn("geo=EA20", seen[0])

    def test_eurostat_hicp_fails_closed_on_extra_dimensions(self):
        payload = json.dumps(
            {
                "id": ["freq", "unit", "coicop", "geo", "time"],
                "size": [1, 2, 1, 1, 1],
                "dimension": {"time": {"category": {"index": {"2026-08": 0}}}},
                "value": [3.3],
            }
        ).encode()
        with self.assertRaisesRegex(ValueError, "extra dimensions"):
            eurostat_hicp_inflation(transport=lambda _url: (200, payload))

    def test_usgs_material_earthquakes_normalizes_geojson(self):
        seen = []
        payload = json.dumps(
            {
                "type": "FeatureCollection",
                "features": [
                    {
                        "id": "us123",
                        "properties": {
                            "time": 1790640000000,
                            "updated": 1790640300000,
                            "mag": 6.1,
                            "place": "Example region",
                            "alert": "yellow",
                            "tsunami": 0,
                            "sig": 600,
                            "status": "reviewed",
                            "url": "https://earthquake.usgs.gov/example",
                        },
                        "geometry": {"type": "Point", "coordinates": [140.0, 35.0, 20.0]},
                    }
                ],
            }
        ).encode()

        def transport(url):
            seen.append(url)
            return 200, payload

        result = usgs_material_earthquakes(
            days=7, min_magnitude=5.5, limit=10, as_of=date(2026, 9, 29), transport=transport
        )
        self.assertEqual(result.provider_id, "usgs-earthquakes")
        self.assertEqual(result.rows[0]["magnitude"], 6.1)
        self.assertEqual(result.rows[0]["longitude"], 140.0)
        self.assertIn("starttime=2026-09-22", seen[0])
        self.assertIn("minmagnitude=5.5", seen[0])
        self.assertIn("eventtype=earthquake", seen[0])

    def test_usgs_rejects_unbounded_requests(self):
        with self.assertRaisesRegex(ValueError, "days"):
            usgs_material_earthquakes(days=31, transport=lambda _url: (200, b"{}"))
        with self.assertRaisesRegex(ValueError, "min_magnitude"):
            usgs_material_earthquakes(min_magnitude=11, transport=lambda _url: (200, b"{}"))

    def test_nasa_eonet_v3_normalizes_current_events(self):
        seen = []
        payload = json.dumps(
            {
                "events": [
                    {
                        "id": "EONET_1",
                        "title": "Example Wildfire",
                        "closed": None,
                        "categories": [{"id": "wildfires", "title": "Wildfires"}],
                        "sources": [{"id": "InciWeb", "url": "https://example.test"}],
                        "geometry": [
                            {
                                "date": "2026-09-28T00:00:00Z",
                                "type": "Point",
                                "coordinates": [-120.0, 35.0],
                            }
                        ],
                    }
                ]
            }
        ).encode()

        def transport(url):
            seen.append(url)
            return 200, payload

        result = nasa_eonet_events(days=30, limit=10, status="open", transport=transport)
        self.assertEqual(result.provider_id, "nasa-eonet")
        self.assertEqual(result.rows[0]["event_id"], "EONET_1")
        self.assertEqual(result.rows[0]["categories"][0]["id"], "wildfires")
        self.assertEqual(result.rows[0]["coordinates"], [-120.0, 35.0])
        self.assertIn("status=open", seen[0])
        self.assertIn("days=30", seen[0])

    def test_nasa_eonet_rejects_bad_status(self):
        with self.assertRaisesRegex(ValueError, "status"):
            nasa_eonet_events(status="active", transport=lambda _url: (200, b"{}"))


if __name__ == "__main__":
    unittest.main()
