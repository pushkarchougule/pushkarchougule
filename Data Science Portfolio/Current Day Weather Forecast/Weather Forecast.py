# Purpose: This program uses an API to obtain current weather data from
# openweathermap website, using user's input like "city, state" or "zip code"
# Author: Pushkar Chougule

import requests

url = "https://api.openweathermap.org/data/2.5/weather"  # base url
# USE a Valid and Active API key relevant for your account
apikey = "8e3839687c6c8caea0bb0095c94b92b6"  # API key   

# below query is used in the weather API call for zip code option
query = {"zip": "00000",
         "country": "US",
         "units": "imperial",
         "APPID": apikey}

headers = {"cache-control": "no-cache"}


########## Current weather retrieval based on City name input ##########

def weather_city_name():
    """this function uses city name to retrieve weather information. along
    with city name, state code, country code can also be used"""

    city_name = input("Pls provide city name:\t")  # accept user input

    # in below statements, we are forming the url1 variable by leveraging the
    # common initial part from 'url' variable and plugging in the city name and
    # api key in the standard url format to be passed down to requests module

    url1 = f"{url}?q={city_name},&units=imperial&appid={apikey}"
    status_city_det = ''  # error details variable initialized

    # below try / except block is used for checking the response from the GET
    # request processing and raising exceptions in case of errors encountered

    try:
        resp_city = requests.request("GET", url1)

    except Exception as exc:
        status_city_det = exc

    status_city = resp_city.status_code  # status code variable

    # below conditional block statements are used to print out the formatted
    # current weather information in case of successful retrieval. In other
    # cases, appropriate error handling is done, using error_handle function.
    # zip code not found error is handled here itself.

    if status_city == requests.codes.ok:
        r_city = resp_city.json()
        weather_print(r_city)
    elif resp_city.status_code == 404:
        print(90 * 'x')
        print("Invalid City / location not found. Please try with valid place")
        print(90 * 'x')
    else:
        error_handle(status_city, status_city_det)


########## Current weather retrieval based on Zip Code input ##########

def weather_zip_code():
    """this function uses US zip code to retrieve weather information.
    an error will be displayed for non US zip codes"""

    zip_code = input("Please provide zip code:\t")

    process_zip = False  # boolean used for weather API call determination

    # below try / except block checks if a valid 5 digit numeric zip code value
    # is provided by the user. if not, then appropriate exceptions are printed.
    # Using only the simple zip code validation for numeric data and length of
    # 5 is performed.

    try:
        if 0 < int(zip_code) <= 99999 and len(zip_code) == 5:
            process_zip = True
        else:
            print("ONLY US Zip codes - 5 digit numeric format are acceptable")
    except ValueError:
        print("********** Not a valid 5 digit numeric zip code value *****")
    except Exception as e:
        print(f"********** An error encountered with zip code value: {e}")

    # below block of code is to set the weather API call parameters and GET
    # the response as well as status code - error handling and a call to
    # the function printing out the current weather information

    if process_zip:

        status_zip_det = ''  # error details variable
        query["zip"] = zip_code  # stores valid zip code to query dictionary

        # below try / except block is used for checking the response from the GET
        # request processing and raising exceptions in case of errors encountered

        try:
            resp_zip = requests.request("GET", url, headers=headers,
                                        params=query)

        except Exception as exc:
            # the exception details stored and later passed into error_handle()
            status_zip_det = exc

        status_zip = resp_zip.status_code  # status code variable

        # below conditional block statements are used to print out the formatted
        # current weather information in case of successful retrieval. In other
        # cases, appropriate error handling is done, using error_handle function.
        # zip code not found error is handled here itself.

        if status_zip == requests.codes.ok:
            r_zip = resp_zip.json()
            weather_print(r_zip)
        # not found error handling using response reason value, text err
        elif resp_zip.reason == 'Not Found':
            print(90 * 'x')
            print("Invalid Zip code / not found. Please try valid US Zip code")
            print(90 * 'x')
        else:
            error_handle(status_zip, status_zip_det)


def weather_print(resp_json):
    """this function prints out formatted weather information"""

    print(f"{90 * '*'}")
    print(f"Current weather conditions for {resp_json['name']}:")
    print(f"Current Temp:\t {resp_json['main']['temp']} degrees")
    print(f"High Temp\t:\t {resp_json['main']['temp_max']} degrees")
    print(f"Low Temp\t:\t {resp_json['main']['temp_min']} degrees")
    print(f"Pressure\t:\t {resp_json['main']['pressure']} hPa")
    print(f"Humidity\t:\t {resp_json['main']['humidity']} %")
    print(f"Description\t:\t {resp_json['weather'][0]['description']}")
    print(f"Clouds\t\t:\t {resp_json['clouds']['all']} %")
    print(f"{90 * '*'}")


# error handling function to deal with various error messages

def error_handle(err_resp_cd, err_resp_det):
    """this is error handling function to navigate through known standard
    error response codes and display appropriate message for end user"""

    print(90 * 'x')

    # below error message can also be handled with error text 'Bad Request'
    if err_resp_cd == 400:
        print("Request cannot be completed due to bad syntax / input")
    # below error message can also be handled with error text 'Unauthorized'
    elif err_resp_cd == 401:
        print("Unauthorized request. Please check authorization key")
    # below error message can also be handled with text 'Internal Server error'
    elif err_resp_cd == 500:
        print("Server encountered unexpected error in processing request")
    # below error message can also be handled with text 'Service Unavailable'
    elif err_resp_cd == 503:
        print("Server unable to handle the request currently, try later")
    else:
        print("error {} encountered".format(err_resp_det))

    print(90 * 'x')


def main():
    """main() function controls the program flow"""

    # Below block of code displays welcome message and the main menu options
    # to choose from, along with acceptable format for each of the options.

    print(140 * '-')
    print("Welcome to Weather Info services powered by openweathermap.org".center(140))
    print("Please read through the following menu and select the option".center(140))
    print(140 * '-')
    print("1. To find weather by using US city name, please enter 1.\t Allowed"
          " formats: CityName or CityName,State or CityName,State,Country")
    print("2. To find weather by using US zip code, please enter 2.\t Allowed"
          " formats: ZipCode - 5 digit numeric. Country code not required")
    print("3. If you wish to quit, please enter q/Q. Any other responses "
          "are not considered valid")
    print(140 * '-')

    option = input().upper()  # accepting the user input

    # This while loop, controls the calls to the appropriate function to fetch
    # the weather information for a given location - city name or zip code.
    # Input option of 1 or 2 will process accordingly and q/Q will stop the
    # processing. Any other values will display error message and prompt
    # the user to provide the valid option.

    while True:

        if option == "1":
            weather_city_name()
        elif option == "2":
            weather_zip_code()
        elif option == 'Q':
            print("Thank you for using our services. Good bye for now")
            break
        else:
            print("xxxxxxxxxx     Invalid option selected     xxxxxxxxxx")

        # accept the user input for determining whether to perform the next
        # iteration or to exit from the weather retrieval services

        option = input("Please choose from option 1 or 2 to continue, q/Q"
                       " to quit the weather retrieval process:\t").upper()


# execute the main() function from within the program file
if __name__ == '__main__':
    main()
