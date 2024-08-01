import os
URL = 'https://api.github.com/repos/department-of-veterans-affairs/va.gov-team/issues'

# get the headers for a request to GH api
def get_headers():
  return {
      'Authorization': f'Bearer {os.getenv("TOKEN")}',
      'Content-Type': 'application/json',
      'Accept': 'application/vnd.github.v3+json'
    }