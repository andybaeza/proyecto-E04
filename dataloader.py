import csv
import uuid
from google.cloud import bigtable

project_name = 'project-60099802-d8b5-4aa9-a90'
instance_name = 'hbitossaludmental'
file = 'dataset.csv'

client = bigtable.Client(project=project_name, admin=True)
instance = client.instance(instance_name)
table = instance.table('habitossalud')
rows = []

with open(file) as fh:
    rd = csv.DictReader(fh, delimiter=',')
    for line in rd:
        line = dict(line)
        row_key = line['Daily_Screen_Time(hrs)'] + '#' + line['Exercise_Frequency(week)'] + '#' + line['Sleep_quaility'] + '#' + line['user_id']
        row = table.row(row_key)

        row.set_cell('demographic_data', 'age', line['Age'] )
        row.set_cell('demographic_data', 'gender', line['Gender'] )
        row.set_cell('tech_use', 'screen_time', line['Daily_Screen_Time(hrs)'] )
        row.set_cell('tech_use', 'days_wout_sm', line['Days_Without_Social_Media'] )
        row.set_cell('tech_use', 'sm_platform', line['Social_Media_Platform'] )
        row.set_cell('habits', 'sleep_quality', line['Sleep_Quality(1-10)'] )
        row.set_cell('habits', 'exercise_freq_week', line['Exercise_Frequency(week)'] )
        row.set_cell('habits', 'stress_level', line['Stress_Level(1-10)'] )
        row.set_cell('happines', 'happines_index', line['Happiness_Index(1-10)'] )

        rows.append(row)

table.mutate_rows(rows)
