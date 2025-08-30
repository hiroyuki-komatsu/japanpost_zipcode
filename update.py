import email.utils
import hashlib
import urllib.request
from datetime import datetime


def get_modified_date(headers):
    last_modified_str = headers.get('Last-Modified')

    if last_modified_str:
        # Converts HTTP date format to datetime object
        timestamp = email.utils.parsedate_to_datetime(last_modified_str)
        return timestamp.strftime('%Y-%m-%d')

    return datetime.now().strftime('%Y-%m-%d')


def download_file(url, file_path):
    """
    Downloads the of url and retrieves information about the file.

    Args:
        url (str): The URL of the file to get information about.
        file_path (str): The path to write the downloaded file.

    Returns:
        dict: A dictionary containing the file's information.
              Returns None if the retrieval fails.
    """
    try:
        req = urllib.request.Request(url)
        sha256_hash = hashlib.sha256()
        
        with urllib.request.urlopen(req) as response:
            # Get the file size
            size = int(response.headers.get('content-length', 0))

            with open(file_path, 'wb') as f:
                # Read in chunks and update the hash
                while True:
                    chunk = response.read(8192)
                    if not chunk:
                        break
                    f.write(chunk)
                    sha256_hash.update(chunk)
            sha256 = sha256_hash.hexdigest()
            date = get_modified_date(response.headers)

            return {
                'URL': url,
                'Date': date,
                'Size': size,
                'SHA256': sha256
            }
    except urllib.error.URLError as e:
        print(f'An error occurred while retrieving the file: {e.reason}')
        return None


def get_info_str(file_name, file_info):
    output = [file_name]
    for key, value in file_info.items():
        output.append(f'*   {key}: {value}')
    return '\n'.join(output)


def update_zipcode():
    jigyosyo_name = 'jigyosyo.zip'
    jigyosyo_url = 'https://www.post.japanpost.jp/zipcode/dl/jigyosyo/zip/jigyosyo.zip'
    jigyosyo_info = download_file(jigyosyo_url, jigyosyo_name)
    jigyosyo_log = get_info_str(jigyosyo_name, jigyosyo_info)

    kenall_name = 'ken_all.zip'
    kenall_url = 'https://www.post.japanpost.jp/zipcode/dl/kogaki/zip/ken_all.zip'
    kenall_info = download_file(kenall_url, kenall_name)
    kenall_log = get_info_str(kenall_name, kenall_info)

    date = datetime.now().strftime('%Y-%m-%d')

    output = f'''\
Update data as of {date}    

{jigyosyo_log}

{kenall_log}
'''
    print(output)


if __name__ == '__main__':
    update_zipcode()