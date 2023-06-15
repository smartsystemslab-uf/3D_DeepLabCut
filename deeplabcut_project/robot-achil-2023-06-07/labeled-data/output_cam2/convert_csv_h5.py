import pandas as pd

df = pd.read_csv('~/deeplabcut/3D_DeepLabCut/deeplabcut_project/robot-achil-2023-06-07/labeled-data/output_cam2/CollectedData_achil.csv')

df.to_hdf('CollectedData_achil.h5', 'data', mode='w', format='table')
del df    # allow df to be garbage collected
