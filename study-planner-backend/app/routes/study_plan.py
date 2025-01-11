from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

study_plan = Blueprint('study_plan', __name__)

@study_plan.route('/study-plan', methods=['POST'])
@jwt_required()
def create_study_plan():
    from app.DBmodels import StudyPlan
    from app import db

    data = request.json

    if not isinstance(data.get('subject'), str):
        print(f"Validation failed: {data.get('subject')} is of type {type(data.get('subject'))}")
        return jsonify({"msg": "Subject must be a string"}), 400

    user_id = get_jwt_identity()
    new_plan = StudyPlan(
        user_id=user_id,
        subject=data['subject'].strip(),
        hours_per_week=data['hours_per_week'],
        due_date=data['due_date']
    )
    db.session.add(new_plan)
    db.session.commit()

    return jsonify({"message": "Study plan created successfully!"}), 201

# Route: Fetch all study plans
@study_plan.route('/study-plan', methods=['GET'])
@jwt_required()
def get_study_plans():
    from app.DBmodels import StudyPlan
    user_id = get_jwt_identity()

    # Query all study plans for the authenticated user
    plans = StudyPlan.query.filter_by(user_id=user_id).all()

    # Convert plans to a list of dictionaries for JSON response
    plans_list = [
        {
            "id": plan.id,
            "subject": plan.subject,
            "hours_per_week": plan.hours_per_week,
            "due_date": plan.due_date.strftime('%Y-%m-%d')
        }
        for plan in plans
    ]

    return jsonify(plans_list), 200

# Route: Fetch a single study plan by ID
@study_plan.route('/study-plan/<int:plan_id>', methods=['GET'])
@jwt_required()
def get_study_plan(plan_id):
    from app.DBmodels import StudyPlan
    user_id = get_jwt_identity()

    # Query the study plan by ID and ensure it belongs to the authenticated user
    plan = StudyPlan.query.filter_by(id=plan_id, user_id=user_id).first()

    if not plan:
        return jsonify({"msg": "Study plan not found"}), 404

    # Convert the plan to a dictionary for JSON response
    plan_dict = {
        "id": plan.id,
        "subject": plan.subject,
        "hours_per_week": plan.hours_per_week,
        "due_date": plan.due_date.strftime('%Y-%m-%d')
    }

    return jsonify(plan_dict), 200

# editing study plans
@study_plan.route('/study-plan/<int:plan_id>', methods=['PUT'])
@jwt_required()
def update_study_plan(plan_id):
    from app.DBmodels import StudyPlan
    from app import db

    user_id = get_jwt_identity()
    data = request.json

    # Find the study plan by ID and check if it belongs to the logged-in user
    study_plan = StudyPlan.query.filter_by(id=plan_id, user_id=user_id).first()

    if not study_plan:
        return jsonify({"msg": "Study plan not found or you do not have access"}), 404

    # Update fields if provided in the request body
    if 'subject' in data:
        study_plan.subject = data['subject']
    if 'hours_per_week' in data:
        study_plan.hours_per_week = data['hours_per_week']
    if 'due_date' in data:
        study_plan.due_date = data['due_date']

    # Save changes to the database
    db.session.commit()
    return jsonify({"msg": "Study plan updated successfully!"}), 200

# Delete study plans 
@study_plan.route('/study-plan/<int:plan_id>', methods=['DELETE'])
@jwt_required()
def delete_study_plan(plan_id):
    from app.DBmodels import StudyPlan
    from app import db

    # Get the current user
    user_id = get_jwt_identity()

    # Find the study plan
    plan = StudyPlan.query.filter_by(id=plan_id, user_id=user_id).first()
    if not plan:
        return jsonify({"msg": "Study plan not found or unauthorized"}), 404

    # Delete the study plan
    db.session.delete(plan)
    db.session.commit()

    return jsonify({"msg": "Study plan deleted successfully"}), 200