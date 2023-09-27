import json
from rich import print
import random
from datetime import datetime, timedelta

day = 3600 * 24

def random_datetime_string():
    # Define the start and end dates
    start_date = datetime(2015, 1, 1)
    end_date = datetime.now()

    # Calculate the time difference in seconds
    time_difference = (end_date - start_date).total_seconds()

    # Generate a random timestamp within the range
    random_create_stamp = random.uniform(0, time_difference)


    random_mod_stamp = random.randint(day*2,day*500) + random_create_stamp

    # Create a new datetime by adding the random timestamp to the start date
    random_create_date = start_date + timedelta(seconds=random_create_stamp)

    random_mod_date = start_date + timedelta(seconds=random_mod_stamp)

    # Format the datetime as a string
    random_create_string = random_create_date.strftime('%Y-%m-%d %H:%M:%S')

    random_mod_string = random_mod_date.strftime('%Y-%m-%d %H:%M:%S')

    return random_create_string,random_mod_string

def random_weighted_permission_string(is_folder=False):
    # Define the characters for each permission
    permission_chars = ['r', 'w', 'x', '-']

    # Define typical permissions for folders and files
    folder_perms_owner = 'rwx'
    folder_perms_group = 'r-x'
    folder_perms_others = 'r-x'
    file_perms_owner = 'rw-'
    file_perms_group = 'r--'
    file_perms_others = 'r--'

    # Determine if it's a folder (weighted probability)
    #is_folder = random.choice([True, False])

    if is_folder:
        # Use typical folder permissions
        owner_perms = folder_perms_owner
        group_perms = folder_perms_group
        others_perms = folder_perms_others
    else:
        # Use typical file permissions
        owner_perms = file_perms_owner
        group_perms = file_perms_group
        others_perms = file_perms_others

    # Combine the permission strings
    permission_string = owner_perms + group_perms + others_perms

    return permission_string


# users = ['jiya','navya','chuck','owen','eva','jack','mia','bob','yash','ahmed','juan']
users = [
    "Ana",
    "Ava",
    "Aya",
    "Bob",
    "Eli",
    "Emi",
    "Jivya",
    "Juan"
    "Kai",
    "Kim",
    "Leo",
    "Luca",
    "Max",
    "Mei",
    "Mia"
    "Navya",
    "Nia",
    "Raj",
    "Ray",
    "Sam",
    "Yara",
    "Zara",
]
entries = []

def assign_ids(json_data, parent_id=0, current_id=1,owner_name=None):
    """
    Recursively assign unique IDs to directories and set parent IDs for files.
    
    Args:
        json_data (list of dict): The JSON data representing the directory structure.
        parent_id (int): The parent ID of the current directory.
        current_id (int): The current ID to be assigned.

    Returns:
        int: The next available ID.
    """
    for item in json_data:
        # Assign the current ID to the current directory
        if 'owner' in item:
            owner_name = item['owner']
        if owner_name:
            item['owner'] = owner_name
            item['group'] = owner_name
        else:
            owner_name = 'root'

        item['id'] = str(current_id)
        entries.append(item)
        current_id += 1

        # Set parent ID for this directory
        item['parent_id'] = str(parent_id)

        if parent_id == 0:
            pass

        # Check if it's a directory
        if item['type'] == 'directory':
            # Recursively assign IDs to subdirectories
            if 'contents' in item:
                current_id = assign_ids(item['contents'], item['id'], current_id,owner_name)

    return current_id





if __name__=='__main__':

    with open('treeout.json') as f:
        data = json.load(f)

    assign_ids(data)
    print(data)

    with open("treewids.json","w") as f:
        json.dump(data,f,indent=4)

    with open("treewids.csv","w") as f:
        i = 0
        for entry in entries:
            is_folder = False
            if 'contents' in entry:
                is_folder = True
                del entry['contents']
            entry['create_date'],entry['mod_date'] = random_datetime_string()
            entry['perms'] = random_weighted_permission_string(is_folder)
            if i == 0:
                print(entry.keys())
                i += 1
            print(list(entry.values()))
            vals = list(entry.values())
            f.write(','.join(vals))
            f.write("\n")


