'''
Created by auto_sdk on 2020.05.20
'''
from top.api.base import RestApi
class AliexpressPostproductRedefiningEditproductcategoryattributesRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.product_category_attributes = None
		self.product_id = None

	def getapiname(self):
		return 'aliexpress.postproduct.redefining.editproductcategoryattributes'
