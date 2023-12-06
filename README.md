# Jellyfin Tools

Enhance your Jellyfin experience with these essential tools designed to streamline and manage mundane tasks.

## Tools Overview

- **Jellyfin Duplicate Finder** (`duplicate_finder.py`)
- **Simple Metadata Check** (`simple_metadata_check.py`)

## Detailed Tool Descriptions
**Jellyfin Duplicate Finder** (`duplicate_finder.py`) helps you find duplicate media files in your Jellyfin. It scans your media library and identifies any duplicate files, allowing you to remove them and free up storage space.

**Simple Metadata Check** (`simple_metadata_check.py`) helps you check the metadata of your media files in Jellyfin. It verifies if the metadata (such as title, description, and artwork) is present and correct. This tool ensures that your media library is properly organized and displays accurate information.

## Prerequisites for Using the Tools

To effectively use these tools, you will need:

- **Python 3.x**: Ensure you have Python 3.x installed on your system.
- **Requests Library**: This can be installed via pip using the command `pip install requests`.
- **Jellyfin Server Access**: You should have an API key for your Jellyfin server.
- **Server URL and User ID**: These are necessary for accessing media categories on your Jellyfin server.

**Obtaining Your Jellyfin URL**
- If you're unsure about this, you might want to revisit why you're here!

**Generating Your API Key**
- Navigate to the Jellyfin admin panel. Go to **Panel -> API Keys** and click on **+** to create a new key.

**Finding Your User ID**
- In the Jellyfin admin panel, click on **Users**, select your username, and find your **userID** in the URL, formatted like: **userId=484b9fcf045dXXXXXXXXXXXXXXXXXXX**.

## How to Use

First, download and extract the repository to your computer.

In the extracted folder, execute the scripts as you would with any standard Python script:
- For **Jellyfin Duplicate Finder**, run: `python3 duplicate_finder.py`
- For **Simple Metadata Check**, run: `python3 simple_metadata_check.py`
