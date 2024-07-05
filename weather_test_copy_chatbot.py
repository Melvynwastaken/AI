# import the module
import python_weather

import asyncio
import os

async def getweather():
  async with python_weather.Client(unit=python_weather.METRIC) as client:
    weather = await client.get('Amsterdam')

    print(weather.temperature)
    
    for daily in weather.daily_forecasts:
      print(daily)

      for hourly in daily.hourly_forecasts:
        print(f' --> {hourly!r}')

if __name__ == '__main__':
  if os.name == 'nt':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
  
  asyncio.run(getweather())