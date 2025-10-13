import pandas as pd
from datetime import datetime

def run_pipeline():
    df = pd.read_csv("customers.csv")
    df["AgeGroup"] = df["Age"].apply(lambda x: 'Young' if x < 30 else('Adult' if x < 50 else 'Senior'))
    df = df[df["Age"] > 20]
    df.to_csv("filtered_customers.csv", index=False)
    print(f"Pipeline completed at {datetime.now()}")

if __name__ == "__main__":
    run_pipeline()