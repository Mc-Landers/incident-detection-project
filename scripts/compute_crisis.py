import argparse, os, sys
import pandas as pd, os, datetime
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from fonctions.crisis_df.load_crisis_df import *
from fonctions.crisis_df.encode_crisis import * 
from fonctions.crisis_df.compute_crisis_column import *
from fonctions.crisis_df.save_crisis_df import *
from fonctions.param import DATA_ROOT

parser = argparse.ArgumentParser(description='Compute Crisis for Timestamp DF.')

if __name__ == '__main__':
    
    df = load_crisis_dataset()
    df = encode_crisis_dataset(df)
    df = compute_crisis_column(df)
    save_crisis(df)