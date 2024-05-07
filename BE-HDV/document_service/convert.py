import io
import os
import shutil

import pandas as pd
class Convert():
    def __int__(self):
        pass
    def excel_to_json(self, file):
        file_name = os.path.join(os.getcwd(), 'temp.xlsx')

        with open(file_name, 'wb') as buffer:
            shutil.copyfileobj(file.file, buffer)
        try:
            df = pd.read_excel(file_name, engine='openpyxl')
            os.remove(file_name)
            return df.to_dict(orient="records")
        except Exception as e:
            print(e)
            os.remove(file_name)
            return False

    def json_to_excel(self, json_data, file_name):
        try:
            df = pd.DataFrame(json_data, columns=json_data[0].keys())
            df.to_excel(file_name, index=False)

            return True

        except Exception as e:
            print(e)
            return False