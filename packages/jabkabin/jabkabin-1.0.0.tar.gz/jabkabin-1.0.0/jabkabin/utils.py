class Utils(object):
    @staticmethod
    def getPasteKey(url: str):
        return url.split("/")[-1].strip()