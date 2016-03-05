# Vets.gov Status Dashboard

A dashboard for Vets.gov projects, and the status of development.

## Getting started

1. Install Jekyll:
  ```
  npm install
  # This will automatically run `bundle install` for Jekyll, too
  ```
2. Clone this repository

3. Run the scraper to get the most up to date files
  - You will need to have Python and pip installed
  - Install github3.py `pip install github3.py`
  - Set GITHUB\_USERNAME and GITHUB\_PASSWORD locally
 
  ```
  $ export GITHUB_USERNAME=your_github_username
  $ export GITHUB_PASSWORD=your_github_password_or_token  
  ```
  - Run the scraper `python scripts/scraper.py`
3. Serve the project locally
  ```
  bundle exec jekyll serve
  ```
4. Build the project locally
  ```
  bundle exec jekyll build
  ```

## License

[The MIT License (MIT)](LICENSE.md)

Copyright © 2015 [Chloi Inc.](http://chloi.io)
