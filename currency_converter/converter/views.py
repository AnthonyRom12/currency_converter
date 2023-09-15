import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import CurrencyRate
from .serializers import CurrencyRateSerializer


class CurrencyRateConverter(APIView):
    BASE_URL = 'https://api.frankfurter.app/latest'

    def fetch_exchange_rate(self, from_currency, to_currency, amount):
        url = f'{self.BASE_URL}?amount={amount}&from={from_currency}&to={to_currency}'
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            return data

    def get(self, request):
        from_currency = request.query_params.get('from')
        to_currency = request.query_params.get('to')
        amount = float(request.query_params.get('amount', 1))

        if not from_currency or not to_currency:
            return Response({'error': 'Invalid currency parameters!'}, status=400)

        conversion_data = self.fetch_exchange_rate(from_currency, to_currency, amount)

        if conversion_data and 'rates' in conversion_data:
            result = conversion_data['rates']
            return Response({'result': result})
        else:
            return Response({'error': "Unable to perform currency conversion!"}, status=400)



