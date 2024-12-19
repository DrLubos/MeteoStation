import json
import requests

class DataLoader:
    """
    Utility class for loading data from JSON files or REST APIs.
    """

    @staticmethod
    def load_from_file(file_path: str) -> dict[str, any]:
        """
        Load data from a JSON file.

        Args:
            file_path (str): Path to the JSON file.

        Returns:
            dict[str, any]: Data loaded from the file.
        """
        with open(file_path, 'r') as file:
            return json.load(file)

    @staticmethod
    def load_from_api(endpoint: str) -> dict[str, any]:
        """
        Load data from a REST API.

        Args:
            endpoint (str): URL of the API endpoint.

        Returns:
            dict[str, any]: Data returned by the API.

        Raises:
            Exception: If the API request fails.
        """
        response = requests.get(endpoint)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"API Error: {response.status_code}")