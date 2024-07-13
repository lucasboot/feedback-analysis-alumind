from flask import Blueprint, render_template

pages_routes = Blueprint('pages_routes', __name__)


@pages_routes.route('/report')
def report():
    # pegar os dados para passar
    # feedbacks = get_all_feedbacks()  
    return render_template('report.html', feedbacks=[])

@pages_routes.route('/simulation')
def simulation():
    # pegar os dados para passar
    # feedbacks = get_all_feedbacks()  
    return render_template('simulation.html')