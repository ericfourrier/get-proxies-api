#!/usr/bin/env python
# -*- coding: utf-8 -*-u

""" 
author = efourrier 

Purpose : this is a small python wrapper for theproxisright.com/api/ , get more info 
on  https://theproxisright.com/

You need to get your api key, and your are limited to 10 calls per day 

You can check your proxy with another proxy provider : http://proxyipchecker.com/#buyvpn
"""



#########################################################
# Import Packages and helpers 
######################################################### 

import os 
import json
import codecs # proper way to write utf-8 encoded file even if the response here are ascii compatible
import pickle

import requests 



#apikey = os.environ.get('PROXY_API_KEY')

# maxResults is 250 maximum 

# default_parameters = {'apiKey':apikey,'onlyActive':True,'onlyHttps':True,'onlyHighAvailLowLatency':True,
# 					#'onlySupportsGoogle':True,'onlySupportsAmazon':True,
# 					# 'onlySupportsCraigslist':True,'onlySupportsTripAdvisor':True,'onlySupportsKayak':True,
# 					'minimumUptimePercentage':99,#'countryCodes':"US",
# 					'onlyHighAnonymity':True,'maxResults':250,'sortByLatestTest':True}


#########################################################
# Main functions 
######################################################### 

class GetProxies(object):
	""" This is a class to get proxies via the theproxisright.com/api/ and process them 
	in order to get the right format for the proxies parameter of the requests package """


	daily_limit = 10
	nb_calls = 0

	def __init__(self,apikey=None):
		self.apikey = apikey
		self.default_parameters = {'apiKey':self.apikey,'onlyActive':True,'onlyHttps':True,'onlyHighAvailLowLatency':True,
					#'onlySupportsGoogle':True,'onlySupportsAmazon':True,
					# 'onlySupportsCraigslist':True,'onlySupportsTripAdvisor':True,'onlySupportsKayak':True,
					'minimumUptimePercentage':99,#'countryCodes':"US",
					'onlyHighAnonymity':True,'maxResults':250,'sortByLatestTest':True,
					#lastTestedHourLimit={lastTestedHourLimit}
					}

	def get_proxies(self,params = None,save_json = None,add_rp = True,**kwargs):

		"""
		add additionnal parameter to the api call (we put params = default_parameters)

		Arguments
		---------
		params : a dictionnary of params put default parameter for consistent get_proxies
		apikey : Your secret apikey, default taken from your environnmemnt variables
		add_rp: add the requests way to declare proxy into the raw json response object 
		**kwargs : to add additionnal parameters to request example : 
		get_proxies(countryCodes="US")

		Returns
		-------
		raw json response from the api 

		"""
		if not params:
			params = self.default_parameters
		for k,v in kwargs.items():
			params[k] = v 
		json_response =  requests.get('https://theproxisright.com/api/proxy/get',params=params).json()
		self.nb_calls += 1
		if add_rp:
			for p in json_response['list']:
				p[u'requests_proxy'] = {u'http':p['type'] + u'://' + p['host'],u'https':p['type'] + u'://' + p['host']}
		if save_json:
			with codecs.open(save_json, 'wb', encoding ='utf-8') as f :
				json.dump(json_response,f,ensure_ascii=False)
		return json_response

	def process_json_dict(self,json_response,save_file = None):
		""" 
		Process the json response from theproxisright api into a text file where 
		each line is a dictionnary : 'ip_adress:port'

		"""
		proxies_dict  =  [{u'http':p['type'] + u'://' + p['host'],u'https':p['type'] + u'://' + p['host']} for p in json_response['list']]
		if save_file:
			with codecs.open(save_file,'wb',encoding='utf-8') as f :
				pickle.dump(proxies_dict,f)
		return proxies_dict

	def process_json_text(self,json_response,save_file = None):
		""" 
		Process the json response from theproxisright api into a text file where 
		each line is 'ip_adress:port'

		"""
		list_ip_address  = [p['host'] for p in json_response['list']]
		if save_file:
			with codecs.open(save_file,'wb',encoding='utf-8') as f :
				f.write("\n".join(list_ip_address))
		return list_ip_address




# if __name__ == "__main__":
# 	gp = GetProxies(apikey=apikey)
# 	proxy_world = gp.get_proxies(save_json="list_https_world_proxies3.json")
# 	proxies_dict_world = gp.process_json_dict(proxy_world,save_file="list_https_world_proxies_test.p")
# 	proxy_us = get_proxies(default_parameters,save_json="list_https_us_proxies.json",countryCodes="US")
# 	process_json(proxy_us,save_file="list_https_us_proxies.txt")
