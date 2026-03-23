import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import OneHotEncoder
from datetime import date, timedelta

class VisitorModel:
    """ML model to predict PMRR visitor count with enhanced features."""
    _instance = None

    def __init__(self):
        self.model        = None
        self.weather_enc  = None
        self.train_enc    = None
        self.temp_enc     = None
        self.feature_cols = None
        self._train()

    def _generate_data(self):
        import random
        random.seed(42)
        np.random.seed(42)

        SCHOOL_BREAKS = set()
        for yr in [2023,2024,2025]:
            d = date(yr,6,12)
            while d <= date(yr,8,13): SCHOOL_BREAKS.add(d); d += timedelta(days=1)
        for yr in [2022,2023,2024]:
            d = date(yr,12,18)
            while d <= date(yr+1,1,6): SCHOOL_BREAKS.add(d); d += timedelta(days=1)
        for yr in [2023,2024,2025]:
            d = date(yr,4,3)
            while d <= date(yr,4,11): SCHOOL_BREAKS.add(d); d += timedelta(days=1)
        for yr in [2023,2024,2025]:
            for mo in [11,12]:
                for day in ([20,21,22,23,24] if mo==11 else []):
                    SCHOOL_BREAKS.add(date(yr,mo,day))

        SPECIAL_EVENTS = {
            date(2023,7,4):'holiday_festival', date(2023,10,28):'halloween',
            date(2023,12,9):'holiday_festival', date(2024,4,20):'easter',
            date(2024,7,4):'holiday_festival', date(2024,10,26):'halloween',
            date(2024,12,7):'holiday_festival', date(2025,4,19):'easter',
            date(2025,7,4):'holiday_festival', date(2025,10,25):'halloween',
        }

        HOLIDAYS = {
            date(2023,1,1),date(2023,1,16),date(2023,2,20),date(2023,5,29),
            date(2023,7,4),date(2023,9,4),date(2023,11,23),date(2023,12,25),
            date(2024,1,1),date(2024,1,15),date(2024,2,19),date(2024,5,27),
            date(2024,7,4),date(2024,9,2),date(2024,11,28),date(2024,12,25),
            date(2025,1,1),date(2025,1,20),date(2025,2,17),date(2025,5,26),
            date(2025,7,4),date(2025,9,1),date(2025,11,27),date(2025,12,25),
        }

        EXPLICIT_SUNDAYS = {
            date(2024,3,10):None, date(2024,3,17):'cable', date(2024,3,24):'speeder',
            date(2024,3,31):'cable', date(2024,4,7):'cable', date(2024,4,14):None,
            date(2024,4,21):'cable', date(2024,4,28):'speeder', date(2024,5,5):'cable',
            date(2024,5,12):None, date(2024,5,19):'cable', date(2024,5,26):'speeder',
            date(2024,6,2):'cable', date(2024,6,9):None, date(2024,6,16):'cable',
            date(2024,6,23):'speeder', date(2024,6,30):'cable',
            date(2024,7,7):'cable', date(2024,7,14):None, date(2024,7,21):'cable',
            date(2024,7,28):'speeder', date(2024,8,4):'cable', date(2024,8,11):None,
            date(2024,8,18):'cable', date(2024,8,25):'speeder',
            date(2024,9,8):'cable', date(2024,9,15):None, date(2024,9,22):'cable',
            date(2024,9,29):'speeder', date(2024,10,6):'cable', date(2024,10,13):None,
            date(2024,10,20):'cable', date(2024,10,27):'speeder',
            date(2025,3,9):None, date(2025,3,16):'cable', date(2025,3,23):'speeder',
            date(2025,3,30):'cable', date(2025,4,6):'cable', date(2025,4,13):None,
            date(2025,4,20):'cable', date(2025,4,27):'speeder', date(2025,5,4):'cable',
            date(2025,5,11):None, date(2025,5,18):'cable', date(2025,5,25):'speeder',
        }

        WEATHER_OPTIONS = ['sunny','sunny','sunny','cloudy','cloudy','rainy','windy']
        WEATHER_WEIGHTS = {'sunny':1.0,'cloudy':0.75,'rainy':0.30,'windy':0.50}
        POWAY_AVG_TEMP  = {1:65,2:67,3:70,4:73,5:76,6:82,7:90,8:91,9:87,10:80,11:72,12:65}
        MONTH_FACTOR    = {1:0.65,2:0.70,3:0.75,4:0.85,5:0.90,6:0.95,7:1.00,
                           8:0.98,9:0.90,10:0.85,11:0.75,12:0.72}

        def temp_bucket(t):
            if t < 60: return 'cold'
            if t < 78: return 'mild'
            if t < 88: return 'warm'
            return 'hot'

        def temp_factor(t):
            if t < 55: return 0.60
            if t < 65: return 0.80
            if t < 78: return 1.00
            if t < 85: return 0.92
            if t < 92: return 0.78
            return 0.60

        records = []
        current = date(2023,1,1)
        while current <= date(2025,12,31):
            dow = current.weekday()
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

            weather       = random.choice(WEATHER_OPTIONS)
            w_factor      = WEATHER_WEIGHTS[weather]
            m_factor      = MONTH_FACTOR[current.month]
            h_factor      = 1.25 if is_holiday else 1.0
            is_school_brk = current in SCHOOL_BREAKS
            sb_factor     = 1.30 if is_school_brk else 1.0
            has_event     = current in SPECIAL_EVENTS
            ev_factor     = 1.45 if has_event else 1.0
            temp          = int(POWAY_AVG_TEMP[current.month] + np.random.normal(0, 6))
            tf            = temp_factor(temp)
            tb            = temp_bucket(temp)

            occupancy = 0.55 * w_factor * m_factor * h_factor * sb_factor * ev_factor * tf
            occupancy = min(0.98, max(0.05, occupancy + np.random.normal(0, 0.05)))
            visitors  = int(round(capacity * rides * occupancy))

            records.append({
                'month': current.month, 'day_of_month': current.day,
                'is_saturday': int(dow==5), 'is_holiday': int(is_holiday),
                'is_school_break': int(is_school_brk), 'has_event': int(has_event),
                'temperature': temp, 'temp_bucket': tb,
                'capacity': capacity, 'rides': rides,
                'weather': weather, 'train_type': train_type,
                'visitors': visitors
            })
            current += timedelta(days=1)
        return pd.DataFrame(records)

    def _train(self):
        df = self._generate_data()
        self.weather_enc = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
        self.train_enc   = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
        self.temp_enc    = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
        self.weather_enc.fit(df[['weather']])
        self.train_enc.fit(df[['train_type']])
        self.temp_enc.fit(df[['temp_bucket']])
        features          = self._build_features(df)
        self.feature_cols = list(features.columns)
        self.model        = GradientBoostingRegressor(n_estimators=150, random_state=42)
        self.model.fit(features, df['visitors'])

    def _build_features(self, df):
        w_cols = ['weather_' + c for c in self.weather_enc.categories_[0]]
        t_cols = ['train_'   + c for c in self.train_enc.categories_[0]]
        b_cols = ['temp_'    + c for c in self.temp_enc.categories_[0]]
        w_df   = pd.DataFrame(self.weather_enc.transform(df[['weather']]),   columns=w_cols)
        t_df   = pd.DataFrame(self.train_enc.transform(df[['train_type']]), columns=t_cols)
        b_df   = pd.DataFrame(self.temp_enc.transform(df[['temp_bucket']]), columns=b_cols)
        base   = df[['month','day_of_month','is_saturday','is_holiday',
                     'is_school_break','has_event','temperature','capacity','rides']]
        return pd.concat([base, w_df, t_df, b_df], axis=1)

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def predict(self, month, day_of_month, is_saturday, is_holiday,
                is_school_break, has_event, weather, train_type, temperature):
        capacity = 65 if is_saturday else 30
        rides    = 16 if is_saturday else 9
        if temperature < 60:   tb = 'cold'
        elif temperature < 78: tb = 'mild'
        elif temperature < 88: tb = 'warm'
        else:                  tb = 'hot'

        row = pd.DataFrame([{
            'month': month, 'day_of_month': day_of_month,
            'is_saturday': int(is_saturday), 'is_holiday': int(is_holiday),
            'is_school_break': int(is_school_break), 'has_event': int(has_event),
            'temperature': temperature, 'temp_bucket': tb,
            'capacity': capacity, 'rides': rides,
            'weather': weather, 'train_type': train_type
        }])
        features = self._build_features(row)
        pred     = int(round(float(self.model.predict(features)[0])))
        pred     = max(0, min(capacity * rides, pred))
        weights  = {f: float(i) for f, i in zip(self.feature_cols, self.model.feature_importances_)}
        return {
            'predicted_visitors': pred,
            'capacity':           capacity * rides,
            'occupancy_pct':      round(pred / (capacity * rides) * 100, 1),
            'feature_weights':    weights
        }

def initVisitor():
    VisitorModel.get_instance()