from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from model.visitor import VisitorModel

visitor_api = Blueprint('visitor_api', __name__, url_prefix='/api/visitor')
api = Api(visitor_api)

class VisitorAPI:
    class _Predict(Resource):
        def post(self):
            data = request.get_json()
            if not data:
                return {'error': 'No data provided'}, 400
            try:
                model  = VisitorModel.get_instance()
                result = model.predict(
                    month       = int(data.get('month', 6)),
                    is_saturday = bool(data.get('is_saturday', True)),
                    is_holiday  = bool(data.get('is_holiday', False)),
                    weather     = data.get('weather', 'sunny'),
                    train_type  = data.get('train_type', 'steam'),
                )
                return jsonify(result)
            except Exception as e:
                return {'error': str(e)}, 500

    api.add_resource(_Predict, '/predict')