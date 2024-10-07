import re
import json
from requests import Session
from bs4 import BeautifulSoup
from typing import Dict, Union, List, Optional


class GoogleLensResults:
    """
    GoogleLens Results Model.
    
    This class processes and extracts the useful data from the 
    Google Lens search response, including text, images, and links.
    
    Attributes:
        response (str): The HTML response from Google Lens.
    """

    def __init__(self, response: str):
        """
        Initialize GoogleLensResults object with the HTML response.
        
        :param response: Raw HTML response from Google Lens.
        """
        self.response = response

    def extract_raw_text(self) -> List[str]:
        """
        Extracts raw text from the Google Lens response.
        
        :return: A list of strings representing the extracted raw text.
        """
        soup = BeautifulSoup(self.response, 'html.parser')
        script_tag = soup.find('script', class_="ds:1")

        if script_tag:
            script_content = script_tag.string.strip()
            match = re.search(r'AF_initDataCallback\((\{.*?\})\);', script_content, re.DOTALL)

            if match:
                json_str = match.group(1)
                json_str = json_str[len("{key: 'ds:1', hash: '2', data:"):][:-len(", sideChannel: {}}")]
                json_data = json.loads(json_str)

                return json_data[3][4][0][0]

        raise ValueError("No valid JSON-like data found in the script.")

    def text_blocks(self, format_output: bool = True) -> List[List[List[Union[str, List[float], Optional[str], Optional[int]]]]]:
        """
        Extract structured visual match data from the Google Lens response.
        
        :param format_output: If True, the function returns structured visual results data; 
                            if False, it returns raw visual match data directly.
        :return: A list of structured visual results data or raw visual match data based on the value of format_output.
        """
        soup = BeautifulSoup(self.response, 'html.parser')
        script_tag = soup.find('script', class_="ds:1")

        if script_tag:
            script_content = script_tag.string.strip()
            match = re.search(r'AF_initDataCallback\((\{.*?\})\);', script_content, re.DOTALL)

            if match:
                json_str = match.group(1)
                json_str = json_str[len("{key: 'ds:1', hash: '2', data:"):][:-len(", sideChannel: {}}")]
                json_data = json.loads(json_str)

                if not format_output:
                    return json_data[2][3][0]

                structured_data = []  # List to hold structured visual match data
                for visual_match in json_data[2][3][0]:  # Iterate through each visual match
                    if visual_match[2] and visual_match[2][0][5]:  # Check if there is visual data
                        structured_visual_match = []  # List to hold structured data for the current visual match
                        for visual_data in visual_match[2][0][5][3][0]:  # Iterate through visual data items
                            structured_item = []  # List to hold structured items for the current visual data
                            for sub_item in visual_data[0]:  # Iterate through sub-items
                                structured_item.append(sub_item)  # Add sub-item to structured item list
                            structured_visual_match.append(structured_item)  # Add structured item to visual match
                        structured_data.append(structured_visual_match)  # Add structured visual match to final list
                return structured_data

        raise ValueError("No valid JSON-like data found in the script.")

    def extract_visual_results(self) -> Dict[str, Union[None, Dict[str, str], List[Dict[str, str]]]]:
        """
        Extracts visual match results from the Google Lens response.
        
        :return: A dictionary containing the main match and a list of similar matches.
        """
        soup = BeautifulSoup(self.response, 'html.parser')

        prerender_script = list(filter(
            lambda s: (
                'AF_initDataCallback(' in s.text and
                re.search(r"key: 'ds:(\d+)'", s.text).group(1) == "0"),
            soup.find_all('script')))[0].text
        prerender_script = prerender_script.replace(
            "AF_initDataCallback(", "").replace(");", "")
        hash = re.search(r"hash: '(\d+)'", prerender_script).group(1)
        prerender_script = prerender_script.replace(
            f"key: 'ds:0', hash: '{hash}', data:",
            f"\"key\": \"ds:0\", \"hash\": \"{hash}\", \"data\":").replace("sideChannel:", "\"sideChannel\":")

        prerender_script = json.loads(prerender_script)

        json_data = prerender_script['data'][1]

        results = {
            "match": None,
            "similar": []
        }

        try:
            results["match"] = {
                "title": json_data[0][1][8][12][0][0][0],
                "thumbnail": json_data[0][1][8][12][0][2][0][0],
                "pageURL": json_data[0][1][8][12][0][2][0][4]
            }
        except IndexError:
            pass
        
        if results["match"] is not None:
            visual_matches = json_data[1][1][8][8][0][12]
        else:
            try:
                visual_matches = json_data[0][1][8][8][0][12]
            except IndexError:
                return results

        for match in visual_matches:
            results["similar"].append(
                {
                    "title": match[3],
                    "thumbnail": match[0][0] if match[0] else None,
                    "pageURL": match[5],
                    "sourceWebsite": match[14]
                }
            )

        return results


class GoogleLens:
    """
    Google Lens class to perform image searches via Google Lens.
    """

    def __init__(self):
        self.url = "https://lens.google.com"
        self.session = Session()
        self.session.headers.update(
            {'User-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0'}
        )

    def __upload_image_file(self, file_path: Union[str, bytes]) -> GoogleLensResults:
        """
        Upload an image using a file path or binary data.
        
        :param file_path: The local path to the image file or binary data.
        :return: An instance of GoogleLensResults containing the response data.
        """
        if isinstance(file_path, bytes):
            multipart = {'encoded_image': ('image.png', file_path), 'image_content': ''}
        elif isinstance(file_path, str):
            multipart = {'encoded_image': (file_path, open(file_path, 'rb')), 'image_content': ''}
        else:
            raise ValueError("file_path must be either a file path (str) or binary data (bytes).")

        response = self.session.post(self.url + "/upload", files=multipart, allow_redirects=False)
        search_url = BeautifulSoup(response.text, 'html.parser').find('meta', {'http-equiv': 'refresh'}).get('content')
        search_url = re.sub("^.*URL='", '', search_url).replace("0; URL=", "")
        response = self.session.get(search_url).text
        return GoogleLensResults(response)

    def __upload_image_url(self, url: str) -> GoogleLensResults:
        """
        Upload an image using a URL.
        
        :param url: The URL of the image to search.
        :return: An instance of GoogleLensResults containing the response data.
        """
        response = self.session.get(self.url + "/uploadbyurl", params={"url": url}, allow_redirects=True).text
        return GoogleLensResults(response)

    def upload_image(self, image_input: Union[str, bytes]) -> GoogleLensResults:
        """
        Decide whether the input is a URL or file and upload the image accordingly.
        
        :param image_input: The image to upload, can be a URL (str) or a file path (str or bytes).
        :return: An instance of GoogleLensResults containing the response data.
        """
        if isinstance(image_input, str):
            if image_input.startswith('http://') or image_input.startswith('https://'):
                return self.__upload_image_url(image_input)
            else:
                return self.__upload_image_file(image_input)
        elif isinstance(image_input, bytes):
            return self.__upload_image_file(image_input)
        else:
            raise ValueError("image_input must be either a URL (str), a file path (str), or binary data (bytes).")
