import json

from app.tests import BaseTestClass


class TestParcelView(BaseTestClass):
    """"""

    def test__create_order(self):
        """This will test POST /parcels"""

        res = self.client.post(
            "api/v2/users/parcels", data=json.dumps(self.generic_parcel), content_type="application/json", headers=self.headers)

        result = json.loads(res.data)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(result["Success"], "Your parcel order has been saved")

    def test_invalid_parcel_name(self):
        """Parcels must have valid names in order to be sent"""
        pass

    def test_invalid_pickup_location(self):
        """Parcels must have valid pickup location"""
        pass

    def test_invalid_destination(self):
        """Parcels must have valid destination"""
        pass

    def test_valid_weight(self):
        """Parcels must have valid weight"""
        pass
