import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import OneHotEncoder
from datetime import date
import os

class VisitorModel:
    """ML model to predict Poway-Midland Railroad visitor count."""
    _instance = None

    def __init__(self):
        self.model         = None
        self.weather_enc   = None
        self.train_enc     = None
        self.feature_cols  = None
        self._train()

    def _generate_data(self):
        """Generate training data based on real PMRR operating schedule and capacity."""
        import random
        random.seed(42)
        np.random.seed(42)

        HOLIDAYS = {
            date(2023,1,1), date(2023,1,16), date(2023,2,20), date(2023,5,29),
            date(2023,7,4), date(2023,9,4), date(2023,11,23), date(2023,12,25),
            date(2024,1,1), date(2024,1,15), date(2024,2,19), date(2024,5,27),
            date(2024,7,4), date(2024,9,2), date(2024,11,28), date(2024,12,25),
            date(2025,1,1), date(2025,1,20), date(2025,2,17), date(2025,5,26),
            date(2025,7,4), date(2025,9,1), date(2025,11,27), date(2025,12,25),
        }
        from datetime import timedelta
        EXPLICIT_SUNDAYS = {
            date(2024,3,10): None,  date(2024,3,17): 'cable', date(2024,3,24): 'speeder',
            date(2024,3,31): 'cable', date(2024,4,7): 'cable', date(2024,4,14): None,
            date(2024,4,21): 'cable', date(2024,4,28): 'speeder', date(2024,5,5): 'cable',
            date(2024,5,12): None, date(2024,5,19): 'cable', date(2024,5,26): 'speeder',
            date(2024,6,2): 'cable', date(2024,6,9): None, date(2024,6,16): 'cable',
            date(2024,6,23): 'speeder', date(2024,6,30): 'cable',
            date(2024,7,7): 'cable', date(2024,7,14): None, date(2024,7,21): 'cable',
            date(2024,7,28): 'speeder', date(2024,8,4): 'cable', date(2024,8,11): None,
            date(2024,8,18): 'cable', date(2024,8,25): 'speeder',
            date(2024,9,8): 'cable', date(2024,9,15): None, date(2024,9,22): 'cable',
            date(2024,9,29): 'speeder', date(2024,10,6): 'cable', date(2024,10,13): None,
            date(2024,10,20): 'cable', date(2024,10,27): 'speeder',
            date(2025,3,9): None, date(2025,3,16): 'cable', date(2025,3,23): 'speeder',
            date(2025,3,30): 'cable', date(2025,4,6): 'cable', date(2025,4,13): None,
            date(2025,4,20): 'cable', date(2025,4,27): 'speeder', date(2025,5,4): 'cable',
            date(2025,5,11): None, date(2025,5,18): 'cable', date(2025,5,25): 'speeder',
        }
        WEATHER_OPTIONS = ['sunny','sunny','sunny','cloudy','cloudy','rainy','windy']
        WEATHER_WEIGHTS = {'sunny':1.0,'cloudy':0.75,'rainy':0.30,'windy':0.50}
        MONTH_FACTOR    = {1:0.65,2:0.70,3:0.75,4:0.85,5:0.90,6:0.95,7:1.00,
                           8:0.98,9:0.90,10:0.85,11:0.75,12:0.72}

        records = []
        current = date(2023,1,1)
        end     = date(2025,12,31)
        while current <= end:
            dow        = current.weekday()
            is_holiday = current in HOLIDAYS
            if dow == 5:
                train_type = 'steam'; capacity = 65; rides = 16
            elif dow == 6:
                if current in EXPLICIT_SUNDAYS:
                    t = EXPLICIT_SUNDAYS[current]
                    if t is None: current += timedelta(days=1); continue
                    train_type = t
                else:
                    if 8 <= current.day <= 14: current += timedelta(days=1); continue
                    train_type = 'cable'
                capacity = 30; rides = 9
            else:
                current += timedelta(days=1); continue

            weather   = random.choice(WEATHER_OPTIONS)
            w_factor  = WEATHER_WEIGHTS[weather]
            m_factor  = MONTH_FACTOR[current.month]
            h_factor  = 1.25 if is_holiday else 1.0
            occupancy = 0.55 * w_factor * m_factor * h_factor
            occupancy = min(0.95, max(0.05, occupancy + np.random.normal(0, 0.06)))
            visitors  = int(round(capacity * rides * occupancy))
            records.append({
                'month': current.month, 'is_saturday': int(dow==5),
                'is_holiday': int(is_holiday), 'capacity': capacity,
                'rides': rides, 'weather': weather, 'train_type': train_type,
                'visitors': visitors
            })
            current += timedelta(days=1)
        return pd.DataFrame(records)

    def _train(self):
        df = self._generate_data()

        self.weather_enc = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
        self.train_enc   = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
        self.weather_enc.fit(df[['weather']])
        self.train_enc.fit(df[['train_type']])

        features = self._build_features(df)
        self.feature_cols = list(features.columns)
        self.model = GradientBoostingRegressor(n_estimators=100, random_state=42)
        self.model.fit(features, df['visitors'])

    def _build_features(self, df):
        w_cols = ['weather_' + c for c in self.weather_enc.categories_[0]]
        t_cols = ['train_'   + c for c in self.train_enc.categories_[0]]
        w_df   = pd.DataFrame(self.weather_enc.transform(df[['weather']]),   columns=w_cols)
        t_df   = pd.DataFrame(self.train_enc.transform(df[['train_type']]),  columns=t_cols)
        return pd.concat([df[['month','is_saturday','is_holiday','capacity','rides']], w_df, t_df], axis=1)

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def predict(self, month, is_saturday, is_holiday, weather, train_type):
        capacity  = 65 if is_saturday else 30
        rides     = 16 if is_saturday else 9
        row = pd.DataFrame([{
            'month': month, 'is_saturday': int(is_saturday),
            'is_holiday': int(is_holiday), 'capacity': capacity,
            'rides': rides, 'weather': weather, 'train_type': train_type
        }])
        features = self._build_features(row)
        pred = int(round(float(self.model.predict(features)[0])))
        pred = max(0, min(capacity * rides, pred))

        importances = self.model.feature_importances_
        weights = {f: float(i) for f, i in zip(self.feature_cols, importances)}
        return {
            'predicted_visitors': pred,
            'capacity':           capacity * rides,
            'occupancy_pct':      round(pred / (capacity * rides) * 100, 1),
            'feature_weights':    weights
        }


def initVisitor():
    VisitorModel.get_instance()