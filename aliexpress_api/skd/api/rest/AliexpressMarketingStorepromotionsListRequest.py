'''
Created by auto_sdk on 2019.07.08
'''
from top.api.base import RestApi
class AliexpressMarketingStorepromotionsListRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.promotion_query_dto = None

	def getapiname(self):
		return 'aliexpress.marketing.storepromotions.list'
