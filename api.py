import requests

# THIS FUNCTION MAKES A GET REQUEST TO THE data.gov.sg API AND STORES THE RESPONSE TO A LIST AND CLEANS IT
##################################################################################
def get_api():
    try:
        api_url = "https://api.data.gov.sg/v1/transport/carpark-availability"   # GRABS THE DATA FROM THE URL (THE API)

        response = requests.get(api_url)

        if response.status_code == 200:  # 200 INDICATES THAT IT WAS SUCCESSFUL
            data = response.json()

            timestamp = data["items"][0]["timestamp"]
            carpark_data = data["items"][0]["carpark_data"]

            with open('api-carpark-availability.csv', 'w') as f:

                # WRITE THE HEADERS
                output_string = f"Timestamp: {timestamp}\nCarpark Number,Total Lots,Lots Available\n"

                # WRITE THE INFORMATION
                for entry in carpark_data:
                    carpark_number = entry["carpark_number"]
                    total_lots = entry["carpark_info"][0]["total_lots"]
                    lots_available = entry["carpark_info"][0]["lots_available"]
                    output_string += f"{carpark_number},{total_lots},{lots_available}\n"
                
                f.write(output_string)

        # IF RESPONSE CODE IS NOT 200 (NOT SUCCESSFUL)
        else:
            print("\nError: Unable to fetch data from the API!")

    # IF UNABLE TO CONNECT TO THE API/URL
    except:
        print("\nError, Maybe its a wifi problem?")

    # RETURNS THE FILE NAME FOR FUTURE REFERENCE
    return 'api-carpark-availability.csv'              
##################################################################################
