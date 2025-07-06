Project Goal:

A real estate investment firm needed to gather comprehensive data on residential properties for sale in a specific, high-value area (e.g., Negombo). The goal was to analyze market trends, average pricing, and property specifications.

My Solution:

I developed a Python and Selenium application that fully automates the data collection process. The script first interacts with the complex search form on LankaPropertyWeb.com, selecting the correct property type, location, and other filters. It then programmatically paginates through all search results to gather a complete list of property links. Finally, it visits each link to extract detailed information, including data from within a map <iframe>.

Technical Challenges & Skills Demonstrated:

Complex Form Automation: Successfully automated multi-step forms with dropdown menus, text inputs, and dynamic suggestion boxes.

iFrame Handling: Wrote code to find and extract the Google Maps link and coordinates from within a nested <iframe>, a common challenge on modern websites.

Robust Pagination: Built a reliable pagination loop that correctly identifies the "Next" button and knows when to stop on the last page.

Advanced Data Extraction: Used specific XPath selectors to reliably find data points (like bedrooms and bathrooms) that did not have unique class names.

Data Cleaning & Structuring: Organized the scraped data into a clean, ready-to-use CSV file.

Final Result:

Delivered a clean spreadsheet containing all requested property details, including geo-location links, allowing the client to immediately begin their market analysis.

