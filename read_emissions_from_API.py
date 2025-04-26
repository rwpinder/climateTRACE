import http.client
import json

def fetch_emissions(api_host, api_path, api_key):
    """
    Fetch emissions data from the Climate TRACE API using http.client.

    Args:
        api_host (str): The API host (e.g., "api.climatetrace.org").
        api_path (str): The API path (e.g., "/emissions").
        api_key (str): The API key for authentication.

    Returns:
        dict: Parsed JSON data containing emissions information.
    """
    connection = http.client.HTTPSConnection(api_host)
    headers = {
       # 'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
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

def parse_emissions_data(emissions_data, gas='co2'):
    """
    Parse emissions data to extract relevant information.

    Args:
        emissions_data (dict): JSON data containing emissions information.

    Returns:
        list: A list of emissions records with relevant details.
    """
    if not emissions_data:
        print("No emissions data to parse.")
        return []

    parsed_data = []
    record = emissions_data
    parsed_record = {
        'country': record.get('country'),
        'continent': record.get('continent'),
        'rank': record.get('rank'),
        'previous_rank': record.get('previousRank'),
        'emissions': [
            {
                'gas': gas,
                'value': value
            } for gas, value in record.get('emissions', []).items()
        ]
    }
    parsed_data.append(parsed_record)
    
    return parsed_data

if __name__ == "__main__":
    # Example usage
    API_HOST = "api.climatetrace.org"  # Replace with the actual API host
    API_PATH = "/v6/country/emissions"  # Replace with the actual API path
    API_KEY = "your_api_key_here"  # Replace with your API key

    emissions_data = fetch_emissions(API_HOST, API_PATH, API_KEY)
    if emissions_data:
        parsed_emissions = parse_emissions_data(emissions_data)
        print(json.dumps(parsed_emissions, indent=4))