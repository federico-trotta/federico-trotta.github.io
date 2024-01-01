# API documentation
This section shows how I document APIs.

:::{note}
I documented APIs for internal use only, so the following section show either APIs I developed in Python for personal projects or part of some APIs I integrated for my clients (this shows only partial code. Furtermore, refactored and created differently from the actual API).
:::

***

## Zendesk API: OAuth tokens management documentation
This section describes how I created use cases in Python for the Zendesk API and how I documented them.\
\
I created a Python program for a customer that uses the Zendesk API to manage access tokens. They needed a program that could manage access tokens on behalf of their customers to help the support team in their daily tasks, making customers do some operations for them.\
\
The complete program and documentation can't be shown, so, in this section, I recreated some of the functions, with different code, to show how I document APIs.

### Prerequisites
#### Get a Zendesk subdomain
To use the code in this section, you first need to have a [Zendesk subdomain](https://www.zendesk.com/) registered.\
\
[Here's](https://developer.zendesk.com/api-reference/) the API reference with its documentation for further basic knowledge.

#### Create an API token
After gaining a Zendesk domain with an admin account, you can create an API token as follows:

**Step 1:** Log in to your Zendesk account and go to the `Admin Center`

```{figure} images/api/4securitas_admin_center.png
:alt: The Zendesk Admin Center documentation by Federico Trotta.
:align: center

*Going to the admin center.*
```

**Step 2:** Click on `Apps and integrations` and then on `Zendesk API`

```{figure} images/api/4securitas_zendesk_api.png
:alt: The Zendesk API documentation by Federico Trotta.
:align: center

*Going to the Zendesk API.*
```

**Step 3:** Click on `Settings`. Then, enable the Token access. Finally, click on `Add API token`

```{figure} images/api/4securitas_api_token.png
:alt: The Zendesk API documentation by Federico Trotta.
:align: center

*Adding a new API token.*
```

Copy and paste the API token somewhere safe: it won't be shown again.\
\
Then, save and you're done.

#### Python prerequisites
To run the program you need:
- Python 3 or later.
- The library `requests`.

Since the library requests is not in the Python standard library, you need to install it via the command:
```python
pip install requests
```

### Use cases implementation
This section shows documentet Python code as use cases for the Zendesk API.

#### Admin authenticator
If you're working with colleagues, each colleague can be an admin, create an admin API token, and use the program.\
\
The admin authenticator program is called `initial.py`. It asks you for your:
-  Your Zendesk login email.
- API token.

After authentication, it creates a file called `settings.py` that stores your:
- Zendesk login email.
- API token.
- Client ID.

:::{note}
You'll provide your email and API token via CLI. The client ID is retrieved by the software automatically.
:::

Here's the Python code:

```python
import requests

# Define the Zendesk subdomain
ZENDESK_SUBDOMAIN = "" # Write your Zendesk subdomain

# Insert user email
email = input(f"\nPlease, insert your Zendesk login email:\n")
# Insert user API token
token = input(f"\nPlease, insert your Zendesk API token:\n")
 
def generate_settings(email, token)->None:
    """ Generates the settings.py file needed to use the main program"""
    # API request
    url = f'https://{ZENDESK_SUBDOMAIN}.zendesk.com/api/v2/oauth/clients'
    auth = (email + '/token', token)
    headers = {
    	"Content-Type": "application/json",
    }

    try:
        # Get response
        response = requests.get(url, auth=auth, headers=headers)
        # Get the clients in the JSON response
        number_of_ids = len(response.json()["clients"])
    
        # Iterate to get the client ID
        for id in range(number_of_ids):
            print(response.json()["clients"][id]["id"])
            client_id = response.json()["clients"][id]["id"]
    except Exception as e:
        print(e)

    # Write credentials to settings.py file
    with open("settings.py", "w") as settings_file:
        settings_file.write(f'EMAIL = "{email}"\n')
        settings_file.write(f'CLIENT_ID = "{client_id}"\n')
        settings_file.write(f'API_TOKEN = "{token}"\n')
        settings_file.close()
    print(f"\nSuccesfully created your settings file!")

if __name__ == "__main__":
    generate_settings(email, token)
```

#### How to create an OAuth token
This program retrieves the information of an admin stored in the `settings.py` file and:
- Gets authentication to the Zendesk API.
- Creates an OAuth token.

Your customers can use the OAuth token in other Python files you have written to authenticate them to the Zendesk API and make some actions on your behalf.\
\
For example, you may want to write a Python file that retrieves the logs on a customer machine and loads them on a Zendesk ticket; let's call it `operator.py`. To load them on a Zendesk ticket you need to authenticate your customer and you can safely do so via a OAuth token.\
\
Here's the code:

```python
import base64
import json
import requests
import settings


# Define the Zendesk subdomain
ZENDESK_SUBDOMAIN = "" # Write your Zendesk domain

# Retrieve info from the settings file
email = settings.EMAIL
token = settings.API_TOKEN
client_id = settings.CLIENT_ID
auth = (email + '/token', token)

def generate_token(client_id:str, auth:str)->base64:
    """Creates an OAuth Token for the Zendesk API"""
    
    # API request to generate a new token
    url = f"https://{ZENDESK_SUBDOMAIN}.zendesk.com/api/v2/oauth/tokens.json"

    headers = {
        "Content-Type": "application/json"
    }

    data = {
        "token": {
            "client_id": client_id,
            "scopes": ["read", "write"]
        }
    }

    response = requests.post(url, headers=headers, json=data, auth=auth)
    
    # Get token ID
    oauth_id = str(response.json()["token"]["id"])
    # Get full token
    oauth_token = str(response.json()["token"]["full_token"])

    # Insert ticket number
    zendesk_ticket_number = input(f"Insert the Zendesk Ticket number: ")

    # Mix ticket number, token id, and full token
    clear_text_msg = f"{zendesk_ticket_number}:{oauth_id}:{oauth_token}"
    # Encode the mixed values
    encoded_msg = base64.b64encode(clear_text_msg.encode('utf-8')).decode('utf-8')

    # Return the mixed values
    print("\nHere's your new token!\n")
    return encoded_msg
    
if __name__ == "__main__":
    generate_token(client_id, auth)
```

#### How to revoke active OAuth tokens
When you create OAuth tokens, they will remain stored in the web server, taking space.\
\
It is a good practice to revoke all the active tokens, from time to time. \
\
The following program revokes all the active tokens:

```python
import json
import requests
import settings


# Define the Zendesk subdomain
ZENDESK_SUBDOMAIN = "" # Write your Zendesk domain

# Retrieve info from the settings file
email = settings.EMAIL
token = settings.API_TOKEN
client_id = settings.CLIENT_ID
auth = (email + '/token', token)

def revoke_all_tokens(auth:str)->None:
    """Revokes all the OAuth Tokens generated for the Zendesk API"""

    # API request to revoke all the tokens
    url = f"https://{ZENDESK_SUBDOMAIN}.zendesk.com/api/v2/oauth/tokens.json"

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers, auth=auth)

    # Calculate the number of existing tokens
    number_of_tokens = len(response.json()["tokens"])

    # Store response to a variable
    response_json = response.json()

    # Iterate to revoke all the existing tokens
    for arrayn in range(number_of_tokens):
        token_id = response_json["tokens"][arrayn]["id"] # Get token id
        url = f'https://{ZENDESK_SUBDOMAIN}.zendesk.com/api/v2/oauth/tokens/{token_id}.json'
        response = requests.delete(url, auth=auth) # Revoke tokens

        # Verify response
        try: 
            if response.status_code == 204:
                print("\nAll the tokens been revoked!\n")
            else:
                print("\nThere was a problem while revoking the tokens!\n")
        except Exception as e:
            print("\nAn exception occurred: ", e)
            
if __name__ == "__main__":
    revoke_all_tokens(auth)
```

***

## Beam API: training a Machine Learning model on a serverless GPU
[Beam](https://www.beam.cloud/) is a service that provides Data Scientists and Developers the possibility to run code on a serverless GPU, utilizing their REST API.\
\
I had the possibility to collaborate with them to [their documentation](https://docs.beam.cloud/getting-started/introduction), creating a use case that describes:
- What are serverless GPUs and why they're revolutionizing the world of data in terms of development.
- How to log in and install the beam CLI on a Linux machine (or, via WSL in Windows).
- A use case on how to train a Machine Learning model on the Beam serverless GPU, using its API.

Read the complete use case [here](https://levelup.gitconnected.com/accelerating-ai-how-serverless-gpus-are-revolutionizing-model-training-af14dd978d64).

***

## CoinGecko API: getting crypto values
This section describes a use case for the CoinGecko API.\
\
This use case has been developed by me in Python and the full code is on my [GitHub](https://github.com/federico-trotta/crypto_prices_API).

### Prerequisites
To use the CoinGecko API you first need to create an account on [their website](https://www.coingecko.com/).\
\
Then, you need to create an [API token](https://apiguide.coingecko.com/getting-started/getting-started). The [free plan](https://www.coingecko.com/en/api/pricing) currently allows you to make 10k API calls per month.

### Requirements
The program uses the `match` statement that, and, at the time of writing this documentation (November 2023), this requires `Python 3.10` (or newer versions).\
\
As the program calls an API, you also need the `requests` library. You can install it via:

```python
pip install requests
```

### Getting started
When you use this software you need to launch the `initial.py` file via:

```python
python3 initial.py
```

This will create a file, called `settings.py`, which stores your email and your API token: this way, every time you use this software, you won't need to insert them.\
\
After that, you can launch the main file via:

```python
python3 main.py
```

Here's how the `initial.py` file works (code reference [here](https://github.com/federico-trotta/crypto_prices_API/blob/main/initial.py)):
- The user inserts the email and the API KEY via CLI.
- The program checks if the `settings.py` file exists in the settings folder, then:
    - If exists, it warns the user that the file already exists. 
    - If it doesn't exist, it creates it and stores the email and the API KEI inserted by the user.

### Structure of the main file
After the first usage, always invoke the main file via:

```python
python3 main.py
```

Here's what it does:
1. It imports the email and the API token from the `settings.py` file.
2. It prints a welcome message reporting the version of the software.
3. It tries to authenticate the user.
4. With a `while` loop, it has a menù that gives the user to choose between three options:
    - **Option 1**: the user can visualize the price of one crypto in a currency of their choice. Also, the user can choose to store the value of the crypto in a CVS file with the current date.
    - **Option 2**: the user can visualize the difference between today's and yesterday's price of a crypto.
    - **Option 0**: it closes the program by breaking the loop.

Here we document all the functions used.

#### The authentication function
The authentication function authenticates the user by verifying their email che API token.\
\
This is a use case of the `GET/ping` method shown in the [documentation](https://www.coingecko.com/api/documentation).\
\
This method has no parameters and returns 200 if the authentication is successful.\
\
In Python, we can test it as follows:

```python
# Try access by pinging the dedicated URL
try:
    ping_url = "https://api.coingecko.com/api/v3/ping"
    response = requests.get(url=ping_url, auth=auth)
    if response.status_code == 200:
        print(f"\nAccess succesfully granted to the API!")
    else:
        print(f"\nAn error occurred while autenticating. Please: try again!")
except Exception as e:
    print(f"\nAn exception occurred:", e)
```

Were the authentication is performed from the email and the API token imported from the `settings.py` file like so (complete code reference [here](https://github.com/federico-trotta/crypto_prices_API/blob/main/main.py)):

```python
# Import settings from the settings file
email = settings.EMAIL
token = settings.API_TOKEN
auth = (email + "/token", token) # Create authenticator
```

#### The `price` module
[This module](https://github.com/federico-trotta/crypto_prices_API/blob/main/functions/price.py) has two functions that retrieve the price of a currency using the API and make some calculations.
The function `visualize_price()` calls the API using the `GET/simple/price` method. 
Here's how this method can be used to show the current price of one crypto with respect to a currency:

```python
def visualize_price(auth:str)->None:
    """Shows the current price of a crypto with respect to a currency.
    The auth variable is created in the main.py file.
    """
     # User inserts crypto and currency
    crypto = input(f"\nChoose your crypto (for example, write 'bitcoin'):\n")
    currency = input(f"Choose the currency (for example, write 'usd'):\n")
   
    # API call
    url_price = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto}&vs_currencies={currency}"

    response = requests.get(url=url_price, auth=auth)

    # Print current price of a crypto in the selected currency
    try:
        if response.status_code == 200:
            data = response.json()
            print(f"\nThe current price for {crypto} is: {data[crypto][currency]: .1f} {currency}")
        else:
            print(f"An error occurred while getting the price: please, try again!")
     except Exception as e:
        print(f"An exception occurred while trying to get the currency value", e)
```

For example, suppose we want to know the current price of bitcoin in USD. Here's what you'll see:

```{figure} images/api/coingecko_price.png
:alt: An image of the program by Federico Trotta.
:align: center

*The current price of bitcoin in USD ($).*
```

The function `price_change()` calls the API using the `GET/coins/{id}/market_chart` method. \
\
Here's how this method can be used to calculate the current price of a crypt with respect to a currency and its yesterday's price. We can also calculate the change in price during the day and print it:

```python
def price_change(auth:str)->None:
    '''Shows the difference of the price of a crypto in a currency with respect to the value it had yesterday.
    The auth variable is created in the main.py file.
    '''

    # User inserts crypto and currency
    crypto = input(f"\nChoose your crypto (for example, write 'bitcoin'):\n")
    currency = input(f"Choose the currency (for example, write 'usd'):\n")

    # API call
    url_increment = f"https://api.coingecko.com/api/v3/coins/{crypto}/market_chart?vs_currency={currency}&days=1&interval=daily"

    response = requests.get(url=url_increment, auth=auth)

    try:
        if response.status_code == 200:
            data = response.json()
            current_value = data["prices"][1][1]
            yesterday_value = data["prices"][0][1]
            change_price = current_value - yesterday_value
            print(f"\nThe current value of {crypto} is {current_value: .1f} {currency} while yesterday's value was {yesterday_value: .1f} {currency}.\nSo, the price has changed by {change_price: .1f} {currency} from yesterday")
        else:
            print(f"An error occurred while getting the price: please, try again!")
    except Exception as e:
        print(f"An exception occurred while trying to get the currency value", e)
```

For example, suppose we want to know the price of Ethereum in EUR. We'd get the following:

```{figure} images/api/coingecko_price_difference.png
:alt: An image of the program by Federico Trotta.
:align: center

*The price of Ethereum in EUR (€)*
```

Note that the response to the `GET` call is the following:

```{figure} images/api/coingecko_get.png
:alt: An image of the program by Federico Trotta.
:align: center

*The GET response.*
```

This is why the slicing used is:
- `current_value = data["prices"][1][1]`
- `yesterday_value = data["prices"][0][1]`

#### The `cvs_creation` module
[This module](https://github.com/federico-trotta/crypto_prices_API/blob/main/functions/csv_creation.py) has two functions:
- The function `new_csv()` creates a CSV writing the header, if it doesn't exist.
- The function `write_data()` writes the current value of a crypto in a currency on the current date.

### Using the main file
The main file is built as a menu with two options:
- Option 1 writes the current value of a crypto and stores its value in the CVS, if the user wants-
- Option 2 prints the difference in the value of a crypto between today and yesterday.

Let's show how the software is expected to work:

```{figure} images/api/coingecko_working.gif
:alt: An image of the program by Federico Trotta.
:align: center

*The expected result.*
```