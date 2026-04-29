#Yadwinder Singh , studentID 32205568

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class HealthcareWorkerEngagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Yadwinder Singh & 32205568")
        self.root.geometry("1000x700")
        self.root.configure(bg="#f4f6f8")

        self.version = "V1.2026"
        self.dataframe = None
        self.summary_data = {}

        self.setup_styles()
        self.create_gui()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Custom.TButton",
            font=("Arial", 11, "bold"),
            padding=(12, 8),
            foreground="black",
            background="#d9d9d9",
            borderwidth=1
        )

        style.map(
            "Custom.TButton",
            foreground=[("pressed", "black"), ("active", "black")],
            background=[("pressed", "#c0c0c0"), ("active", "#e6e6e6")]
        )

    def create_gui(self):
        header = tk.Frame(self.root, bg="#1f4e79", pady=10)
        header.pack(fill=tk.X)

        title_label = tk.Label(
            header,
            text="Healthcare Worker Engagement and Retention System",
            font=("Arial", 18, "bold"),
            fg="white",
            bg="#1f4e79"
        )
        title_label.pack()

        info_label = tk.Label(
            header,
            text=f"Developer: Yadwinder Singh | Student ID: 32205568 | Version: {self.version}",
            font=("Arial", 11),
            fg="white",
            bg="#1f4e79"
        )
        info_label.pack()

        button_frame = tk.Frame(self.root, bg="#f4f6f8", pady=15)
        button_frame.pack()

        ttk.Button(
            button_frame,
            text="Load Data",
            command=self.load_data,
            style="Custom.TButton"
        ).grid(row=0, column=0, padx=10, pady=10, ipadx=20)

        ttk.Button(
            button_frame,
            text="Process & Summarize Data",
            command=self.process_data,
            style="Custom.TButton"
        ).grid(row=0, column=1, padx=10, pady=10, ipadx=20)

        ttk.Button(
            button_frame,
            text="Pie Chart (Department)",
            command=self.show_pie_chart,
            style="Custom.TButton"
        ).grid(row=0, column=2, padx=10, pady=10, ipadx=20)

        ttk.Button(
            button_frame,
            text="Bar Chart (Gender)",
            command=self.show_bar_chart,
            style="Custom.TButton"
        ).grid(row=0, column=3, padx=10, pady=10, ipadx=20)

        ttk.Button(
            button_frame,
            text="Dashboard",
            command=self.show_dashboard,
            style="Custom.TButton"
        ).grid(row=1, column=1, padx=10, pady=10, ipadx=20)

        ttk.Button(
            button_frame,
            text="Generate report.txt",
            command=self.generate_report,
            style="Custom.TButton"
        ).grid(row=1, column=2, padx=10, pady=10, ipadx=20)

        self.status_label = tk.Label(
            self.root,
            text="Please load a CSV file to begin.",
            font=("Arial", 11, "italic"),
            bg="#f4f6f8",
            fg="#333333"
        )
        self.status_label.pack(pady=5)

        self.text_area = tk.Text(self.root, width=120, height=28, font=("Courier New", 10))
        self.text_area.pack(padx=15, pady=10)

    def load_data(self):
        file_path = filedialog.askopenfilename(
            title="Select CSV File",
            filetypes=[("CSV Files", "*.csv")]
        )

        if not file_path:
            return

        try:
            self.dataframe = pd.read_csv(file_path)

            required_columns = [
                "EmployeeID", "Age", "Gender", "MaritalStatus", "Education",
                "Department", "JobRole", "HourlyRate", "YearsAtCompany",
                "YearsInCurrRole", "DistanceFromHome", "BusinessTravel",
                "WorkLifeBalance", "YearsLastPromotion", "YearsCurrManager", "Attrition"
            ]

            missing_columns = [col for col in required_columns if col not in self.dataframe.columns]

            if missing_columns:
                messagebox.showerror(
                    "Missing Columns",
                    f"The CSV file is missing these required columns:\n{missing_columns}"
                )
                self.dataframe = None
                return

            self.status_label.config(text=f"Data loaded successfully: {file_path}")
            self.text_area.delete("1.0", tk.END)
            self.text_area.insert(tk.END, "First 10 rows of the loaded dataset:\n\n")
            self.text_area.insert(tk.END, str(self.dataframe.head(10)))
            messagebox.showinfo("Success", "CSV data loaded successfully.")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load CSV file.\n{e}")

    def process_data(self):
        if self.dataframe is None:
            messagebox.showwarning("No Data", "Please load a CSV file first.")
            return

        try:
            df = self.dataframe.copy()

            total_employees = len(df)
            unique_departments = df["Department"].unique().tolist()
            different_education_levels = df["Education"].nunique()
            single_count = (df["MaritalStatus"] == "Single").sum()
            divorced_count = (df["MaritalStatus"] == "Divorced").sum()

            min_years = df["YearsAtCompany"].min()
            max_years = df["YearsAtCompany"].max()
            avg_years = df["YearsAtCompany"].mean()

            min_distance = df["DistanceFromHome"].min()
            max_distance = df["DistanceFromHome"].max()
            avg_distance = df["DistanceFromHome"].mean()

            min_hourly = df["HourlyRate"].min()
            max_hourly = df["HourlyRate"].max()
            avg_hourly = df["HourlyRate"].mean()

            marital_percentages = df["MaritalStatus"].value_counts(normalize=True) * 100
            single_percentage = marital_percentages.get("Single", 0)
            married_percentage = marital_percentages.get("Married", 0)
            divorced_percentage = marital_percentages.get("Divorced", 0)

            avg_work_life_balance = df["WorkLifeBalance"].mean()
            total_attritions = (df["Attrition"] == "Yes").sum()

            self.summary_data = {
                "Total number of employees": total_employees,
                "Unique departments": unique_departments,
                "Number of different education levels": different_education_levels,
                "Number of single employees": int(single_count),
                "Number of divorced employees": int(divorced_count),
                "Minimum years at company": float(min_years),
                "Maximum years at company": float(max_years),
                "Average years at company": float(avg_years),
                "Minimum distance from home": float(min_distance),
                "Maximum distance from home": float(max_distance),
                "Average distance from home": float(avg_distance),
                "Minimum hourly rate": float(min_hourly),
                "Maximum hourly rate": float(max_hourly),
                "Average hourly rate": float(avg_hourly),
                "Single percentage": float(single_percentage),
                "Married percentage": float(married_percentage),
                "Divorced percentage": float(divorced_percentage),
                "Average work-life balance": float(avg_work_life_balance),
                "Total attritions": int(total_attritions)
            }

            self.display_summary()
            messagebox.showinfo("Success", "Data processed and summarized successfully.")

        except Exception as e:
            messagebox.showerror("Error", f"Error while processing data.\n{e}")

    def display_summary(self):
        self.text_area.delete("1.0", tk.END)
        self.text_area.insert(tk.END, "OVERALL SUMMARY\n")
        self.text_area.insert(tk.END, "=" * 70 + "\n\n")

        for key, value in self.summary_data.items():
            if isinstance(value, float):
                self.text_area.insert(tk.END, f"{key}: {value:.2f}\n")
            else:
                self.text_area.insert(tk.END, f"{key}: {value}\n")

    def show_pie_chart(self):
        if self.dataframe is None:
            messagebox.showwarning("No Data", "Please load a CSV file first.")
            return

        department_counts = self.dataframe["Department"].value_counts()

        plt.figure(figsize=(8, 6))
        plt.pie(
            department_counts.values,
            labels=department_counts.index,
            autopct="%1.1f%%",
            startangle=90
        )
        plt.title("Employees by Department")
        plt.show()

    def show_bar_chart(self):
        if self.dataframe is None:
            messagebox.showwarning("No Data", "Please load a CSV file first.")
            return

        gender_counts = self.dataframe["Gender"].value_counts()

        plt.figure(figsize=(8, 6))
        plt.bar(gender_counts.index, gender_counts.values)
        plt.title("Employees by Gender")
        plt.xlabel("Gender")
        plt.ylabel("Number of Employees")
        plt.show()

    def show_dashboard(self):
        if self.dataframe is None:
            messagebox.showwarning("No Data", "Please load a CSV file first.")
            return

        if not self.summary_data:
            self.process_data()

        dashboard_window = tk.Toplevel(self.root)
        dashboard_window.title("Dashboard Summary")
        dashboard_window.geometry("1100x750")
        dashboard_window.configure(bg="white")

        title = tk.Label(
            dashboard_window,
            text="Healthcare Employee Dashboard",
            font=("Arial", 18, "bold"),
            bg="white",
            fg="#1f4e79"
        )
        title.pack(pady=10)

        metrics_frame = tk.Frame(dashboard_window, bg="white")
        metrics_frame.pack(pady=10)

        total_employees = self.summary_data.get("Total number of employees", 0)
        avg_work_life = self.summary_data.get("Average work-life balance", 0)
        total_attritions = self.summary_data.get("Total attritions", 0)
        attrition_rate = (total_attritions / total_employees * 100) if total_employees > 0 else 0

        metric_values = [
            ("Total Employees", total_employees),
            ("Avg Work-Life Balance", f"{avg_work_life:.2f}"),
            ("Total Attritions", total_attritions),
            ("Attrition Rate", f"{attrition_rate:.2f}%")
        ]

        for i, (label_text, value) in enumerate(metric_values):
            card = tk.Frame(metrics_frame, bg="#d6eaf8", bd=2, relief=tk.RIDGE, padx=20, pady=15)
            card.grid(row=0, column=i, padx=10, pady=10)

            tk.Label(card, text=label_text, font=("Arial", 12, "bold"), bg="#d6eaf8").pack()
            tk.Label(card, text=str(value), font=("Arial", 16, "bold"), bg="#d6eaf8", fg="#154360").pack()

        charts_frame = tk.Frame(dashboard_window, bg="white")
        charts_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        department_counts = self.dataframe["Department"].value_counts()
        fig1 = plt.Figure(figsize=(5, 4), dpi=100)
        ax1 = fig1.add_subplot(111)
        ax1.pie(department_counts.values, labels=department_counts.index, autopct="%1.1f%%", startangle=90)
        ax1.set_title("Department Distribution")

        canvas1 = FigureCanvasTkAgg(fig1, master=charts_frame)
        canvas1.draw()
        canvas1.get_tk_widget().grid(row=0, column=0, padx=20, pady=20)

        gender_counts = self.dataframe["Gender"].value_counts()
        fig2 = plt.Figure(figsize=(5, 4), dpi=100)
        ax2 = fig2.add_subplot(111)
        ax2.bar(gender_counts.index, gender_counts.values)
        ax2.set_title("Gender Distribution")
        ax2.set_xlabel("Gender")
        ax2.set_ylabel("Count")

        canvas2 = FigureCanvasTkAgg(fig2, master=charts_frame)
        canvas2.draw()
        canvas2.get_tk_widget().grid(row=0, column=1, padx=20, pady=20)

    def generate_report(self):
        if not self.summary_data:
            messagebox.showwarning("No Summary", "Please process the data first.")
            return

        try:
            with open("report.txt", "w", encoding="utf-8") as file:
                file.write("Healthcare Worker Engagement and Retention Report\n")
                file.write("=" * 60 + "\n\n")
                for key, value in self.summary_data.items():
                    if isinstance(value, float):
                        file.write(f"{key}: {value:.2f}\n")
                    else:
                        file.write(f"{key}: {value}\n")

            messagebox.showinfo("Success", "report.txt generated successfully in the project folder.")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate report.\n{e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = HealthcareWorkerEngagementApp(root)
    root.mainloop()