import requests

class SyncPasteBin(object):
    def __init__(self, API_key: str):
        self.__APIKey = API_key
        self.APIURL = "https://pastebin.com/api/api_post.php"
        self.APIURLLOGIN = "https://pastebin.com/api/api_login.php"
        self.APIURLRAW = "https://pastebin.com/api/api_raw.php"
        self.__userKey = None
    
    def newPaste(self, code: str, api_paste_name: str, api_paste_format: str = None, api_paste_private: int = 0, api_folder_key = None, api_paste_expire_date = "N"):
        data = {
            "api_dev_key": self.__APIKey,
            "api_option": "paste",
            "api_paste_code": code,
            "api_paste_name": api_paste_name,
            "api_paste_private": api_paste_private,
            "api_paste_expire_date": api_paste_expire_date
        }
        if api_paste_format:
            data["api_paste_format"] = api_paste_format
        if api_folder_key:
            data["api_folder_key"] = api_folder_key
        responce = requests.post(self.APIURL, data)
        return responce.text

    def getNewUserKey(self, username: str, password: str):
        self.__userKey = requests.post(self.APIURLLOGIN, data={"api_dev_key": self.__APIKey, "api_user_name": username, "api_user_password": password}).text
    
    def listenUserPastes(self, api_results_limit: int):
        if not self.__userKey:
            return "Generate user key using getNewUserKey(username, password)"
        
        responce = requests.post(self.APIURL, data={
            "api_dev_key": self.__APIKey,
            "api_user_key": self.__userKey,
            "api_results_limit": api_results_limit,
            "api_option": "list"
        })

        return responce.text

    def deletePaste(self, api_paste_key: str):
        if not self.__userKey:
            return "Generate user key using getNewUserKey(username, password)"

        responce = requests.post(self.APIURL, data={
            "api_dev_key": self.__APIKey,
            "api_user_key": self.__userKey,
            "api_paste_key": api_paste_key,
            "api_option": "delete"
        })

        return responce.text

    def getInfo(self):
        if not self.__userKey:
            return "Generate user key using getNewUserKey(username, password)"
        
        responce = requests.post(self.APIURL, data={
            "api_dev_key": self.__APIKey,
            "api_user_key": self.__userKey,
            "api_option": "userdetails"
        })

        return responce.text

    def getRawPrivatePastes(self, api_paste_key: str):
        if not self.__userKey:
            return "Generate user key using getNewUserKey(username, password)"
        
        responce = requests.post(self.APIURLRAW, data={
            "api_dev_key": self.__APIKey,
            "api_user_key": self.__userKey,
            "api_paste_key": api_paste_key,
            "api_option": "show_paste"
        })

        return responce.text

    def getRawPaste(self, api_paste_key: str):
        responce = requests.get(f"https://pastebin.com/raw/{api_paste_key}")
        return responce.text