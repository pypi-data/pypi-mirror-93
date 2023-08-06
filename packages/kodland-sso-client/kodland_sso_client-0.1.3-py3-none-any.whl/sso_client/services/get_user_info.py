import json
from typing import Any

import requests
from django.conf import settings


class GetUserInfo(object):
	"""
	request to sso server to get user's info
	"""
	
	@staticmethod
	def get_info(access_token: str) -> dict:
		url = f'{settings.SSO_URL}info'
		
		headers = {
			'Authorization': 'Bearer {}'.format(access_token)
		}
		
		response = requests.get(url, headers=headers)
		
		if response.status_code == 200:
			info = json.loads(response.text)
			return info
		else:
			return {}
		
	@staticmethod
	def get_student_info_by_param(user_id: int, param_name: str) -> Any:
		url = f'{settings.SSO_URL}student_info'
		data = {
			'user_id': user_id,
			'param': param_name
		}
		response = requests.post(url, data=data)

		if response.status_code == 200:
			info = json.loads(response.text)
			return info.get('value')
