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
        'employee_name': 'Jane Smith',
        'team': 'Phoenix DevOps',
        'evaluation_period': 'July 2025',
        'generation_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        
        'attendance_summary': {
            'total_days': 22,
            'present_days': 20,
            'absent_days': 2
        },
        'attendance_details': [
            {'date': '2025-07-07', 'status': 'Absent'},
            {'date': '2025-07-18', 'status': 'Absent'},
        ],
        
        'sprint_velocity': [
            {'sprint': 'Sprint 25.1', 'committed': 30, 'delivered': 28},
            {'sprint': 'Sprint 25.2', 'committed': 35, 'delivered': 35},
            {'sprint': 'Sprint 25.3', 'committed': 32, 'delivered': 34},
            {'sprint': 'Sprint 25.4', 'committed': 40, 'delivered': 38},
        ],
        
        'monthly_evaluation': {
            'Overall Performance': 'Exceeds Expectations',
            'Key Strengths': [
                'Excellent problem-solving skills in CI/CD pipeline optimization.',
                'Proactive communication within the team.',
                'Strong grasp of containerization technologies (Docker, Kubernetes).'
            ],
            'Areas for Improvement': [
                'Could delegate tasks more effectively to junior team members.',
                'Expand knowledge in cloud cost management.'
            ]
        },
        
        'trainers_feedback': [
            'Jane is a quick learner and actively participates in advanced Kubernetes workshops.',
            'She has successfully applied concepts from the "Infrastructure as Code" training to real-world projects.',
            'Her feedback on training materials is always insightful and helps improve the content for others.'
        ]
    }

    # Generate the report
    generate_evaluation_report(report_data)