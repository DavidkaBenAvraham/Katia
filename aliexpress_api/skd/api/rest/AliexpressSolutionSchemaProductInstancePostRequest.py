'''
Created by auto_sdk on 2022.01.10
'''
from top.api.base import RestApi
class AliexpressSolutionSchemaProductInstancePostRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.developer_features = None
		self.product_instance_request = None

	def getapiname(self):
		return 'aliexpress.solution.schema.product.instance.post'
