import jinja2
import os
from datetime import datetime

def generate_evaluation_report(data, template_name='report_template.html', output_filename='evaluation_report.html'):
    """
    Generates an HTML evaluation report from a template and data.

    :param data: A dictionary containing the data for the report.
    :param template_name: The name of the Jinja2 template file.
    :param output_filename: The name of the output HTML file.
    """
    try:
        # Set up Jinja2 environment
        template_loader = jinja2.FileSystemLoader(searchpath=".")
        template_env = jinja2.Environment(loader=template_loader)
        template = template_env.get_template(template_name)

        # Render the template with the data
        output_html = template.render(data)

        # Write the output to a file
        with open(output_filename, 'w') as f:
            f.write(output_html)

        print(f"Successfully generated report: {os.path.abspath(output_filename)}")

    except jinja2.TemplateNotFound:
        print(f"Error: Template '{template_name}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    # --- Sample Data ---
    # In a real application, you would fetch this data from a database,
    # APIs, or other sources.

    report_data = {
        'employee_name': 'Yousif',
        'team': 'AIOps (Team Code Orbit)',
        'evaluation_period': 'Overall',
        'generation_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        
        'attendance_summary': {
            'total_days': 81,
            'present_days': 80,
            'absent_days': 1
        },
        'attendance_details': [
            {'date': '2025-07-22', 'status': 'Absent (1st Half) Arrived late'},
            {'date': '2025-07-24', 'status': 'Absent (2nd Half) Left early'}
        ],
        
        'sprint_velocity': [
            {'sprint': 'Sprint 1 & 2 [Overview & Datastructures]', 'committed': 100, 'delivered': ((30/50) * 100), 'plagiarism': 'Yes'},
            {'sprint': 'Sprint 3 & 4 [Computer Networks & APIs]', 'committed': 100, 'delivered': ((20/50) * 100), 'plagiarism': 'Yes'},
            {'sprint': 'Sprint 5 & 6 [Databases & REST API]', 'committed': 100, 'delivered': ((15/50) * 100), 'plagiarism': 'No'},
            {'sprint': 'Sprint 7 & 8 [Data Analysis & Machine Learning]', 'committed': 100, 'delivered': ((33.3/50) * 100), 'plagiarism': 'Yes'},
        ],
        
        'monthly_evaluation': {
            'Overall Performance': 'Below Average',
            'Monthly Progress': [
                {'month': 'April', 'percentage': 16, 'notes': 'Most of the coding related solutions were left empty.'},
                {'month': 'May', 'percentage': 49.3, 'notes': 'Only a warning for copy/pasting was issued. JPlag detected plagiarism in submissions.'},
                {'month': 'June', 'percentage': 0, 'notes': "Didn't submit"},
                {'month': 'July', 'percentage': 0, 'notes': 'Submitted but failed the viva and unable to explain anything.'}
            ],
            'Key Strengths': [
                'He can speak for his team.',
                'He clearly states if he feels something is wrong.',
            ],
            'Areas for Improvement': [
                'Avoid copying others, try to understand the task and complete it independently.',
                'Reduce the dependency on others for task completion.',
                'Utilize the time effectively to complete the tasks.',
                'Focus on the sessions and try to come up with questions.',
                'Focus on self upskilling rather than thinking about other matters.',
                'Improve the selection of words to communicate without causing misunderstandings.'
            ]
        },
        
        'trainers_feedback': [
            'He is not able to focus during the sessions thus unable to answer any question that is asked.',
            'His mind is usually occupied with other thoughts preventing him from engaging at all.',
            'He seems to have no interest in programming, although he has the potential to do well if he develops interest like he did participate well in the "Databases" sessions.',
            'He has to be extremely consistent in practice, so he can start understanding the basics and start catching up.'
        ]
    }

    # Generate the report
    generate_evaluation_report(report_data)