import urllib.request
import json
import ipaddress
import sys

def download_aws_ip_set():
  """Downloads the AWS IP range JSON file and returns it as a dictionary."""

  # URL of the AWS IP range JSON file
  aws_ip_range_url = 'https://ip-ranges.amazonaws.com/ip-ranges.json'

  # Download the JSON file
  with urllib.request.urlopen(aws_ip_range_url) as url:
    aws_ip_range_data = json.load(url)

  return aws_ip_range_data['prefixes']

# Find ip given IP belongs to any AWS Service
def find_aws_ip(aws_ip_range_data, ip_to_find):
  """Finds the AWS IP ranges that contain the given IP address and includes the first/last IP in the chosen range."""
  matches = []
  ip_to_check = ipaddress.ip_address(ip_to_find)

  for prefix in aws_ip_range_data:
    network = ipaddress.ip_network(prefix['ip_prefix'])
    if ip_to_check in network:
      range_data = dict(prefix)
      range_data['first_ip'] = str(network.network_address)
      range_data['last_ip'] = str(network.broadcast_address)
      matches.append(range_data)

  return matches

sys.stdout.write(json.dumps(find_aws_ip(download_aws_ip_set(), sys.argv[1]),indent=2))