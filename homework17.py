import json

import requests
from django.http import JsonResponse
from django.urls import path


def post_current_market_state(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))

        from_currency = data["USD"]
        to_currency = data["EUR"]

        url = f"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={from_currency}&to_currency={to_currency}&apikey=6I2HOYT0DOXGAH5T"

        try:
            response: str = requests.get(url, timeout=10)
            response.raise_for_status()

            rate = (
                response.json()
                .get("Realtime Currency Exchange Rate", {})
                .get("5. Exchange Rate")
            )
            if rate is None:
                return JsonResponse(
                    {"error": "Не удалось получить курс обмена"}, status=500
                )

            return JsonResponse({"rate": rate})
        except requests.RequestException as e:
            return JsonResponse(
                {"error": f"Ошибка при запросе к внешнему API: {str(e)}"}, status=500
            )
    else:
        return JsonResponse({"error": "Метод не разрешен"}, status=405)


urlpatterns = [
    path(route="post-current", view=post_current_market_state),
]
