##SubScan## - Advanced Subdomain Enumeration BY MIDO

**SubScan** is a powerful tool for subdomain enumeration and vulnerability scanning. It utilizes popular subdomain enumeration tools like **Subfinder** and **Sublist3r** (I manually fix bugs), and optionally integrates a vulnerability scanning step (currently mocked). This tool is designed to be used by penetration testers, bug bounty hunters, and security researchers.

## Features
- **Subdomain Enumeration**: Uses tools like Subfinder and Sublist3r to discover subdomains.
- **Parallel Execution**: Runs subdomain enumeration tools in parallel for faster results.
- **Vulnerability Scanning**: Optionally scan the discovered subdomains for common vulnerabilities (currently mocked).
- **Output**: Combines results from both tools into a single output file.
- **Logging**: All actions are logged for detailed review.
- **Verbose Mode**: Enables detailed output for deeper insights during execution.

## Prerequisites
Before using **SubScan**, you need to have the following dependencies installed:
- **Python 3.x**
- **Subfinder**: [Subfinder GitHub](https://github.com/projectdiscovery/subfinder)
- **Sublist3r**: [Sublist3r GitHub](https://github.com/aboul3la/Sublist3r)
- **pyfiglet**: To generate the ASCII banner.
- **termcolor**: For colored terminal output.

### Install Dependencies
Install Python packages with pip:
```bash
pip install termcolor pyfiglet

Install Subfinder and Sublist3r

To install Subfinder and Sublist3r, you can follow the instructions on their respective GitHub pages:

    Subfinder:

go get -u github.com/projectdiscovery/subfinder/v2/cmd/subfinder

Sublist3r: Clone the repository and install the requirements:

    git clone https://github.com/aboul3la/Sublist3r.git
    cd Sublist3r
    pip install -r requirements.txt
    chmod + *

Usage
Basic Command

Run the tool with a specified domain:

python3 subscan.py -d example.com

Available Arguments

    -d, --domain (required): Target domain for subdomain enumeration and vulnerability scanning.
    --no-subfinder: Skip Subfinder subdomain enumeration.
    --no-sublist3r: Skip Sublist3r subdomain enumeration.
    --vuln: Run a vulnerability scan (currently mocked, you can replace it with an actual scanner like nmap).
    -o, --output: Specify the output file name (default: output.txt).
    -p, --ports: Specify the ports for vulnerability scanning (default: 80,443).
    --verbose: Enable verbose mode for detailed output during execution.

Example

python subscan.py -d example.com -o subdomains.txt --vuln --verbose

This will:

    Enumerate subdomains using Subfinder and Sublist3r.
    Run a vulnerability scan on discovered subdomains.
    Output the results to subdomains.txt.
    Enable verbose output for detailed logging.

Output

The tool generates three types of outputs:

    Subdomain Results: From both Subfinder and Sublist3r (saved in subfinder_output.txt and sublist3r_output.txt).
    Combined Output: The results from both tools combined into one file (e.g., combined_output.txt).
    Log File: Detailed logs are saved in scan.log.b(if u see and error on log from subfinder dont worry just run again the command)

Example Output

[*] Running Subfinder...
[*] Running Sublist3r...
[*] Combining output from Subfinder and Sublist3r...
[*] Vulnerability scan completed. No vulnerabilities found (mock scan).
[*] Scan completed. Check the output files and logs for details.

License

This project is licensed under the MIT License - see the LICENSE file for details.
Contributing

If you would like to contribute to SubScanX, feel free to open an issue or submit a pull request. Your contributions are always welcome!
TODO

    Integrate an actual vulnerability scanning tool (e.g., nmap).
    Add more scanning features like brute-forcing subdomains or DNS enumeration.

Author

Created by [MIDO].
Feel free to reach out via [GitHub Profile or Email].


### Key Sections:
- **Overview**: A brief description of what the project does.
- **Features**: What the tool can do.
- **Prerequisites**: List of required software and installation instructions.
- **Usage**: Instructions on how to use the script, including arguments and an example command.
- **License**: Information about licensing.
- **Contributing**: How others can contribute to the project.
- **TODO**: Future improvements.

This `README.md` should provide clear documentation for users of your project, helping them set up and use **SubScanX** efficiently.

