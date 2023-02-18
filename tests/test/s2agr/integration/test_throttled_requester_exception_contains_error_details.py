import unittest

from hamcrest import assert_that, equal_to
import vcr

from s2agr.requester import ThrottledRequester, ThrottledRequesterException
from s2agr.urls import UrlBuilderForSinglePaper, q
from test.s2agr.helpers.samples import sample_01_id

test_vcr = vcr.VCR(
    cassette_library_dir='helpers/cassettes',
    path_transformer=vcr.VCR.ensure_suffix('.yaml')
)

class ThrottledRequesterTestCase(unittest.TestCase):
    @test_vcr.use_cassette
    def test_exception_contains_api_error_details(self):
        requester = ThrottledRequester(0.01)
        url = UrlBuilderForSinglePaper(sample_01_id()).with_query(q().with_fields('non-existent-field')).get_url()
        try:
            requester.get(url)
            self.fail('should have thrown an exception')
        except ThrottledRequesterException as e:
            assert_that(str(e), equal_to('Unrecognized or unsupported fields: [non-existent-field]'))


if __name__ == '__main__':
    unittest.main()
