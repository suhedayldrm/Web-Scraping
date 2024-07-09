from dictionaries import person_dict, inst_dict, antra_dict, all_dicts
from dependencies import *

#Lets find a website to scrape
#we can call it www.cutie.com


class CutieScraper:
    
    person_dict = person_dict
    inst_dict = inst_dict
    antra_dict = antra_dict
    all_dicts = all_dicts
    
    def __init__(self):
        self.all_dicts = self.person_dict | self.inst_dict | self.antra_dict

    @staticmethod
    def html_info(url):
        """
        Get information from a given URL.

        Args:
            url (str): The URL.

        Returns:
            BeautifulSoup object or None: Parsed HTML data or None if an error occurs.
        """
        try:
            response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            response.raise_for_status()  # Raise an exception if there's an HTTP error
            raw_response = response.text
            soup = BeautifulSoup(raw_response, "html.parser")
            if soup.find(string=re.compile("nicht gefunden|warning")):
                return None
            else:
                return soup
        except requests.exceptions.RequestException as e:
            print(f"Error fetching URL: {e}")
            return None


    def html_person_search(self, person_name):
        """
        Search information using a person's name.
        Args:
            person_name (str): The person's name.
            Put person's name in the middle of the URL. 
            Because it is the search URL
            
        Returns:
            BeautifulSoup object or None: Parsed HTML data or None if an error occurs.
        """
        if not isinstance(person_name, str):
            print("Invalid input type")
            return None
        try:
            url = f"https://cutie={person_name.replace(' ', '+')}=person"
            soup = self.html_info(url)
            person_id = soup.find("div", class_="eintrag").find("h2").find("a", href=True)['href'].replace("/cutie/person/", "")
            return person_id
        except Exception as e:
            print(f"Error searching for person: {e}")
            return None


    def html_person_info(self, person_name):
        """
        Get information from CUTIE using a person id.
    
        Args:
            person_id (int): The person's id.
    
        Returns:
            BeautifulSoup object: Parsed HTML data of the person's URL from CUTIE.
            
        """
        try:
            person_id = self.html_person_search(person_name)
            person_url = "https://example/person/" + str(person_id)
            soup = self.html_info(person_url)
            return soup
        except:
            print("Could not find the person")
            return None

    def html_project_info(self,project_id):
        """
        Get information from CUTIE using a project ID.
    
        Args:
            project_id (int): A project ID.
    
        Returns:
            BeautifulSoup object: Parsed HTML data from CUTIE.
        """
        if not isinstance(project_id, int):
            print("Invalid input type. It should be numeric.")
            return None
    
        try:
            project_url = f"https://cutie/projekt/{project_id}"
            soup = self.html_info(project_url)
            return soup
        except:
            print("Invalid ID")
            return None

    @staticmethod
    def person_base(soup):
        
        """
        Extracts information about a person from a BeautifulSoup object.

        Args:
        soup (BeautifulSoup): A BeautifulSoup object representing the HTML content of a web page.

        Returns:
        tuple: A tuple containing a dictionary with person information and a list of project IDs.
               The dictionary has the following keys:
               - "Person Id": The unique identifier for the person.
               - "Person Current Inst.": The current institutional affiliation of the person.
               The list contains project IDs associated with the person.

        If an error occurs during extraction, returns None.
        """
        if not soup:
            return None
        try:
            person_data = {}
            person_data["Person Id"] = soup.find("a", href=re.compile("person"))["href"].split("?")[0].replace("/cutie/person/", "")
            project_ids = [x["href"].replace("/cutie/projekt/", "") for x in soup.find_all(href=re.compile("projekt"))]
            person_data["Person Current Inst."] = soup.find('div', class_='details').get_text(separator=",", strip=True).replace("Adresse, ", "")
            return person_data, project_ids
        except Exception as e:
            print(f"Error extracting person information: {e}")
            return None, None
        

    def person_info(self, person_name):
        """
        Get information using a person's name.

        Args:
            person_name (str): The person's name.

        Returns:
            person_data (dictionary) and project ids(list) or None: The person's information(tuple) or None if an error occurs.
            person's name is added into the person_data.
        """
        try:
            soup = self.html_person_info(person_name)
            person_data, project_ids = self.person_base(soup)
            person_data["Person name"] = person_name
            return person_data, project_ids
        except Exception as e:
            print(f"Error getting person information: {e}")
            return None
        
    @staticmethod
    def get_roles(soup):
        """
        Extracts roles associated with a person or institution from a BeautifulSoup object.
        Args:
        soup (bs4.BeautifulSoup): The BeautifulSoup object representing the HTML content.
        Returns:
        list: A list of dictionaries, each containing a x and associated information.
              Example: [{"Name": "Adam Smith", "Role": "Applicant", "id":32342234 }, ...]
              Returns an empty list if no roles are found or an error occurs.
        Raises:
        Exception: If an error occurs during extraction.
        """
        roles = []
        try:
            all_roles = soup.find_all(href=re.compile("institution|person"))
            for x in all_roles:
                role = x.find_previous("span", "name").string.strip()
                person_or_inst_id =  x["href"].replace("/cutie/person/", "").replace("/cutie/institution/", "")
                roles.append({"name": x.get_text(separator=", ", strip=True), "id": person_or_inst_id, "role": role})
    
            return roles
        except Exception as e:
            print(f"Error extracting roles: {e}")
            return []

    @staticmethod
    def find_dict(roles):
        
        """
        Assigns roles to different categories which are institutions(inst_dict), researchers(person_dict), applicants(antra_dict) and formats them.
        
        Args:
        roles (list): A list of dictionaries representing roles, with role keys and associated information.
        
        Returns:
        dict: A dictionary containing categorized and formatted roles.
        
        Example:
        Usage: {"Researchers": ["name": "Adam Smith", "role": "Role1(eng)", "id": "123"], ...}
        """
        
        roles_data = {"Researchers": [], "Institutions": [], "Antragstellende/Mitverantwortliche": []}
        for role in roles:
            if role["role"] in person_dict:
                role["role"] = person_dict[role["role"]]
                roles_data["Researchers"].append(role)
            elif role["role"] in inst_dict:
                role["role"] = inst_dict[role["role"]]
                roles_data["Institutions"].append(role)
            elif role["role"] in antra_dict:
                role["role"] = antra_dict[role["role"]]
                roles_data["Antragstellende/Mitverantwortliche"].append(role)
            else:
                roles_data["Researchers"].append(role)
        
        return roles_data


    def project_info(self, project_id):
        
        """
        Extracts all information about a project from a given project ID using many functions.
        Args:
        project_id (str): The unique identifier for the project.
        
        Returns:
        dict or None: A dictionary containing whole project information, including roles. Returns None if an error occurs during extraction.
        """
        project_data = {}
        soup = self.html_project_info(project_id)
        roles = self.get_roles(soup)
        roles_data = self.find_dict(roles)

        try:
            project_data["Project Title"] = soup.find("title").text.strip().replace('DFG - CUTIE - ', '')
            project_data["Project ID"] = project_id
            project_data["DFG-Verfahren"] = soup.find("span", "name", string=" DFG-Verfahren").find_next_sibling("span").string

            #combine roles_data and project_data
            project_data = (project_data | roles_data)

            return project_data
        except Exception as e:
            print(f"Error extracting project information: {e}")
            return None


    def combined_info(self,person_name):
        
        """
        Combines information about a person and their associated projects.
        
        Args:
        person_name (str): The name of the person.
        
        Returns:
        list or None: A list of dictionaries containing combined information about a person and her/his projects info 
        Returns None if an error occurs during extraction.
        
        Example:
        Usage: combined_info = combined_info("Adam Smith")
        """
        
        data = []
        try:
            person_data, project_ids = self.person_info(person_name)
            for project_id in project_ids:
                project_id = int(project_id)
                project_data = self.project_info(project_id)
                combined = (project_data|person_data)
                data.append(combined)
            return data
        except:
            return None
