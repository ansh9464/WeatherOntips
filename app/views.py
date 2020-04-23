from django.shortcuts import render
import requests
# Create your views here.
def index(request):
    return render(request,'app/index.html')
def home(request):
    city = request.GET.get('text', 'default')
    search_address='http://dataservice.accuweather.com/locations/v1/cities/search?apikey=GeGCZ346TanjSyw8QeEr6Mj2ASze7StU&q='+city+'&details=true'
    r=requests.get(search_address).json()
    if(len(r)==0):
        return render(request, 'app/error.html')
    else:
        key=r[0]["Key"]
        forecast_url='http://dataservice.accuweather.com/forecasts/v1/daily/5day/'+key+'?apikey=GeGCZ346TanjSyw8QeEr6Mj2ASze7StU&details=true'
        data=requests.get(forecast_url).json()
        i=1
        weather={}
        weather[1]={}
        weather[1]['city']=city
        for d in data['DailyForecasts']:
            weather[1][i]={}
            weather[1][i]['min_temp']=d['Temperature']['Minimum']['Value']
            weather[1][i]['max_temp']=d['Temperature']['Maximum']['Value']
            weather[1][i]['desc']=d['Day']['ShortPhrase']
            if(d['Day']['Icon']<10):
                weather[1][i]['icon']=str(0)+str(d['Day']['Icon'])
            else:
                weather[1][i]['icon']=d['Day']['Icon']
            weather[1][i]['prec']=d['Day']['PrecipitationProbability']
            i=i+1
        dit={'curr_weather':weather}
        return render(request,'app/home.html',dit)