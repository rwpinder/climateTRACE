import http.client

import json

def fetch_emissions(api_host, api_path, api_key, query_params=None):
    """
    Fetch emissions data from the Climate TRACE API using http.client.

    Args:
        api_host (str): The API host (e.g., "api.climatetrace.org").
        api_path (str): The API path (e.g., "/emissions").
        api_key (str): The API key for authentication.
        query_params (dict): Optional dictionary of query parameters.


    Returns:
        dict: Parsed JSON data containing emissions information.
    """
    connection = http.client.HTTPSConnection(api_host)

    if query_params:
        from urllib.parse import urlencode
        api_path += "?" + urlencode(query_params)

    headers = {
       # 'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
        'countries': 'USA'
    }

    try:
        connection.request("GET", api_path, headers=headers)
        response = connection.getresponse()
        if response.status != 200:
            print(f"Error: Received HTTP {response.status} - {response.reason}")
            return None

        data = response.read().decode('utf-8')
        return json.loads(data)
    except Exception as e:
        print(f"Error fetching data from API: {e}")
        return None
    finally:
        connection.close()

def get_emissions_by_gas(emissions_data):
    """
    Parse emissions data to extract a dictionary of emissions with keys that are the name of the gas.

    Args:
        emissions_data (dict): JSON data containing emissions information.

    Returns:
        dict: A dictionary containing a key for each gas and emissions as the value.
    """
    if not emissions_data:
        print("No emissions data to parse.")
        return {}

    try:
       
        # Check if emissions_data is a dictionary or a list
        if isinstance(emissions_data, list):
            # If it's a list, iterate through each record
            for record in emissions_data:
                emissions_by_gas = record.get('emissions', {})

        
        return emissions_by_gas
    except KeyError as e:
        print(f"Key error while parsing data: {e}")
        return {}

if __name__ == "__main__":
    # Example usage
    API_HOST = "api.climatetrace.org"  # Replace with the actual API host
    API_PATH = "/v6/country/emissions"  # Replace with the actual API path
    API_KEY = "your_api_key_here"  # Replace with your API key
    q_params = { 'countries': 'USA'}  # Example query parameters
    emissions_data = fetch_emissions(API_HOST, API_PATH, API_KEY, q_params)
    if emissions_data:
        emissions = get_emissions_by_gas(emissions_data)
        print(json.dumps(emissions, indent=4))
