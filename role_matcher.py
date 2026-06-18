import pandas as pd
import os

def load_career_dataset(filepath="career_dataset.csv"):
    """Loads the career dataset from a CSV file."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Dataset {filepath} not found.")
    return pd.read_csv(filepath)

def match_skills(extracted_skills: list, dataset_path="career_dataset.csv") -> list:
    """
    Matches the extracted skills against the dataset and returns
    the top 3 recommended roles along with match scores and missing skills.
    """
    try:
        df = load_career_dataset(dataset_path)
    except FileNotFoundError:
        return []

    # Normalize extracted skills for matching (lowercase, strip whitespace)
    extracted_skills_lower = [skill.lower().strip() for skill in extracted_skills]

    recommendations = []

    for index, row in df.iterrows():
        role = row['Role']
        required_skills = [s.strip() for s in row['Skills'].split(',')]
        required_skills_lower = [s.lower() for s in required_skills]

        # Calculate matches
        matched_skills = [skill for skill in required_skills if skill.lower() in extracted_skills_lower]
        missing_skills = [skill for skill in required_skills if skill.lower() not in extracted_skills_lower]
        
        # Calculate score: (Matched / Total Required) * 100
        total_required = len(required_skills)
        if total_required > 0:
            match_score = (len(matched_skills) / total_required) * 100
        else:
            match_score = 0.0

        recommendations.append({
            "role": role,
            "match_score": round(match_score, 2),
            "matched_skills": matched_skills,
            "missing_skills": missing_skills
        })

    # Sort by match score in descending order
    recommendations.sort(key=lambda x: x["match_score"], reverse=True)

    # Return top 3 recommendations
    return recommendations[:3]
