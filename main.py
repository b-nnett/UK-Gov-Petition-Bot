import requests, random, threading
from colorama import Fore

with open("first_names.txt", "r") as f:
	first_names = f.read().splitlines()
	
with open("first_names.txt", "r") as f:
	postcodes = f.read().splitlines()
	
class petition:
	def __init__(self):
		self.session = requests.Session()

		self.petition_id = 643008
		self.catchall = "iclouw.com"
		
		self.name = random.choice(first_names)
		self.postcode = random.choice(postcodes)

		self.email = f"{self.name.lower()}{random.randint(1, 99)}@{self.catchall}"

		self.headers = {
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
			'Accept-Language': 'en-GB,en;q=0.9',
			'Cache-Control': 'max-age=0',
			'Connection': 'keep-alive',
			'Host': 'petition.parliament.uk',
			'Origin': 'https://petition.parliament.uk',
			'Referer': f'https://petition.parliament.uk/petitions/{self.petition_id}/signatures/new',
			'Sec-Fetch-Dest': 'document',
			'Sec-Fetch-Mode': 'navigate',
			'Sec-Fetch-Site': 'same-origin',
			'Sec-Fetch-User': '?1',
			'Upgrade-Insecure-Requests': '1',
			'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
			'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
			'sec-ch-ua-mobile': '?0',
			'sec-ch-ua-platform': '"macOS"',
			'Content-Type': 'application/x-www-form-urlencoded',
		}

		self.first_load()

		if self.load_register() == True:
			if self.initiate_signature() == True:
				self.submit_signature()
	
	def first_load(self):
		response = self.session.get(f'https://petition.parliament.uk/petitions/{self.petition_id}', headers=self.headers)
		
		if response.status_code == 200:
			print(Fore.GREEN + f"[Success] Loaded petition {self.petition_id} successfully")
			return True
		
		else:
			print(Fore.RED + f"[Error] Failed to load petition {self.petition_id}, status code: {response.status_code}")
		
	def load_register(self):
		cookies = {
			'seen_cookie_message': 'yes',
		}

		response = self.session.get(f'https://petition.parliament.uk/petitions/{self.petition_id}/signatures/new', cookies=cookies, headers=self.headers)
		
		self.auth_token = response.text.split('name="authenticity_token" value="')[1].split('"')[0]
		
		# check to see if the auth_token is valid, if it's not - just move on...
		
		if len(self.auth_token) > 100:
			print(Fore.RED + f"[Error] Failed to initiate signature for petition {self.petition_id}, status code: {response.status_code}")    

			return False

		return True

		
	def initiate_signature(self):		
		data = {
			'authenticity_token': self.auth_token,
			'signature[autocorrect_domain]': '1',
			'signature[uk_citizenship]': [
				'0',
				'1',
			],
			'signature[name]': self.name,
			'signature[email]': self.email,
			'signature[location_code]': 'GB',
			'signature[postcode]': self.postcode,
			'signature[notify_by_email]': [
				'0',
				'1',
			],
			'move:next': 'Continue',
		}

		response = self.session.post(f'https://petition.parliament.uk/petitions/{self.petition_id}/signatures/new', headers=self.headers, data=data)
		
		self.auth_token = response.text.split('name="authenticity_token" value="')[1].split('"')[0]
		
		# Basic error handling to see if the auth_token is valid, if it's not - just move on...
		
		if len(self.auth_token) > 100:
			print(Fore.RED + f"[Error] Failed to initiate signature for petition {self.petition_id}, status code: {response.status_code}")    
			
			# print(response.text)
						
			return False
		
		return True
		
	def submit_signature(self):
		data = {
			'authenticity_token': self.auth_token,
			'signature[name]': self.name,
			'signature[uk_citizenship]': '1',
			'signature[postcode]': self.postcode,
			'signature[location_code]': 'GB',
			'signature[notify_by_email]': '1',
			'signature[email]': self.email,
			'commit': 'Yes – this is my email address',
		}

		response = self.session.post(f'https://petition.parliament.uk/petitions/{self.petition_id}/signatures', headers=self.headers, data=data)
		
		if "Please click on the link in the email to confirm your address." in response.text:
			print(Fore.GREEN + f"[Success] Signed petition (Email: {self.email})")
			
		else:
			print(Fore.RED + f"[Failed] Failed to sign petition (Email: {self.email}) (Status Code: {response.status_code})")

			print(response.text)
			
			print

def thread_main():
	while(True):
		petition()

for i in range(0, 1):
	t = threading.Thread(target=thread_main).start()