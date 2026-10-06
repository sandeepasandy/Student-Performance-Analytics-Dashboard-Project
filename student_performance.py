import pandas as pd

# Student performance data
data = {
    "Name": ["Ravi", "Priya", "Arun", "Sita", "Kiran"],
    "Attendance": [85, 92, 70, 95, 80],
    "Maths": [78, 88, 65, 92, 75],
    "Science": [82, 90, 60, 95, 72],
    "English": [75, 85, 70, 90, 78]
}

# Create DataFrame
df = pd.DataFrame(data)

# Calculate average marks
df["Average"] = (
    df["Maths"] +
    df["Science"] +
    df["English"]
) / 3

# Calculate performance status
df["Status"] = df["Average"].apply(
    lambda x: "Excellent" if x >= 85
    else "Good" if x >= 70
    else "Needs Improvement"
)

# Display student data
print("\n===== STUDENT PERFORMANCE ANALYTICS =====\n")
print(df.to_string(index=False))

# Class average
class_average = df["Average"].mean()

print("\nClass Average:", round(class_average, 2))

# Top performer
top_student = df.loc[df["Average"].idxmax(), "Name"]
top_score = df["Average"].max()

print("Top Performer:", top_student)
print("Top Average:", round(top_score, 2))

# Students needing improvement
print("\n===== STUDENTS NEEDING IMPROVEMENT =====")

students_need_help = df[df["Status"] == "Needs Improvement"]

if len(students_need_help) > 0:
    print(students_need_help[["Name", "Average", "Status"]].to_string(index=False))
else:
    print("No students need improvement.")

# Save results
df.to_csv("student_performance_results.csv", index=False)

print("\nResults saved to student_performance_results.csv")