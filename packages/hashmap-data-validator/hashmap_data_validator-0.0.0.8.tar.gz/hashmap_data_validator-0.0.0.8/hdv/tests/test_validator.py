from hdv.validator import Validator

s = Validator()

s.hdv(sf_query= "select name, owner from TEST_DB.PANDAS_CLOUDY_TEST.validator_test", jdbc_query= "select name, owner from test.validator")