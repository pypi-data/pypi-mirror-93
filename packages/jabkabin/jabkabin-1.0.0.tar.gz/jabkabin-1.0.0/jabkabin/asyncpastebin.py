import aiohttp

class SyncPasteBin(object):
    def __init__(self, API_key: str):
        self.__APIKey = API_key
        self.APIURL = "https://pastebin.com/api/api_post.php"
        self.APIURLLOGIN = "https://pastebin.com/api/api_login.php"
        self.APIURLRAW = "https://pastebin.com/api/api_raw.php"
        self.__userKey = None
    
    async def newPaste(self, code: str, api_paste_name: str, api_paste_format: str = None, api_paste_private: int = 0, api_folder_key = None, api_paste_expire_date = "N"):
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
        async with aiohttp.ClientSession() as session:
            async with session.post(self.APIURL, data) as r:
                return await r.text()

    async def getNewUserKey(self, username: str, password: str):
        async with aiohttp.ClientSession() as session:
            async with session.post(self.APIURLLOGIN, data={"api_dev_key": self.__APIKey, "api_user_name": username, "api_user_password": password}) as r:
                self.__userKey = await r.text()
        
        return "Success"
    
    async def listenUserPastes(self, api_results_limit: int):
        if not self.__userKey:
            return "Generate user key using getNewUserKey(username, password)"
        
        async with aiohttp.ClientSession() as session:
            async with session.post(self.APIURL, data={"api_dev_key": self.__APIKey, "api_user_key": self.__userKey, "api_results_limit": api_results_limit, "api_option": "list"}) as r:
                return await r.text()

        

    async def deletePaste(self, api_paste_key: str):
        if not self.__userKey:
            return "Generate user key using getNewUserKey(username, password)"


        async with aiohttp.ClientSession() as session:
            async with session.post(self.APIURL, data={"api_dev_key": self.__APIKey, "api_user_key": self.__userKey, "api_paste_key": api_paste_key, "api_option": "delete"}) as r:
                return await r.text()

    async def getInfo(self):
        if not self.__userKey:
            return "Generate user key using getNewUserKey(username, password)"
        
        async with aiohttp.ClientSession() as session:
            async with session.post(self.APIURL, data={"api_dev_key": self.__APIKey, "api_user_key": self.__userKey, "api_option": "userdetails"}) as r:
                return await r.text()

    async def getRawPrivatePastes(self, api_paste_key: str):
        if not self.__userKey:
            return "Generate user key using getNewUserKey(username, password)"
        
        async with aiohttp.ClientSession() as session:
            async with session.post(self.APIURLRAW, data={"api_paste_key": api_paste_key, "api_user_key": self.__userKey, "api_dev_key": self.__APIKey, "api_option": "show_paste"}) as r:
                return await r.text()


    async def getRawPaste(self, api_paste_key: str):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://pastebin.com/raw/{api_paste_key}") as r:
                return await r.text()