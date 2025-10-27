import jinja2
import os
import json
from datetime import datetime
from collections import defaultdict


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PARENT_DIR = os.path.join(BASE_DIR, 'templates')
TRANSFORMED_DATA_DIR = os.path.join(BASE_DIR, 'transformed_data')
OUTPUT_DIR = os.path.join(BASE_DIR, 'output_reports')


def generate_evaluation_report(data, template_name='report_template.html', output_filename='evaluation_report.html'):
    """
    Generates an HTML evaluation report from a template and data.

    :param data: A dictionary containing the data for the report.
    :param template_name: The name of the Jinja2 template file.
    :param output_filename: The name of the output HTML file.
    """
    try:
        # Set up Jinja2 environment
        template_loader = jinja2.FileSystemLoader(searchpath=TEMPLATE_PARENT_DIR)
        template_env = jinja2.Environment(loader=template_loader)
        template = template_env.get_template(template_name)

        # Render the template with the data
        output_html = template.render(data)

        # Write the output to a file
        with open(os.path.join(OUTPUT_DIR, output_filename), 'w') as f:
            f.write(output_html)

        print(f"Successfully generated report: {os.path.abspath(os.path.join(OUTPUT_DIR, output_filename))}")

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
    # generate_evaluation_report(report_data)

    # for transformed_file in os.listdir(TRANSFORMED_DATA_DIR):
    #     if transformed_file.endswith('.json'):
    #         try:
    #             with open(os.path.join(TRANSFORMED_DATA_DIR, transformed_file), 'r', encoding='utf-8') as json_file:
    #                 json_file = json.load(json_file)

    #                 for month_name_key, month_data in json_file.items():
    #                     team_members_eval_data = defaultdict(dict)
    #                     # Iterate through each team member in the month and store performance data
    #                     for team_member_name_key, team_member_data in month_data.items():
    #                         if team_member_name_key != "sprint_info":
    #                             data_to_append = {}
    #                             for heading, value in team_member_data[-4:]:
    #                                 data_to_append[heading] = value
                                
    #                             if team_member_name_key not in team_members_eval_data:
    #                                 team_members_eval_data[team_member_name_key] = data_to_append
    #                             else:
    #                                 for heading, score in data_to_append.items():
    #                                     team_members_eval_data[team_member_name_key][heading] += score
                        
    #                     # Collects the monthly sprints information
    #                     collected_sprint_number = ""
    #                     collected_sprint_name = ""
    #                     for sprint_no, sprint_data in month_data['sprint_info'].items():
    #                         collected_sprint_number += f"{sprint_no.strip(':')} & "
    #                         collected_sprint_name += f"{sprint_data.get('name_of_sprint', '')} & "
    #                     collected_sprint_number = collected_sprint_number.strip(' & ')
    #                     collected_sprint_name = collected_sprint_name.strip(' & ')
    #                     print(f"Sprint Numbers: {collected_sprint_number}")
    #                     print(f"Sprint Names: {collected_sprint_name}")


    #             # output_file = transformed_file.replace('.json', '_report.html')
    #             # generate_evaluation_report(data, output_filename=output_file)
    #         except Exception as e:
    #             print(f"Failed to generate report for {transformed_file}: {e}")