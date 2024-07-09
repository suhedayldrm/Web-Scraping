from dependencies import *
from dictionaries import person_dict, inst_dict, antra_dict
from cutie import CutieScraper
import json

if __name__ == "__main__":
    scraper = CutieScraper()
    
    people_names = ["Eda Akman", "Ken Barbie"]
    results = []
    
    for person_name in people_names:
        try:

            results.extend(scraper.combined_info(person_name))
        except Exception as e:
            print(f"Error processing {person_name}: {e}")

    results_df = pd.DataFrame(results)
    print(results_df)

    # Save the combined data to a JSON file
    json_filename = "combined_data.json"
    with open(json_filename, 'w') as json_file:
        json.dump(results, json_file, indent=2)

    print(f"Data saved to {json_filename}")