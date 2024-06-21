from flask import Flask, request, jsonify
import traceback
import fil


app = Flask(__name__)

@app.route('/execute_sql', methods=['POST'])
def execute_sql():
    data = request.get_json()
    sql_command = data.get('sql_command')

    if not sql_command:
        rows = fil.sql("""
            select
                scraped_at,
                company_name,
                job_title,
                location,
                job_page_url
            from jobs
            order by job_id desc
            ;""")

        # Convert the result to a list of dictionaries
        results = [dict(row) for row in rows]
        return jsonify(results), 200

    try:
        rows = fil.sql(sql_command)

        # Convert the result to a list of dictionaries
        results = [dict(row) for row in rows]
        return jsonify(results), 200

    except:
        error_msg = str(traceback.format_exc())
        return jsonify({"error": error_msg}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)