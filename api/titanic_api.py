from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from model.titanic import TitanicModel

titanic_api = Blueprint('titanic_api', __name__, url_prefix='/api/titanic')
api = Api(titanic_api)


class TitanicAPI:
    class _Predict(Resource):
        def post(self):
            data = request.get_json()
            if not data:
                return {'error': 'No data provided'}, 400
            try:
                model    = TitanicModel.get_instance()
                result   = model.predict(data)
                weights  = model.feature_weights()
                return jsonify({
                    'survive':         result['survive'],
                    'die':             result['die'],
                    'feature_weights': weights
                })
            except Exception as e:
                return {'error': str(e)}, 500

    api.add_resource(_Predict, '/predict')