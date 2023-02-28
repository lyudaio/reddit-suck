# Reddit Suck

Reddit Suck is a command-line tool that allows you to download all types of images and videos from a specified subreddit. 

## Installation

1. Clone the repository: `git clone https://github.com/lyudaio/reddit-suck.git`
2. Install the required dependencies: `pip install -r requirements.txt`
3. Navigate to the cloned directory: `cd reddit-suck`

## Usage

```bash
Usage: python main.py [OPTIONS] SUBREDDIT

Options:
  --num-posts INTEGER  Number of posts to download. Default is 10.
  --help               Show this message and exit.
```

## Examples

- Download 10 posts from r/memes: `python main.py memes`
- Download 20 posts from r/funny: `python main.py funny --num-posts 20`
- Download 1000 posts from r/gifs (maximum number of posts): `python main.py gifs --num-posts 1000`

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
