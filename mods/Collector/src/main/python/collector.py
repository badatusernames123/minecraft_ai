# This is the main python file for the collector
from CollectorServer import CollectorServer
from Screenshot import Screenshot
import socket
import os
import pickle_tools
import csv
import re


##################################################
# Utility functions
##################################################

# Take a screenshot and update data file
def take_screenshot():
    screenshot = Screenshot()
    return screenshot

def store_image(image, path):
    # Split the path to get the directory structure
    directories = os.path.split(path)[0]

    # Ensure that the directory structure exists
    if not os.path.exists(directories):
        os.makedirs(directories)

    # Save the image
    image.store(path)

def append_to_csv(path, image_name, label):
    # Split the path to get the directory structure
    directories = os.path.split(path)[0]

    # Ensure that the directory structure exists
    if not os.path.exists(directories):
        os.makedirs(directories)

    # Append the data to the csv file
    with open(path, 'a') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([image_name, label])

##################################################
# Callback function
##################################################

def action_selector(message, collection_data, recog_map):
    if message.startswith('Block Recognition'):
        collection_data['n_screenshots'] += 1
        datapoint_id = 'image_' + str(collection_data['n_screenshots'])

        print('taking screenshot')
        screenshot = take_screenshot()
        store_image(screenshot, f'data/screenshots/{datapoint_id}.png')
        
        parts = message.split()
        blockstate_string = parts[2] 
        distance = float(parts[3])

        if blockstate_string not in recog_map:
            recog_map[blockstate_string] = len(recog_map) + 1
        blockstate_id = recog_map[blockstate_string]

        append_to_csv('datasets/recognition_labels.csv', datapoint_id, blockstate_id)
        append_to_csv('datasets/distance_labels.csv', datapoint_id, distance)
        print(f'Blockstate String: {blockstate_string} Distance: {distance}')
        print(f'Label stored: {datapoint_id} -> ({blockstate_id}, {distance})')


##################################################
# Startup
##################################################

print('Loading collection data')
collection_data = {'n_screenshots': 0}
collection_data = pickle_tools.load_from_pickle('mods/Collector/data/collection_data.pkl', collection_data)


print('Loading blockstate map')
recog_map = pickle_tools.load_from_pickle('mods/Collector/data/recog_map.pkl', dict())


ip = socket.gethostbyname(socket.gethostname())
server = CollectorServer(ip, 5050, action_selector, collection_data, recog_map)  # Use your desired IP and port
server.listen_for_clients()



