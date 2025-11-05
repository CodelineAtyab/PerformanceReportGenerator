"""
Script to update key strengths, areas of improvement, and trainer feedback
for all individual report JSON files based on performance categories.
"""

import json
import os
from pathlib import Path

# Define the base directory
BASE_DIR = Path(__file__).resolve().parent
INDIVIDUAL_REPORTS_DIR = BASE_DIR / "transformed_data" / "individual_reports"

# Category 1: Top performers - Always available, consistent, smart, hard working
TOP_PERFORMERS = [
    "Fatma Almukhaini",
    "Quds",
    "Hajer",
    "Fatma Al-Balushi",
    "Al Zahra",
    "Mahmood",
    "Maha",
    "Duaa",
    "Deena"
]

# Category 2: Below average - Limited engagement, below expectations
BELOW_AVERAGE = [
    "Ahmed",
    "Nouf",
    "Sarah",
    "Ebaa",
    "Adham"
]

# Category 3: Average performers - Rest of the team members
# Will be determined by exclusion

def get_top_performer_feedback():
    """Generate feedback for top performers"""
    return {
        "Key Strengths": [
            "Consistently demonstrates exceptional problem-solving abilities and analytical thinking across all data science modules.",
            "Shows remarkable dedication and active engagement in training sessions, always prepared and eager to learn.",
            "Exhibits strong technical proficiency with steady progress in both programming fundamentals and advanced data science concepts."
        ],
        "Areas for Improvement": [
            "N/A considering their level"
        ],
        "trainers_feedback": [
            "It has been an absolute pleasure working with this trainee throughout the data science program. From day one, they demonstrated an exceptional combination of technical aptitude, dedication, and intellectual curiosity that set them apart. Their consistent availability and engagement in every training session reflected a genuine commitment to mastering the field of data science. What impressed me most was their natural problem-solving ability – they approached complex analytical challenges with confidence and creativity, often going beyond the basic requirements to explore deeper insights. Their steady progression in developing both technical and analytical skills has been remarkable to witness. They not only grasped fundamental concepts quickly but also showed the initiative to connect theoretical knowledge with practical applications. Their work ethic, combined with their smart approach to learning, makes them a valuable asset to any data science team. I have no doubt they will continue to excel in their data science journey and make meaningful contributions to any organization fortunate enough to have them. I wholeheartedly recommend them for advanced data science roles and am confident they will continue to grow and achieve great success in this field."
        ]
    }

def get_below_average_feedback():
    """Generate feedback for below average performers"""
    return {
        "Key Strengths": [
            "Shows potential in understanding basic data science concepts when actively engaged.",
            "Demonstrates willingness to participate when prompted and supported."
        ],
        "Areas for Improvement": [
            "Needs to significantly increase engagement and active participation during training sessions to fully grasp complex concepts.",
            "Should focus on developing stronger problem-solving skills through consistent practice and hands-on application.",
            "Must improve performance on assessments by dedicating more time to understanding core concepts and completing practice exercises.",
            "Would benefit from seeking help proactively and participating more actively in group discussions and collaborative activities."
        ],
        "trainers_feedback": [
            "Throughout the data science training program, this trainee showed limited engagement and participation in the learning process. Their current performance level, as reflected in assessment results, indicates they are not yet meeting the expected standards for this stage of training. During sessions, there was often a lack of active involvement, which impacted their ability to fully understand and apply complex data science concepts. Problem-solving activities revealed gaps in their analytical thinking and technical application skills. However, it's important to note that every learner has potential for growth. With a fundamental shift in approach – including more consistent attendance, greater focus during sessions, active participation in discussions, and dedicated practice outside of class time – there is an opportunity for meaningful improvement. I encourage them to take ownership of their learning journey, ask questions when concepts are unclear, and engage more deeply with the material. With sustained effort and commitment, they can bridge the current performance gap and develop the skills necessary to succeed in data science. I remain hopeful that with increased dedication and focus, they will be able to demonstrate their capabilities more effectively in future endeavors."
        ]
    }

def get_average_performer_feedback():
    """Generate feedback for average performers"""
    return {
        "Key Strengths": [
            "Maintains consistent attendance and demonstrates reliable commitment to completing assigned sprint tasks.",
            "Shows solid understanding of core data science concepts and can apply them effectively with guidance."
        ],
        "Areas for Improvement": [
            "Would benefit from taking more initiative in exploring advanced topics and challenging themselves beyond basic requirements.",
            "Should work on enhancing problem-solving speed and confidence when tackling complex analytical challenges independently."
        ],
        "trainers_feedback": [
            "I had the opportunity to work with this trainee throughout the data science training program, and they demonstrated a commendable level of dedication and consistency. Their attendance was reliable, and they consistently completed their sprint assignments, showing a solid work ethic and commitment to the learning process. They grasped core data science concepts well and were able to apply them effectively in structured assignments. Their problem-solving abilities are developing at a steady pace, and with the right foundation in place, they have good potential for growth. While their performance has been solid and dependable, I believe there is room for them to push themselves further. Encouraging them to explore topics beyond the curriculum, take on more challenging projects independently, and build greater confidence in tackling complex problems would help elevate their skills to the next level. With continued practice and a proactive approach to learning, I am confident they can enhance their analytical capabilities and technical proficiency. Overall, they have demonstrated the fundamentals needed to succeed in data science roles, and with focused effort on areas of improvement, they have the potential to grow into a stronger, more independent data science professional. I am optimistic about their continued development and future contributions to the field."
        ]
    }

def normalize_name(name):
    """Normalize name for comparison (lowercase, remove extra spaces)"""
    return name.lower().strip()

def get_feedback_by_name(employee_name):
    """Determine which feedback to use based on employee name"""
    normalized_name = normalize_name(employee_name)
    
    # Check if top performer
    if any(normalize_name(name) == normalized_name for name in TOP_PERFORMERS):
        return get_top_performer_feedback()
    
    # Check if below average
    if any(normalize_name(name) == normalized_name for name in BELOW_AVERAGE):
        return get_below_average_feedback()
    
    # Default to average performer
    return get_average_performer_feedback()

def update_report_file(file_path):
    """Update a single report file with appropriate feedback"""
    try:
        # Read the JSON file
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        employee_name = data.get("employee_name", "Unknown")
        
        # Get appropriate feedback
        feedback = get_feedback_by_name(employee_name)
        
        # Update the monthly_evaluation section
        if "monthly_evaluation" in data:
            data["monthly_evaluation"]["Key Strengths"] = feedback["Key Strengths"]
            data["monthly_evaluation"]["Areas for Improvement"] = feedback["Areas for Improvement"]
        
        # Update trainers_feedback
        data["trainers_feedback"] = feedback["trainers_feedback"]
        
        # Write back to file
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Updated: {employee_name} ({file_path.name})")
        
    except Exception as e:
        print(f"✗ Error updating {file_path.name}: {str(e)}")

def main():
    """Main function to update all report files"""
    print("=" * 70)
    print("Starting feedback update process...")
    print("=" * 70)
    
    # Get all JSON files in the individual_reports directory
    json_files = list(INDIVIDUAL_REPORTS_DIR.glob("*.json"))
    
    if not json_files:
        print("No JSON files found in the individual_reports directory!")
        return
    
    print(f"\nFound {len(json_files)} report files to update.\n")
    
    # Update each file
    for json_file in sorted(json_files):
        update_report_file(json_file)
    
    print("\n" + "=" * 70)
    print("Feedback update completed!")
    print("=" * 70)
    
    # Print summary by category
    print("\n" + "=" * 70)
    print("SUMMARY BY CATEGORY:")
    print("=" * 70)
    print(f"\nTop Performers ({len(TOP_PERFORMERS)}):")
    for name in TOP_PERFORMERS:
        print(f"  - {name}")
    
    print(f"\nBelow Average ({len(BELOW_AVERAGE)}):")
    for name in BELOW_AVERAGE:
        print(f"  - {name}")
    
    print(f"\nAverage Performers (remaining team members):")
    # Determine average performers by reading all files
    all_employees = []
    for json_file in json_files:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            all_employees.append(data.get("employee_name", "Unknown"))
    
    for emp in sorted(all_employees):
        if not any(normalize_name(name) == normalize_name(emp) for name in TOP_PERFORMERS + BELOW_AVERAGE):
            print(f"  - {emp}")
    
    print("\n")

if __name__ == "__main__":
    main()
