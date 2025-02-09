from flask import Flask, request, jsonify, render_template
import datetime

app = Flask(__name__)

def suggest_best_times_for_two_weeks():
    # Get the current date and time
    now = datetime.datetime.now()

    # Suggest the next best times for email outreach
    # General best practices: Tuesday to Thursday, 10 AM to 2 PM
    best_days = ['Tuesday', 'Wednesday', 'Thursday']
    best_hours = [10, 11, 12, 13, 14]

    suggested_times = []

    for day_offset in range(14):  # Check the next 14 days
        current_day = (now + datetime.timedelta(days=day_offset)).strftime('%A')
        if current_day in best_days:
            for hour in best_hours:
                suggested_time = now + datetime.timedelta(days=day_offset)
                suggested_time = suggested_time.replace(hour=hour, minute=0, second=0, microsecond=0)
                suggested_times.append(suggested_time)

    return suggested_times

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_best_times', methods=['POST'])
def get_best_times():
    user_input = request.json.get('user_input').strip().lower()
    if user_input == 'yes':
        best_times = suggest_best_times_for_two_weeks()
        response = []
        for time in best_times[:15]:  # Provide only the first 15 suggested times
            time_str = time.strftime('%A, %Y-%m-%d %H:%M:%S')
            if time.strftime('%H:%M:%S') == '12:00:00':
                response.append(f"Suggested time for email outreach: {time_str} (Note: People may be having lunch around this time)")
            else:
                response.append(f"Suggested time for email outreach: {time_str}")
        return jsonify(response)
    else:
        return jsonify(["No worries, have a good rest of your day!"])

if __name__ == '__main__':
    app.run(debug=True, port=5000)  # Change the port number here