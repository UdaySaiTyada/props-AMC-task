from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import pandas as pd
from django.views.decorators.csrf import csrf_exempt
import googlemaps
import xlwt

google_maps_api_key = googlemaps.Client(key="GOOGLE_API_KEY")


# Create your views here.
@csrf_exempt
def upload_csv(request):
	try:
		DataFrame = pd.read_csv('input.csv')
		DataFrame.index = range(0, DataFrame.shape[0])
		coordinates = pd.DataFrame([], index = DataFrame.index, columns = ['latitude', 'longitude'])
		# print("came here")
		for i in DataFrame.index:
			# print(i)
			result = google_maps_api_key.geocode(DataFrame.at[i, 'location'])
			coordinates.at[i,'latitude'] = result[0]["geometry"]["location"]["lat"]
			coordinates.at[i,'longitude'] = result[0]["geometry"]["location"]["lng"]
		DataFrame = pd.concat([DataFrame, coordinates], axis = 1)
		DataFrame.to_csv('output.csv', index = False)
		return JsonResponse({'response': "Success"})
	except:
		return JsonResponse({'response': "Internal server error"})
