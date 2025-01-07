from pipeline import main
locations = ["colombo","bentota"]
hotel_list = ["CINNAMON LAKESIDE","the palms"]
start_date = "2024-11-28"
end_date = "2024-12-05"
duration = 7
pax_size = 4
print(main.generate_trip_details(locations, hotel_list, start_date,end_date,duration,pax_size)) 