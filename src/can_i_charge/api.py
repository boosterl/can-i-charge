from shellrecharge_api import ShellRechargeApi

class Api:
    def get_api(self, api_name):
        return {
            "shellrecharge": ShellRechargeApi()
        }.get(api_name)
