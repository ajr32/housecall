# Getting Started with HouseCall

Welcome to **HouseCall**, an open-source command-line tool that analyzes
Home Assistant installations and provides insights, recommendations, and
reports to help you understand, organize, and improve your smart home.

------------------------------------------------------------------------

# Requirements

Before using HouseCall, ensure you have:

-   Python 3.11 or later
-   A working Home Assistant installation
-   A Home Assistant Long-Lived Access Token

------------------------------------------------------------------------

# Installation

Clone the repository:

``` bash
git clone https://github.com/<your-github-username>/housecall.git
cd housecall
```

Create a virtual environment:

**Windows**

``` bash
python -m venv .venv
.venv\Scripts\activate
```

**Linux / macOS**

``` bash
python -m venv .venv
source .venv/bin/activate
```

Install HouseCall:

``` bash
pip install -e .
```

------------------------------------------------------------------------

# Configuration

Create a `.env` file in the project root.

``` text
HA_URL=http://homeassistant.local:8123
HA_TOKEN=your_long_lived_access_token
```

Replace the values with your Home Assistant URL and your Long-Lived
Access Token.

------------------------------------------------------------------------

# Running HouseCall

Start HouseCall with:

``` bash
python -m housecall
```

If everything is configured correctly, you should see output similar to:

``` text
==================================================
🏠 HouseCall
==================================================
Testing connection...
✓ Connected

Scanning Home Assistant...
```

------------------------------------------------------------------------

# Output

HouseCall currently generates:

-   `inventory.json` --- A complete inventory of your Home Assistant
    installation.

Additional reports and analysis modules will be added in future
releases.

------------------------------------------------------------------------

# Troubleshooting

## Authentication Failed

Verify that:

-   Your Home Assistant URL is correct.
-   Your Long-Lived Access Token is valid.
-   The token has not been revoked.

## Unable to Connect

Verify that:

-   Home Assistant is running.
-   The URL is reachable.
-   Firewalls or VPNs are not blocking access.

------------------------------------------------------------------------

# Next Steps

Future HouseCall releases will add:

-   Doctor
-   Housekeeping
-   Organization
-   Dashboard Advisor
-   Dashboard Designer
-   Dashboard Generator
-   Discover
-   Smart Advisor

Thank you for trying HouseCall!
