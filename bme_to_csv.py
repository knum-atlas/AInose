import json
import csv

# lokalizacja oryginalnego pliku
with open(r'C:\Users\maksk\My Drive\studia\atlas\bosch\test program\fake_goodgirl_sample.bmespecimen', 'r') as file:
    data = json.load(file)

# wyciagniecie data points
data_points = data['data']['specimenDataPoints']
cycles = data['data']['cycles']

# mapowa id cykli na id sensorow
cycle_id_to_sensor_id = {cycle['id']: cycle['sensorId'] for cycle in cycles}

# kolumnty w csv
column_labels = ["Data Point ID", "Resistance Gassensor", "Temperature", "Pressure", "Relative Humidity", "Time Since PowerOn", "Real time clock", "Error Code", "Cycle Step Index", "Cycle ID", "Sensor ID"]

# lokalizacja pliku output
with open(r'C:\Users\maksk\onedrive\Desktop\output.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(column_labels)
    for data_point in data_points:
        # sensor id
        cycle_id = data_point[-1]  # cycle id zazwyczaj jest ostatnie w bloku danych
        sensor_id = cycle_id_to_sensor_id.get(cycle_id)
        # dopisanie sensor id do danych
        data_point.append(sensor_id)
        writer.writerow(data_point)
