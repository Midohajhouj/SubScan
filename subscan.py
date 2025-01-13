import os
import time
import argparse
import logging
from termcolor import colored
from pyfiglet import figlet_format
from multiprocessing import Process, Queue
import re
import requests
import sys

# Initialize logging with timestamp and custom format
logging.basicConfig(
    filename="scan.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Stylish Banner to display the project name and description
def banner():
    print(colored(figlet_format("SubScan", font="slant"), "cyan"))
    print(colored("Advanced Subdomain Enumeration BY MIDO", "magenta"))
    print(colored("=" * 65, "yellow"))

# Section banner to visually separate different sections in the output
def section_banner(title):
    print("\n" + colored("=" * 65, "cyan"))
    print(colored(f"[ {title} ]", "magenta"))
    print(colored("=" * 65, "cyan"))

# Run a system command with error handling and logging
def run_command(command, task_name, output_queue=None):
    try:
        start_time = time.time()
        logging.info(f"Starting {task_name}: {command}")
        result = os.system(command)
        if result != 0:
            raise Exception(f"{task_name} encountered an error. Exit code: {result}")
        elapsed_time = time.time() - start_time
        logging.info(f"Completed {task_name} in {elapsed_time:.2f} seconds.")
        print(colored(f"[*] {task_name} completed in {elapsed_time:.2f} seconds.", "green"))

        # Send the status to the queue for process synchronization
        if output_queue:
            output_queue.put(f"{task_name} completed successfully.")
    except Exception as e:
        logging.error(f"Error during {task_name}: {e}")
        print(colored(f"[!] Error during {task_name}: {e}", "red"))
        if output_queue:
            output_queue.put(f"{task_name} failed with error: {e}")

# Subdomain scan logic using ThreatCrowd API
def get_domain(url):
    """Extract domain from a URL"""
    regex = r'^(?:https?://)?(?:[^@/\n]+@)?(?:)?([^:/?\n]+).*'
    match = re.match(regex, url)
    if match:
        return match.group(1)
    return None

def subdomain_scan(url):
    """Scan for subdomains using the ThreatCrowd API"""
    domain = get_domain(url)
    if not domain:
        return None
    
    api_url = f"http://ci-www.threatcrowd.org/searchApi/v2/domain/report/?domain={domain}"
    print(f"Searching for subdomains of {domain}\nLoading...")
    
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def run_subfinder(domain, output_file, output_queue):
    section_banner("Running Subfinder")
    command = f"subfinder -d {domain} -o {output_file}"
    run_command(command, "Subfinder", output_queue)

def run_sublist3r(domain, output_file, output_queue):
    section_banner("Running Sublist3r")
    command = f"python3 sublist3r.py -d {domain} -o {output_file}"
    run_command(command, "Sublist3r", output_queue)

# Combine outputs from multiple tools into a single file
def combine_outputs(subfinder_output, sublist3r_output, combined_output):
    try:
        with open(combined_output, "w") as outfile:
            for file in [subfinder_output, sublist3r_output]:
                if os.path.exists(file):
                    with open(file, "r") as infile:
                        outfile.write(infile.read())
                        outfile.write("\n")
        print(colored(f"[*] Combined output saved to {combined_output}", "green"))
    except Exception as e:
        logging.error(f"Error combining outputs: {e}")
        print(colored(f"[!] Error combining outputs: {e}", "red"))

# Parse command-line arguments for user customization
def parse_arguments():
    parser = argparse.ArgumentParser(description="Advanced Subdomain Enumeration and Vulnerability Scanner")
    parser.add_argument("-d", "--domain", required=True, help="Target domain for scanning")
    parser.add_argument("--no-subfinder", action="store_true", help="Skip Subfinder enumeration")
    parser.add_argument("--no-sublist3r", action="store_true", help="Skip Sublist3r enumeration")
    parser.add_argument("--vuln", action="store_true", help="Run a vulnerability scan (mock)")
    parser.add_argument("-o", "--output", default="output.txt", help="Specify output file name (default: output.txt)")
    parser.add_argument("-p", "--ports", default="80,443", help="Specify ports for vulnerability scanning (default: 80,443)")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose mode for detailed output")
    return parser.parse_args()

# Main function to orchestrate the scanning processes
def main():
    banner()
    args = parse_arguments()
    domain = args.domain
    output_file = args.output
    ports = args.ports

    # Ensure output directory exists
    output_dir = "output"
    if not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir)
            logging.info(f"Created output directory: {output_dir}")
        except Exception as e:
            logging.error(f"Failed to create output directory: {e}")
            print(colored(f"[!] Failed to create output directory: {e}", "red"))
            return  # Exit if directory creation fails

    subfinder_output = os.path.join(output_dir, f"subfinder_{output_file}")
    sublist3r_output = os.path.join(output_dir, f"sublist3r_{output_file}")
    combined_output = os.path.join(output_dir, f"combined_{output_file}")

    # Verbose mode
    if args.verbose:
        print(colored("[*] Verbose mode enabled.", "yellow"))
        logging.info(f"Verbose mode enabled. Domain: {domain}, Output file: {output_file}, Ports: {ports}")

    processes = []
    output_queue = Queue()

    # Run Subfinder unless skipped
    if not args.no_subfinder:
        p = Process(target=run_subfinder, args=(domain, subfinder_output, output_queue))
        processes.append(p)
        p.start()
    else:
        print(colored("[*] Skipping Subfinder.", "yellow"))

    # Run Sublist3r unless skipped
    if not args.no_sublist3r:
        p = Process(target=run_sublist3r, args=(domain, sublist3r_output, output_queue))
        processes.append(p)
        p.start()
    else:
        print(colored("[*] Skipping Sublist3r.", "yellow"))

    # Run Subdomain scan using ThreatCrowd API
    subdomain_data = subdomain_scan(domain)
    if subdomain_data and 'subdomains' in subdomain_data:
        subdomains = subdomain_data['subdomains']
        if subdomains:
            print(colored(f"Subdomains of {domain} found from ThreatCrowd API!", "green"))
            for subdomain in subdomains:
                print(f"     [+] http://{subdomain}")
        else:
            print(colored(f"Failed to find subdomains of {domain} from ThreatCrowd API.", "red"))
    else:
        print(colored(f"Failed to retrieve subdomains from ThreatCrowd API for {domain}.", "red"))

    # Wait for enumeration processes to complete
    for p in processes:
        p.join()

    # Combine outputs if both tools are used
    if not args.no_subfinder and not args.no_sublist3r:
        combine_outputs(subfinder_output, sublist3r_output, combined_output)

    # Run vulnerability scan if enabled
    if args.vuln:
        # Mock vulnerability scan
        print(colored(f"[*] Running mock vulnerability scan for {domain}.", "yellow"))
        time.sleep(2)
        print(colored("[*] Vulnerability scan completed. No vulnerabilities found (mock scan).", "green"))
    else:
        print(colored("[*] Skipping vulnerability scan.", "yellow"))

    print(colored("\n[*] Scan completed. Check the output files and logs for details.", "green"))

# Entry point of the script
if __name__ == "__main__":
    main()
