"""
Generate 500,000 synthetic farm records for RAPIDS benchmark
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import random

def generate_synthetic_farm_data(num_records=500000):
    """Generate synthetic farm performance data"""
    
    print(f"Generating {num_records:,} synthetic farm records...")
    
    # Base data
    crop_types = ["Rice", "Wheat", "Cotton", "Sugarcane", "Maize", "Pulses", "Soybean", "Potato", "Tomato", "Onion"]
    states = ["Punjab", "Haryana", "Maharashtra", "Karnataka", "Tamil Nadu", "Andhra Pradesh", "Uttar Pradesh", "Bihar", "West Bengal", "Gujarat"]
    districts = {
        "Punjab": ["Ludhiana", "Amritsar", "Jalandhar"],
        "Haryana": ["Karnal", "Ambala", "Hisar"],
        "Maharashtra": ["Nashik", "Pune", "Nagpur"],
        "Karnataka": ["Bengaluru Rural", "Mysuru", "Hassan"],
        "Tamil Nadu": ["Coimbatore", "Erode", "Salem"],
        "Andhra Pradesh": ["Krishna", "Guntur", "Anantapur"],
        "Uttar Pradesh": ["Meerut", "Saharanpur", "Lucknow"],
        "Bihar": ["Patna", "Gaya", "Muzaffarpur"],
        "West Bengal": ["Bardhaman", "Murshidabad", "Nadia"],
        "Gujarat": ["Ahmedabad", "Surat", "Vadodara"]
    }
    seasons = ["Kharif", "Rabi"]
    diseases_list = ["Leaf Blight", "Stem Rot", "Powdery Mildew", "Rust", "Bacterial Wilt", "None"]
    
    # Generate data
    data = []
    start_date = datetime(2024, 1, 1)
    
    for i in range(num_records):
        if i % 50000 == 0:
            print(f"Generated {i:,} records...")
        
        state = random.choice(states)
        district = random.choice(districts[state])
        crop = random.choice(crop_types)
        season = random.choice(seasons)
        year = random.randint(2023, 2026)
        
        # Farm characteristics
        farm_size = round(random.uniform(0.5, 50), 2)  # acres
        farm_id = f"FARM_{i+1:06d}"
        user_id = f"USER_{random.randint(1, 100000):06d}"
        
        # Performance metrics (correlated with farm practices)
        base_yield = {
            "Rice": 25, "Wheat": 30, "Cotton": 15, "Sugarcane": 700,
            "Maize": 28, "Pulses": 12, "Soybean": 18, "Potato": 250,
            "Tomato": 300, "Onion": 200
        }[crop]
        
        yield_variance = random.uniform(0.7, 1.3)
        crop_yield = round(base_yield * yield_variance * farm_size, 2)
        
        # Risk factors
        diseases_count = random.randint(0, 5)
        avg_risk_score = random.randint(0, 100)
        weather_score = random.randint(0, 100)
        
        # Higher diseases correlate with lower yield
        if diseases_count > 2:
            crop_yield *= 0.8
        
        # Location
        location = {
            "state": state,
            "district": district,
            "lat": round(random.uniform(8.0, 35.0), 6),
            "lng": round(random.uniform(68.0, 97.0), 6)
        }
        
        # Timestamp (distributed over 2 years)
        days_offset = random.randint(0, 730)
        timestamp = start_date + timedelta(days=days_offset)
        
        record = {
            "farm_id": farm_id,
            "user_id": user_id,
            "crop_type": crop,
            "farm_size_acres": farm_size,
            "yield_kg": crop_yield,
            "diseases_count": diseases_count,
            "avg_risk_score": avg_risk_score,
            "weather_score": weather_score,
            "location": json.dumps(location),
            "season": season,
            "year": year,
            "timestamp": timestamp.isoformat()
        }
        
        data.append(record)
    
    print(f"Generated {num_records:,} records successfully!")
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Save to CSV
    csv_filename = "farm_performance_500k.csv"
    df.to_csv(csv_filename, index=False)
    print(f"\nSaved to {csv_filename}")
    print(f"File size: {df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB")
    
    # Display sample
    print("\nSample data:")
    print(df.head(10))
    
    # Statistics
    print("\nDataset Statistics:")
    print(f"Total records: {len(df):,}")
    print(f"Unique farms: {df['farm_id'].nunique():,}")
    print(f"Unique users: {df['user_id'].nunique():,}")
    print(f"Date range: {df['timestamp'].min()} to {df['timestamp'].max()}")
    print(f"\nCrop distribution:")
    print(df['crop_type'].value_counts())
    
    return df

if __name__ == "__main__":
    df = generate_synthetic_farm_data(500000)
    print("\n✅ Synthetic data generation complete!")
    print("Next: Upload to BigQuery and run RAPIDS benchmark")
