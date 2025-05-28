from flask import Flask, render_template, request, make_response, session, flash, redirect, url_for
from Counting_Algo import get_counts
from Even_Number_Filter import EvenFirstDigit
from comb_sort import combSort
import pandas as pd
import csv
import time
import os
import math
from io import StringIO

app = Flask(__name__)
app.secret_key = 'GeorgiaGwenGraciellaGirlie'

@app.route('/')
def portfolio():
    return render_template('portfolio.html')

@app.route('/act1', methods=['GET', 'POST'])
def activity1():
    if request.method == 'POST':
        action = request.form.get('action')
        counts = get_counts()
        if action == "save":
            # Create CSV in memory
            si = StringIO()
            writer = csv.writer(si)
            writer.writerow(["Category", "Count"])
            writer.writerow(["Males", counts['males']])
            writer.writerow(["Females", counts['females']])
            writer.writerow(["Computers", counts['computers']])
            # Optionally add lists:
            writer.writerow([])
            writer.writerow(["Student List"])
            for student in counts['students']:
                writer.writerow([student])
            writer.writerow([])
            writer.writerow(["Lab Equipment List"])
            for item in counts['lab']:
                writer.writerow([item])

            output = make_response(si.getvalue())
            output.headers["Content-Disposition"] = "attachment; filename=CountingAlgorithm.csv"
            output.headers["Content-type"] = "text/csv"
            return output
        return render_template('Act1.html', 
                                show_results=True, 
                                males=counts['males'], 
                                females=counts['females'], 
                                computers=counts['computers'], 
                                students=counts['students'], 
                                lab=counts['lab'])
    return render_template('Act1.html', show_results=False)

@app.route('/act2', methods=['GET', 'POST'])
def activity2():
    show_results = False
    filtered_results = {}

    if request.method == 'POST':
        action = request.form.get('action')

        if action == "filter_even_first_digit":
            file = request.files['csv_file']
            if not file:
                return render_template('Act2.html', error="No file uploaded.")

            try:
                df = pd.read_csv(file)
                df.columns = df.columns.str.strip()
                if "Number1" not in df.columns:
                    return render_template('Act2.html', error="CSV must contain 'Number1' column.")

                # Use the modified function
                filtered_results = EvenFirstDigit(df)
                session['filtered_results'] = filtered_results
                show_results = True
            except Exception as e:
                return render_template('Act2.html', error=f"Error reading CSV: {e}")

        elif action == "save":
            # Handle CSV download
            filtered_results = session.get('filtered_results', {})
            if not any(filtered_results.values()):
                return render_template('Act2.html', error="No results to save. Filter first!")
            
            # Create CSV in memory
            si = StringIO()
            writer = csv.writer(si)
            
            # Write headers
            writer.writerow(['Number', 'Status'])
            
            # Write data with status labels
            status_map = {
                'even': 'Even First Digit',
                'odd': 'Odd First Digit',
                'invalid': 'Invalid Entry'
            }
            
            for category, status in status_map.items():
                for number in filtered_results.get(category, []):
                    writer.writerow([number, status])
            
            # Create download response
            output = make_response(si.getvalue())
            output.headers["Content-Disposition"] = "attachment; filename=EvenFilteredResults.csv"
            output.headers["Content-type"] = "text/csv"
            return output
        if not filtered_results:
            filtered_results = session.get('filtered_results', {})

    return render_template(
        'Act2.html',
        show_results=show_results,
        filtered_results=filtered_results)

@app.route('/act3', methods=['GET', 'POST'])
def activity3():
    #sorted_data = None
    #execution_time = None
    #order = None
    #page = request.args.get('page', 1, type=int)
    #page_size = 30
    if request.method == 'POST':
        action = request.form.get('action')
        order = request.form.get('order')

        if action == 'save':
            sorted_data = session.get('sorted_data')
            order = session.get('order')

            if not sorted_data:
                flash("No sorted data to save. Please sort first.")
                return render_template('Act3.html')

            si = StringIO()
            writer = csv.writer(si)
            writer.writerow(['Model', 'No_of_ratings'])
            for row in sorted_data:
                writer.writerow([row['Model'], row['No_of_ratings']])

            output = make_response(si.getvalue())
            output.headers["Content-Disposition"] = f"attachment; filename=SortedRatings_{order}.csv"
            output.headers["Content-type"] = "text/csv"
            return output

        if order not in ['ascending', 'descending']:
            flash("Please select a valid sorting order.")
            return render_template('Act3.html')

        uploaded_file = request.files.get('csv_file')
        if uploaded_file and uploaded_file.filename != '':
            try:
                df = pd.read_csv(uploaded_file)
            except Exception as e:
                flash(f"Error reading uploaded CSV file: {e}")
                return render_template('Act3.html')
        else:
            if not os.path.exists(csvFile):
                flash("Default CSV file not found and no file uploaded.")
                return render_template('Act3.html')
            df = pd.read_csv(csvFile)

        if "No_of_ratings" not in df.columns:
            flash("CSV file error: 'No_of_ratings' column not found.")
            return render_template('Act3.html')

        df["No_of_ratings"] = df["No_of_ratings"].replace({',': ''}, regex=True)
        df["No_of_ratings"] = pd.to_numeric(df["No_of_ratings"], errors='coerce')
        df = df.dropna(subset=["No_of_ratings"])

        ratings_list = df['No_of_ratings'].tolist()
        sorted_ratings, execution_time = combSort(ratings_list, order)

        df['No_of_ratings'] = sorted_ratings
        dfSorted = df.sort_values(by=['No_of_ratings', 'Model'], ascending=(order == 'ascending'))

        sorted_data = dfSorted[['Model', 'No_of_ratings']].to_dict(orient='records')

        session['sorted_data'] = sorted_data
        session['order'] = order

        return render_template('Act3.html',
                               sorted_data=sorted_data,
                               execution_time=execution_time,
                               order=order,
                               page=1,
                               total_pages=1)

    return render_template('Act3.html')

@app.route('/act4', methods=['GET', 'POST'])
def activity4():
    return render_template('Act4.html')

@app.route('/act5', methods=['GET', 'POST'])
def activity5():
    return render_template('Act5.html')

if __name__ == '__main__':
    app.run(debug=True)
