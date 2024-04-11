import json 
import pandas as pd
import numpy as np


class DataDecoder:
    """
    Klasa służy do transformacji danych w formacie `json` do bardziej przyjaznej formy w postaci szeregów czasowych własności fizycznych gotowych do uczenia.
    
    # Argumenty:
    
    - `filepath: str` - ścieżka do pliku z pomiarami z elektronicznego nosa.
    """
    
    def __init__(self, filepath:str):
        with open(filepath, 'r') as f:
            self.raw_data = json.load(f)['data']

        self.__extract_measurements()
        
    def __extract_measurements(self): # metoda służy do szczytania i organizacji danych
        measurements = self.raw_data['specimenDataPoints']
        measurements = [{'resistancy': measurement[1],
                        'temperature': measurement[2],
                        'pressure': measurement[3],
                        'rel_humidity':measurement[4],
                        'real_time': measurement[6],
                        'cycle_step_id': measurement[8],
                        'cycle_id': measurement[9]} for measurement in measurements]
        
        measurements_df = pd.DataFrame(measurements)

        cycles = self.raw_data['cycles']
        cycles_df = pd.DataFrame(cycles)

        self.measurements = measurements_df.merge(cycles_df[['id', 'sensorId']], left_on='cycle_id', right_on='id', how='left')
        
        self.measurements = self.measurements.drop('id', axis = 1)
        
    def get_data_ts(self) -> list:
        """
        Funkcja zwraca listę z danymi w postaci szeregu czasowego.
        """
        dataset = []

        for sensor, sensor_frame in self.measurements.groupby('sensorId'):
            for cycle, cycle_frame in sensor_frame.groupby('cycle_step_id'):                
                dataset.append({'sensorId': sensor,
                                'cycle_step_id': cycle,
                                'resistancy': cycle_frame['resistancy'],
                                'temperature': cycle_frame['temperature'],
                                'rel_humidity': cycle_frame['rel_humidity'],
                                'pressure': cycle_frame['pressure']})
            
        return dataset

        

if __name__ == "__main__":
    import matplotlib.pyplot as plt


    encoder = DataDecoder('/home/piotr/Kodowanko/ATLAS/Nochal/data/jsons/próbki/5 kawa_pod.json')
    data_ts = encoder.get_data_ts()


    fig, axes = plt.subplots(nrows = 2, ncols = 2, figsize = (16, 12))
    axes = axes.flatten()
    example = data_ts[np.random.randint(0, len(data_ts) - 1)]
    
    
    fig.suptitle(f"Measurement features of {example['sensorId']}. sensor within {example['cycle_step_id']}. cycle")
    
    for i, feature in enumerate(['resistancy', 'rel_humidity', 'pressure', 'temperature']):
        axes[i].plot(example[feature])
        axes[i].set_title(feature)