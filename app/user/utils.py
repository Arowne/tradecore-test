import holidays
import datetime

from .models import User
from .models import Login

from ip2geotools.databases.noncommercial import DbIpCity

def ip_localisation(ip, user):
    response = DbIpCity.get("92.184.112.171", api_key='free')
    
    get_holidays = holidays.CountryHoliday(response.country) 
    today = datetime.datetime.today()

    is_holiday = today.strftime("%Y-%m-%d") in get_holidays
    
    Login.objects.create(user=user, location=response.country, is_holiday=is_holiday)