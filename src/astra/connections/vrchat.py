import vrchatapi

from vrchatapi.api.users_api import UsersApi

class VRChatConnector:
    
    @staticmethod
    async def search_user(**kwargs):
        # wrapper for vrchatapi.api.users_api.UsersApi.search_users
        with vrchatapi.ApiClient() as api_client:
            api_client.user_agent = "AstraSE/1.4.0"
            users_api = UsersApi(api_client)
            return users_api.search_users(**kwargs)