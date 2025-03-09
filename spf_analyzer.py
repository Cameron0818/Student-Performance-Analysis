#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Jan 28 10:04:26 2025
Based on: https://www.kaggle.com/datasets/lainguyn123/student-performance-factors
Sample input: --TASK="1"
@author: rivera
@author: STUDENT_ID
"""

'''
This code was commented by Deepseek AI
'''

import pandas as pd

def process_csv() -> pd.DataFrame:
    """Read and return processed CSV data from 'data/a2-data.csv'.
    
    Returns:
        pd.DataFrame: DataFrame containing loaded student performance data.
    """
    a2_data_df: pd.DataFrame = pd.read_csv('data/a2-data.csv') 
    return a2_data_df

def task1(data: pd.DataFrame) -> None:
    """Generate CSV of students who studied more than 40 hours.
    
    Filters dataset to include only students with >40 study hours, keeping
    Record_ID, Hours_Studied and Exam_Score. Outputs to 'output.csv'.
    
    Args:
        data (pd.DataFrame): Input student performance data
    """
    data = data.loc[data['Hours_Studied'] > 40, ['Record_ID','Hours_Studied','Exam_Score']]
    data.to_csv('output.csv', index=False)
    return

def task2(data: pd.DataFrame) -> None:
    """Generate top 10 highest exam scores (>=85) with tie-breakers.
    
    Filters for scores >=85, sorts by descending Exam_Score and ascending Record_ID,
    outputs top 10 results to 'output.csv'.
    
    Args:
        data (pd.DataFrame): Input student performance data
    """
    data = (data.loc[data['Exam_Score'] >= 85, ['Record_ID','Hours_Studied','Exam_Score']]
        .sort_values(by = ['Exam_Score', 'Record_ID'], ascending = [False, True])
        .head(10))
    data.to_csv('output.csv', index=False)
    return

def task3(data: pd.DataFrame) -> None:
    """Generate records for students with perfect attendance and extracurriculars.
    
    Filters for students with 100% attendance and extracurricular activities,
    outputs Record_ID and Exam_Score to 'output.csv'.
    
    Args:
        data (pd.DataFrame): Input student performance data
    """
    data = data.loc[(data['Extracurricular_Activities'] == 'Yes') & (data['Attendance'] == 100), 
        ['Record_ID', 'Exam_Score']]
    data.to_csv('output.csv', index=False)
    return

def task4(data: pd.DataFrame) -> None:
    """Calculate average attendance per grade category.
    
    Converts scores to letter grades, calculates mean attendance per grade,
    and outputs sorted results to 'output.csv'.
    
    Args:
        data (pd.DataFrame): Input student performance data
    """
    # Convert columns to numeric types (handling invalid entries)
    data = data.copy()
    data['Exam_Score'] = pd.to_numeric(data['Exam_Score'], errors='coerce')
    data['Attendance'] = pd.to_numeric(data['Attendance'], errors='coerce')

    def assign_grade(score: float) -> str:
        """Map numerical exam score to letter grade.
        
        Args:
            score (float): Numerical exam score (0-100)
            
        Returns:
            str: Corresponding letter grade or None for invalid scores
        """
        if pd.isna(score):
            return None
        if 90 <= score:
            return 'A+'
        elif 85 <= score < 90:
            return 'A'
        elif 80 <= score < 85:
            return 'A-'
        elif 77 <= score < 80:
            return 'B+'
        elif 73 <= score < 77:
            return 'B'
        elif 70 <= score < 73:
            return 'B-'
        elif 65 <= score < 70:
            return 'C+'
        elif 60 <= score < 65:
            return 'C'
        elif 50 <= score < 60:
            return 'D'
        elif 0 <= score < 50:
            return 'F'
        else:
            return None  # Handles scores >100

    # Apply grading and clean data
    data['Grade'] = data['Exam_Score'].apply(assign_grade)
    data = data.dropna(subset=['Grade', 'Attendance'])  # Remove invalid entries

    # Configure categorical sorting for grade order
    grade_order = ['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'D', 'F']
    data['Grade'] = pd.Categorical(data['Grade'], categories=grade_order, ordered=True)

    # Calculate and format results
    result = (
        data.groupby('Grade', as_index=False, observed=True)
        ['Attendance'].mean()
        .round(1)
        .sort_values('Grade')
    )

    result.to_csv('output.csv', index=False)
    return

def task5(data: pd.DataFrame) -> None:
    """Identify top 50 students with above-average tutoring for their grade.
    
    Groups students by simplified letter grades, compares individual tutoring
    sessions to group average, outputs top 50 performers to 'output.csv'.
    
    Args:
        data (pd.DataFrame): Input student performance data
    """
    def assign_grade(score: float) -> str:
        """Simplified grade mapping for tutoring analysis."""
        if score >= 80:
            return 'A'
        elif 70 <= score < 80:
            return 'B'
        elif 60 <= score < 70:
            return 'C'
        elif 50 <= score < 60:
            return 'D'
        else:
            return 'F'
    
    # Add grades and calculate group averages
    data['Grade'] = data['Exam_Score'].apply(assign_grade)
    grade_avg_tutoring = data.groupby('Grade')['Tutoring_Sessions'].mean().round(1).to_dict()
    
    # Create comparison column and sort results
    data['Grade_Average_Tutoring_Sessions'] = data['Grade'].map(grade_avg_tutoring)
    data['Above_Average'] = data['Tutoring_Sessions'] > data['Grade_Average_Tutoring_Sessions']
    
    result = data[['Record_ID', 'Tutoring_Sessions', 'Grade_Average_Tutoring_Sessions', 
                  'Above_Average', 'Exam_Score', 'Grade']]
    
    result = result.sort_values(by=['Exam_Score', 'Record_ID'], ascending=[False, True]).head(50)
    
    result.to_csv('output.csv', index=False)
    return

def main():
    """Main entry point for command line execution.
    
    Parses TASK argument and executes corresponding analysis task.
    """
    import sys
    import argparse
    
    # Configure command line argument parsing
    parser = argparse.ArgumentParser(description='Student Performance Factor Analyzer')
    parser.add_argument('--TASK', type=str, help='Task number to execute (1-5)')
    
    args = parser.parse_args()
    
    # Load data and execute task
    data = process_csv()
    
    task_mapping = {
        "1": task1,
        "2": task2,
        "3": task3,
        "4": task4,
        "5": task5
    }
    
    # Validate and run task
    selected_task = task_mapping.get(args.TASK)
    if selected_task:
        selected_task(data)
    else:
        print("Invalid task number. Please specify a task between 1 and 5.")
        sys.exit(1)
    
if __name__ == '__main__':
    main()