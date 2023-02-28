import os
import random
import requests
import string
import click
from tqdm import tqdm
from hurry.filesize import size
import time


def generate_random_string(length):
    """Generate a random string of fixed length"""
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


def download_file(url, directory):
    """Download a file from the specified URL and save it to the specified directory"""
    try:
        with requests.get(url, stream=True, timeout=30) as response:
            response.raise_for_status()
            filename = os.path.join(directory, generate_random_string(10) + os.path.splitext(url)[1])
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            return os.path.getsize(filename)
    except requests.exceptions.RequestException as e:
        click.secho(f"Failed to download file: {url} ({str(e)})", fg='red')
        return 0


def download_images_and_videos(subreddit, num_posts):
    """Download all types of images and videos from a specified subreddit"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    # create a directory to store the downloaded files
    directory = os.path.join(os.getcwd(), subreddit)
    os.makedirs(directory, exist_ok=True)

    # scrape the subreddit for image and video submissions
    url = f'https://www.reddit.com/r/{subreddit}/hot.json?limit={num_posts}'
    response = requests.get(url, headers=headers)
    data = response.json()['data']['children']

    pbar = tqdm(total=num_posts, desc=f'Downloading from /r/{subreddit}', dynamic_ncols=True, colour='yellow', unit='KB')
    total_size = 0
    count = 0
    num_images_videos = 0
    start_time = time.time()

    for post in data:
        # get the URL and file type of the post
        url = post['data']['url']
        file_type = url.split('.')[-1]

        # download the file if it's an image or video
        if file_type in ['jpg', 'jpeg', 'png', 'gif', 'gifv', 'mp4', 'mov', 'webm']:
            file_size = download_file(url, directory)
            total_size += file_size
            if file_size > 0:
                num_images_videos += 1
            count += 1
            pbar.update(1)

            if count >= num_posts or num_images_videos >= num_posts:
                break

    if num_images_videos < num_posts:
        pbar.color = 'red'
        pbar.close()
        click.secho(f"\nSome media failed to download\n", bold=True, fg='yellow')
    else:
        pbar.color = 'green'
        pbar.close()

    # print total size and time taken to download the files
    size_str = size(total_size)
    time_taken = time.time() - start_time
    click.secho(f"\nTotal size downloaded: {size_str}", bold=True, fg='green')
    click.secho(f"Time taken: {time_taken:.2f} seconds\n", bold=True, fg='green')

@click.command()
@click.argument('subreddit')
@click.option('--num-posts', default=10, help='Number of posts to download')
def main(subreddit, num_posts):
    if num_posts > 1000:
        num_posts = 1000
        click.secho("Maximum number of posts is 1000. Downloading 1000 posts...", fg='yellow')

    download_images_and_videos(subreddit, num_posts)

if __name__ == '__main__':
    main()
