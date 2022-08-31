import metoffer
# I was mainly using this to check weather for local skateparks
# Sign up for a met office datapoint account (for free!)
# You can then get an API key once registered
api_key = "ce0d4a4a-cdc8-4e94-90ba-ae09bc4040e5"

M = metoffer.MetOffer(api_key)

# I was mainly using this to check weather for local skateparks...

# M32 51.471869541617664, -2.5628872819068595
# Warmley/Cadbury Heath 51.46126335502879, -2.473647799851539
# Bradley Stoke 51.53631245052903, -2.5451194440253953
# Daveside (Bristol City FC) 51.444700, -2.616010
# Dean lane (Bedminster) 51.444890, -2.598120

# location currently set to: Bedminster, Bristol, UK.
x = M.nearest_loc_forecast(51.444890, -2.598120, metoffer.DAILY)
y = metoffer.Weather(x)

# Print the location
print(y.name)
print(y.country)
print("\n")

# Day and night system is a bit janky, but it works...
night = 1
day = 0
for i in y.data:

    print("{} - {}".format(i["timestamp"][0],
          metoffer.WEATHER_CODES[i["Weather Type"][0]]))
    if day % 2 == 0:
        print("Day Maximum Temperature: ",
              y.data[day]["Day Maximum Temperature"][0])
        print("Feels Like Day Maximum Temperature: ",
              y.data[day]["Feels Like Day Maximum Temperature"][0])

    if night % 2 == 0:
        print("Night Minimum Temperature: ",
              y.data[day]["Night Minimum Temperature"][0])
        print("Feels Like Night Minimum Temperature: ",
              y.data[day]["Feels Like Night Minimum Temperature"][0])
        print("\n")

    day += 1
    night += 1
