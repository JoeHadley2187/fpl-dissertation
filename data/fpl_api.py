import requests


class FplApi:
    def __init__(self):
        self.BASE_URL = "https://fantasy.premierleague.com/api"

    def get_bootstrap(self):
        try:
            response = requests.get(f"{self.BASE_URL}/bootstrap-static/")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError:
            print("Error retrieving bootstrap static data, HTTP Status Code: ", response.status_code)
        except requests.exceptions.RequestException as e:
            print("Request failed:", e)
        return None

    def get_players(self):
        data = self.get_bootstrap()
        if data:
            return data.get("elements", [])
        return []

    def get_player_summary(self,id):
        try:
            response = requests.get(f"{self.BASE_URL}/element-summary/{id}/")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError:
            print("Error retrieving player summery data, HTTP Status Code: ", response.status_code)
        except requests.exceptions.RequestException as e:
            print("Request failed:", e)
        return None

    def get_fixtures(self):
        try:
            response = requests.get(f"{self.BASE_URL}/fixtures/")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError:
            print("Error retrieving fixtures data, HTTP Status Code: ", response.status_code)
        except requests.exceptions.RequestException as e:
            print("Request failed:", e)
        return None

    def get_id_top_10k_managers(self,page):
        try:
            response = requests.get(f"{self.BASE_URL}/leagues-classic/314/standings/?page_standings={page}")
            response.raise_for_status()
            data = response.json()
            return data.get("standings", {}).get("results", [])
        except requests.exceptions.HTTPError:
            print("Error retrieving leagues classic data, HTTP Status Code: ", response.status_code)
        except requests.exceptions.RequestException as e:
            print("Request failed:", e)
            return None

    def get_managers_picks_for_gw(self,id,gw):
        try:
            response = requests.get(f"{self.BASE_URL}/entry/{id}/event/{gw}/picks/")
            response.raise_for_status()
            data = response.json()
            return data.get("picks", [])
        except requests.exceptions.HTTPError:
            print("Error retrieving manager picks, HTTP Status Code: ", response.status_code)
        except requests.exceptions.RequestException as e:
            print("Request failed:", e)
            return None





