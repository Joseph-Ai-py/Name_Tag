import sys
import unittest

sys.path.insert(0, str(__file__).rsplit("/", 2)[0] + "/streamlit")

from brand_dna import build_brand_dna, build_trace, check_brand_integrity


class BrandDNARegressionTests(unittest.TestCase):
    def setUp(self):
        self.brand = {
            "brand_name": "알고맵",
            "brand_name_en": "Algomap",
            "name_meaning": "데이터의 지도",
            "slogan": "나를 읽는 지도",
        }

    def test_normalization_keeps_canonical_foundation(self):
        dna = build_brand_dna(self.brand, {}, {}, {}, {})
        self.assertEqual(dna["foundation"]["brand_name"], "알고맵")
        self.assertEqual(dna["foundation"]["slogan"], "나를 읽는 지도")

    def test_user_trace_preserves_status(self):
        trace = build_trace(
            "O", "foundation", "직접 입력", "사용자 의도", "알고맵", "사용자 확정", status="user_confirmed"
        )
        self.assertEqual(trace["status"], "user_confirmed")

    def test_unrelated_brand_contamination_is_detected(self):
        dna = build_brand_dna(self.brand, {}, {}, {}, {})
        report = check_brand_integrity(
            self.brand,
            dna,
            {"story": "숲결 폐플라스틱 업사이클링 자연 친화"},
        )
        self.assertEqual(report["status"], "FAIL")
        self.assertTrue(any(issue["category"] == "cross_brand_contamination" for issue in report["issues"]))


if __name__ == "__main__":
    unittest.main()
