import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import mysql.connector
from fpdf import FPDF
from tkcalendar import DateEntry
import datetime
import re

# ==============================
# Database Handler
# ==============================
class DatabaseHandler:
    def __init__(self):
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Amogh@123",  # Update with your MySQL password
                database="resume"       # Update with your database name
            )
            self.cursor = self.conn.cursor()
        except Exception as e:
            messagebox.showerror("Database Connection Error", str(e))
    
    def execute(self, query, params=None):
        try:
            self.cursor.execute(query, params or ())
            self.conn.commit()
        except Exception as e:
            messagebox.showerror("DB Error", str(e))
    
    def fetchall(self, query, params=None):
        self.cursor.execute(query, params or ())
        return self.cursor.fetchall()
    
    def fetchone(self, query, params=None):
        self.cursor.execute(query, params or ())
        return self.cursor.fetchone()
    
    def close(self):
        self.cursor.close()
        self.conn.close()

db = DatabaseHandler()

# ==============================
# Validation Functions
# ==============================
def validate_email(email):
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(email_pattern, email))

def validate_contact(contact):
    contact_pattern = r'^\+\d{2}-\d{10}$'
    return bool(re.match(contact_pattern, contact))

def validate_year(year):
    if not year.isdigit() or len(year) != 4 or not (1900 <= int(year) <= datetime.datetime.now().year):
        return False
    return True

# ==============================
# PDF Resume Generator
# ==============================
class ResumePDF(FPDF):
    def __init__(self):
        super().__init__(orientation='P', unit='mm', format='A4')
        self.set_margins(20, 20, 20)  # Adjusted margins for better layout

    def header(self):
        pass  # No title

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def generate_resume_pdf(data):
    try:
        pdf = ResumePDF()
        pdf.add_page()

        # Faculty Name and Contact Information
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, f"{data.get('salutation', '')} {data.get('name', '')}", ln=True, align='C')
        pdf.ln(5)

        # Contact Details Section
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, "Contact Information", ln=True)
        pdf.set_font("Arial", size=10)
        contact_details = [
            f"Faculty ID: {data.get('faculty_id', 'N/A')}",
            f"Department: {data.get('department', 'N/A')}",
            f"Email: {data.get('email', 'N/A')}",
            f"Phone: {data.get('contact_no', 'N/A')}",
            f"LinkedIn: {data.get('linkedin', 'N/A')}",
            f"Google Scholar: {data.get('google_scholar_link', 'N/A')}",
            f"ORCID: {data.get('orcid', 'N/A')}",
            f"Website: {data.get('website', 'N/A')}"
        ]
        for detail in contact_details:
            if detail.split(": ")[1] != 'N/A':  # Only include non-empty fields
                pdf.set_x(20)
                pdf.multi_cell(170, 6, detail, align='L')
        pdf.ln(5)
        pdf.line(20, pdf.get_y(), 190, pdf.get_y())
        pdf.ln(5)

        # Professional Summary
        if data.get('objective'):
            pdf.set_font("Arial", 'B', 12)
            pdf.set_x(20)
            pdf.cell(0, 10, "Professional Summary", ln=True)
            pdf.set_font("Arial", size=10)
            pdf.set_x(20)
            pdf.multi_cell(170, 6, data['objective'], align='J')  # Justified text
            pdf.ln(5)
            pdf.line(20, pdf.get_y(), 190, pdf.get_y())
            pdf.ln(5)

        # Research Interests
        if data.get('research_interest'):
            pdf.set_font("Arial", 'B', 12)
            pdf.set_x(20)
            pdf.cell(0, 10, "Research Interests", ln=True)
            pdf.set_font("Arial", size=10)
            pdf.set_x(20)
            pdf.multi_cell(170, 6, data['research_interest'], align='J')
            pdf.ln(5)
            pdf.line(20, pdf.get_y(), 190, pdf.get_y())
            pdf.ln(5)

        # Education
        if data.get('education'):
            pdf.set_font("Arial", 'B', 12)
            pdf.set_x(20)
            pdf.cell(0, 10, "Education", ln=True)
            pdf.set_font("Arial", size=10)
            for edu in data['education']:
                pdf.set_x(20)
                pdf.multi_cell(170, 6, f"- {edu}", align='L')
            pdf.ln(5)
            pdf.line(20, pdf.get_y(), 190, pdf.get_y())
            pdf.ln(5)

        # Professional Experience
        if data.get('experience'):
            pdf.set_font("Arial", 'B', 12)
            pdf.set_x(20)
            pdf.cell(0, 10, "Professional Experience", ln=True)
            pdf.set_font("Arial", size=10)
            for exp in data['experience']:
                pdf.set_x(20)
                pdf.multi_cell(170, 6, f"- {exp}", align='L')
            pdf.ln(5)
            pdf.line(20, pdf.get_y(), 190, pdf.get_y())
            pdf.ln(5)

        # Publications
        if data.get('publications'):
            pdf.set_font("Arial", 'B', 12)
            pdf.set_x(20)
            pdf.cell(0, 10, "Selected Publications", ln=True)
            pdf.set_font("Arial", size=10)
            for pub in data['publications']:
                pdf.set_x(20)
                pdf.multi_cell(170, 6, f"- {pub}", align='L')
            pdf.ln(5)
            pdf.line(20, pdf.get_y(), 190, pdf.get_y())
            pdf.ln(5)

        # Professional Affiliations
        if data.get('professional_affiliation'):
            pdf.set_font("Arial", 'B', 12)
            pdf.set_x(20)
            pdf.cell(0, 10, "Professional Affiliations", ln=True)
            pdf.set_font("Arial", size=10)
            pdf.set_x(20)
            pdf.multi_cell(170, 6, data['professional_affiliation'], align='J')
            pdf.ln(5)
            pdf.line(20, pdf.get_y(), 190, pdf.get_y())
            pdf.ln(5)

        # Awards and Honors
        if data.get('awards'):
            pdf.set_font("Arial", 'B', 12)
            pdf.set_x(20)
            pdf.cell(0, 10, "Awards and Honors", ln=True)
            pdf.set_font("Arial", size=10)
            pdf.set_x(20)
            pdf.multi_cell(170, 6, data['awards'], align='J')
            pdf.ln(5)

        # Save PDF
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if not file_path:
            messagebox.showwarning("Cancelled", "PDF generation cancelled.")
            return
        pdf.output(file_path)
        messagebox.showinfo("Success", "Resume PDF generated successfully!")
    except Exception as e:
        messagebox.showerror("PDF Error", f"Failed to generate PDF: {str(e)}")

# ==============================
# Main Application GUI
# ==============================
class FacultyManagementApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Nagpur University Faculty Management System")
        self.geometry("1200x1000")
        self.configure(bg="#fff5e6")
        self.font_size = 10  # Initial font size
        
        # Bind zoom event
        self.bind_all("<Control-MouseWheel>", self.zoom)
        
        # Style Configuration
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TNotebook", background="#fff5e6", borderwidth=0)
        style.configure("TButton", font=("Segoe UI", 10), padding=6, background="#ff4500", foreground="#ffffff")
        style.configure("TLabel", font=("Segoe UI", 10), background="#fff5e6", foreground="#00008b")
        style.configure("Treeview", font=("Segoe UI", 10), rowheight=25, background="#fff5e6", foreground="#00008b")
        style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"), background="#fff5e6", foreground="#00008b")
        style.map("TNotebook.Tab", background=[("selected", "#ff4500")], foreground=[("selected", "#ffffff")])
        style.map("Treeview", background=[("selected", "#ff4500")], foreground=[("selected", "#ffffff")])
        
        # Developer Label
        tk.Label(self, text="Developed by Amogh Lanjewar", bg="#fff5e6", fg="gray", font=("Segoe UI", 8)).pack(anchor="ne", padx=10, pady=5)
        
        # Main Title
        tk.Label(self, text="Nagpur University Faculty Management System", bg="#fff5e6", fg="#00008b", font=("Segoe UI", 36, "bold")).pack(pady=10)
        
        # Notebook for Tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill='both')
        
        self.dept_tab = ttk.Frame(self.notebook)
        self.faculty_tab = ttk.Frame(self.notebook)
        self.view_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.dept_tab, text="Department Management")
        self.notebook.add(self.faculty_tab, text="Faculty Management")
        self.notebook.add(self.view_tab, text="View/Search/Resume")
        
        self.create_dept_tab()
        self.create_faculty_tab()
        self.create_view_tab()
        
        self.education_data = []
        self.experience_data = []
        self.publication_data = []
    
    def zoom(self, event):
        if event.delta > 0:
            self.font_size += 1
        else:
            self.font_size = max(8, self.font_size - 1)
        self.set_font_size(self, self.font_size)
    
    def set_font_size(self, widget, size):
        try:
            widget.configure(font=("Segoe UI", size))
        except:
            pass
        for child in widget.winfo_children():
            self.set_font_size(child, size)
    
    def create_dept_tab(self):
        container = ttk.Frame(self.dept_tab, padding=20)
        container.pack(expand=True, fill="both")
        
        ttk.Label(container, text="Department Name:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.dept_name_entry = ttk.Entry(container)
        self.dept_name_entry.grid(row=0, column=1, padx=10, pady=10)
        
        ttk.Label(container, text="Department Shortform:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.dept_short_entry = ttk.Entry(container)
        self.dept_short_entry.grid(row=1, column=1, padx=10, pady=10)
        
        ttk.Label(container, text="Subfield(s) (comma separated):").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.subfield_entry = ttk.Entry(container, width=50)
        self.subfield_entry.grid(row=2, column=1, padx=10, pady=10)
        
        ttk.Button(container, text="Save Department", command=self.save_department).grid(row=3, column=1, pady=20, sticky="e")
    
    def save_department(self):
        dept_name = self.dept_name_entry.get().strip()
        short_form = self.dept_short_entry.get().strip().upper()
        subfields = self.subfield_entry.get().strip().split(',')
        if not dept_name or not short_form:
            messagebox.showerror("Input Error", "Please provide both department name and shortform.")
            return
        
        query = "INSERT INTO departments (department_name, short_code) VALUES (%s, %s)"
        db.execute(query, (dept_name, short_form))
        dept_id = db.cursor.lastrowid
        for sf in subfields:
            if sf.strip():
                query = "INSERT INTO subfields (department_id, subfield_name) VALUES (%s, %s)"
                db.execute(query, (dept_id, sf.strip()))
        messagebox.showinfo("Success", "Department saved successfully!")
        self.dept_name_entry.delete(0, tk.END)
        self.dept_short_entry.delete(0, tk.END)
        self.subfield_entry.delete(0, tk.END)
        self.refresh_departments()
    
    def create_faculty_tab(self):
        container = ttk.Frame(self.faculty_tab, padding=20)
        container.pack(expand=True, fill="both")
        
        paned_window = ttk.PanedWindow(container, orient=tk.HORIZONTAL)
        paned_window.pack(fill="both", expand=True)
        
        left_frame = ttk.Frame(paned_window, padding=10)
        paned_window.add(left_frame, weight=2)
        
        basic_frame = ttk.LabelFrame(left_frame, text="Basic Information", padding=10)
        basic_frame.pack(fill="x", pady=10)
        
        ttk.Label(basic_frame, text="Salutation:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.salutation_entry = ttk.Entry(basic_frame)
        self.salutation_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(basic_frame, text="Full Name:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.name_entry = ttk.Entry(basic_frame)
        self.name_entry.grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Label(basic_frame, text="Department:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.dept_combo = ttk.Combobox(basic_frame, state="readonly")
        self.dept_combo.grid(row=1, column=1, padx=5, pady=5)
        self.dept_combo.bind("<<ComboboxSelected>>", self.load_subfields)
        self.refresh_departments()
        
        ttk.Label(basic_frame, text="Subfield:").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.subfield_combo = ttk.Combobox(basic_frame, state="readonly")
        self.subfield_combo.grid(row=1, column=3, padx=5, pady=5)
        
        ttk.Label(basic_frame, text="Faculty Type:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.faculty_type_entry = ttk.Entry(basic_frame)
        self.faculty_type_entry.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(basic_frame, text="Contact No. (e.g., +91-1234567890):").grid(row=2, column=2, padx=5, pady=5, sticky="w")
        self.contact_entry = ttk.Entry(basic_frame)
        self.contact_entry.grid(row=2, column=3, padx=5, pady=5)
        
        ttk.Label(basic_frame, text="Email:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.email_entry = ttk.Entry(basic_frame)
        self.email_entry.grid(row=3, column=1, padx=5, pady=5)
        
        ttk.Label(basic_frame, text="Google Scholar Link:").grid(row=3, column=2, padx=5, pady=5, sticky="w")
        self.gs_entry = ttk.Entry(basic_frame)
        self.gs_entry.grid(row=3, column=3, padx=5, pady=5)
        
        ttk.Label(basic_frame, text="ORCID:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.orcid_entry = ttk.Entry(basic_frame)
        self.orcid_entry.grid(row=4, column=1, padx=5, pady=5)
        
        ttk.Label(basic_frame, text="LinkedIn:").grid(row=4, column=2, padx=5, pady=5, sticky="w")
        self.linkedin_entry = ttk.Entry(basic_frame)
        self.linkedin_entry.grid(row=4, column=3, padx=5, pady=5)
        
        ttk.Label(basic_frame, text="Website:").grid(row=5, column=0, padx=5, pady=5, sticky="w")
        self.website_entry = ttk.Entry(basic_frame)
        self.website_entry.grid(row=5, column=1, padx=5, pady=5)
        
        additional_frame = ttk.LabelFrame(left_frame, text="Additional Details", padding=10)
        additional_frame.pack(fill="x", pady=10)
        
        ttk.Label(additional_frame, text="Objective:").grid(row=0, column=0, padx=5, pady=5, sticky="nw")
        self.objective_text = tk.Text(additional_frame, width=30, height=2)
        self.objective_text.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(additional_frame, text="Research Interest:").grid(row=0, column=2, padx=5, pady=5, sticky="nw")
        self.research_text = tk.Text(additional_frame, width=30, height=2)
        self.research_text.grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Label(additional_frame, text="Professional Affiliation:").grid(row=1, column=0, padx=5, pady=5, sticky="nw")
        self.affiliation_text = tk.Text(additional_frame, width=30, height=2)
        self.affiliation_text.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(additional_frame, text="Awards and Honors:").grid(row=1, column=2, padx=5, pady=5, sticky="nw")
        self.awards_text = tk.Text(additional_frame, width=30, height=2)
        self.awards_text.grid(row=1, column=3, padx=5, pady=5)
        
        ttk.Label(additional_frame, text="Current Status:").grid(row=2, column=0, padx=5, pady=5, sticky="nw")
        self.status_text = tk.Text(additional_frame, width=30, height=2)
        self.status_text.grid(row=2, column=1, padx=5, pady=5)
        
        right_frame = ttk.Frame(paned_window, padding=10)
        paned_window.add(right_frame, weight=1)
        
        subdetails_frame = ttk.Notebook(right_frame)
        subdetails_frame.pack(fill="both", expand=True)
        
        self.create_education_tab(subdetails_frame)
        self.create_experience_tab(subdetails_frame)
        self.create_publication_tab(subdetails_frame)
        
        ttk.Button(container, text="Save Faculty", command=self.save_faculty).pack(pady=20, anchor="e")
    
    def refresh_departments(self):
        result = db.fetchall("SELECT id, department_name FROM departments")
        self.dept_map = {dept_name: dept_id for dept_id, dept_name in result}
        self.dept_combo['values'] = list(self.dept_map.keys())
    
    def load_subfields(self, event):
        dept_name = self.dept_combo.get()
        dept_id = self.dept_map.get(dept_name)
        if dept_id:
            result = db.fetchall("SELECT id, subfield_name FROM subfields WHERE department_id=%s", (dept_id,))
            self.subfield_map = {subfield_name: sub_id for sub_id, subfield_name in result}
            self.subfield_combo['values'] = list(self.subfield_map.keys())
    
    def generate_faculty_id(self, dept_id):
        query = "SELECT short_code FROM departments WHERE id=%s"
        res = db.fetchone(query, (dept_id,))
        short_code = res[0] if res else "XX"
        query = "SELECT COUNT(*) FROM faculty WHERE department_id=%s"
        res = db.fetchone(query, (dept_id,))
        serial = int(res[0]) + 1 if res else 1
        return f"NU{short_code}{serial:03d}"
    
    def create_education_tab(self, parent):
        self.edu_frame = ttk.Frame(parent, padding=10)
        parent.add(self.edu_frame, text="Education")
        
        ttk.Label(self.edu_frame, text="Degree:").grid(row=0, column=0, padx=5, pady=5)
        self.degree_entry = ttk.Entry(self.edu_frame)
        self.degree_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(self.edu_frame, text="Institution:").grid(row=0, column=2, padx=5, pady=5)
        self.institution_entry = ttk.Entry(self.edu_frame)
        self.institution_entry.grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Label(self.edu_frame, text="Year (e.g., 2002):").grid(row=0, column=4, padx=5, pady=5)
        self.edu_year_entry = ttk.Entry(self.edu_frame, width=10)
        self.edu_year_entry.grid(row=0, column=5, padx=5, pady=5)
        
        ttk.Button(self.edu_frame, text="Add Education", command=self.add_education).grid(row=0, column=6, padx=5, pady=5)
        
        self.edu_listbox = tk.Listbox(self.edu_frame, height=4, width=50)
        self.edu_listbox.grid(row=1, column=0, columnspan=7, padx=5, pady=5)
    
    def add_education(self):
        degree = self.degree_entry.get().strip()
        institution = self.institution_entry.get().strip()
        year = self.edu_year_entry.get().strip()
        if not degree or not institution:
            messagebox.showerror("Input Error", "Please fill Degree and Institution fields.")
            return
        if year and not validate_year(year):
            messagebox.showerror("Input Error", "Year must be a 4-digit number between 1900 and current year.")
            return
        record = f"{degree}, {institution}{', ' + year if year else ''}"
        self.education_data.append(record)
        self.edu_listbox.insert(tk.END, record)
        self.degree_entry.delete(0, tk.END)
        self.institution_entry.delete(0, tk.END)
        self.edu_year_entry.delete(0, tk.END)
    
    def create_experience_tab(self, parent):
        self.exp_frame = ttk.Frame(parent, padding=10)
        parent.add(self.exp_frame, text="Experience")
        
        ttk.Label(self.exp_frame, text="Title:").grid(row=0, column=0, padx=5, pady=5)
        self.exp_title_entry = ttk.Entry(self.exp_frame, width=15)
        self.exp_title_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(self.exp_frame, text="Place:").grid(row=0, column=2, padx=5, pady=5)
        self.exp_place_entry = ttk.Entry(self.exp_frame, width=15)
        self.exp_place_entry.grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Label(self.exp_frame, text="Start Date:").grid(row=1, column=0, padx=5, pady=5)
        self.start_date = DateEntry(self.exp_frame, width=12, date_pattern="yyyy-mm-dd")
        self.start_date.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(self.exp_frame, text="End Date:").grid(row=1, column=2, padx=5, pady=5)
        self.end_date = DateEntry(self.exp_frame, width=12, date_pattern="yyyy-mm-dd")
        self.end_date.grid(row=1, column=3, padx=5, pady=5)
        
        self.present_var = tk.BooleanVar()
        ttk.Checkbutton(self.exp_frame, text="Present", variable=self.present_var, command=self.toggle_end_date).grid(row=1, column=4, padx=5, pady=5)
        
        ttk.Button(self.exp_frame, text="Add Experience", command=self.add_experience).grid(row=0, column=4, padx=5, pady=5)
        
        self.exp_listbox = tk.Listbox(self.exp_frame, height=4, width=50)
        self.exp_listbox.grid(row=2, column=0, columnspan=5, padx=5, pady=5)
    
    def toggle_end_date(self):
        if self.present_var.get():
            self.end_date.configure(state="disabled")
        else:
            self.end_date.configure(state="normal")
    
    def add_experience(self):
        title = self.exp_title_entry.get().strip()
        place = self.exp_place_entry.get().strip()
        start = self.start_date.get_date().strftime("%Y-%m-dd")
        end = "Present" if self.present_var.get() else self.end_date.get_date().strftime("%Y-%m-dd")
        if not title or not place:
            messagebox.showerror("Input Error", "Please fill Title and Place fields.")
            return
        record = f"{title}, {place}, {start} - {end}"
        self.experience_data.append(record)
        self.exp_listbox.insert(tk.END, record)
        self.exp_title_entry.delete(0, tk.END)
        self.exp_place_entry.delete(0, tk.END)
    
    def create_publication_tab(self, parent):
        self.pub_frame = ttk.Frame(parent, padding=10)
        parent.add(self.pub_frame, text="Publications")
        
        ttk.Label(self.pub_frame, text="Title:").grid(row=0, column=0, padx=5, pady=5)
        self.pub_title_entry = ttk.Entry(self.pub_frame)
        self.pub_title_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(self.pub_frame, text="Journal:").grid(row=0, column=2, padx=5, pady=5)
        self.pub_journal_entry = ttk.Entry(self.pub_frame)
        self.pub_journal_entry.grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Label(self.pub_frame, text="Year (e.g., 2002):").grid(row=1, column=0, padx=5, pady=5)
        self.pub_year_entry = ttk.Entry(self.pub_frame, width=10)
        self.pub_year_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(self.pub_frame, text="DOI:").grid(row=1, column=2, padx=5, pady=5)
        self.pub_doi_entry = ttk.Entry(self.pub_frame)
        self.pub_doi_entry.grid(row=1, column=3, padx=5, pady=5)
        
        ttk.Label(self.pub_frame, text="Publication Link:").grid(row=2, column=0, padx=5, pady=5)
        self.pub_link_entry = ttk.Entry(self.pub_frame, width=30)
        self.pub_link_entry.grid(row=2, column=1, columnspan=3, padx=5, pady=5)
        
        ttk.Button(self.pub_frame, text="Add Publication", command=self.add_publication).grid(row=0, column=4, rowspan=3, padx=5, pady=5)
        
        self.pub_listbox = tk.Listbox(self.pub_frame, height=4, width=50)
        self.pub_listbox.grid(row=3, column=0, columnspan=5, padx=5, pady=5)
    
    def add_publication(self):
        title = self.pub_title_entry.get().strip()
        journal = self.pub_journal_entry.get().strip()
        year = self.pub_year_entry.get().strip()
        doi = self.pub_doi_entry.get().strip()
        link = self.pub_link_entry.get().strip()
        if not title or not journal or not year or not doi or not link:
            messagebox.showerror("Input Error", "Please fill all Publication fields.")
            return
        if not validate_year(year):
            messagebox.showerror("Input Error", "Year must be a 4-digit number between 1900 and current year.")
            return
        record = f"{title}, {journal}, {year}, DOI: {doi}, Link: {link}"
        self.publication_data.append(record)
        self.pub_listbox.insert(tk.END, record)
        self.pub_title_entry.delete(0, tk.END)
        self.pub_journal_entry.delete(0, tk.END)
        self.pub_year_entry.delete(0, tk.END)
        self.pub_doi_entry.delete(0, tk.END)
        self.pub_link_entry.delete(0, tk.END)
    
    def save_faculty(self):
        salutation = self.salutation_entry.get().strip()
        name = self.name_entry.get().strip()
        dept_name = self.dept_combo.get().strip()
        subfield_name = self.subfield_combo.get().strip()
        faculty_type = self.faculty_type_entry.get().strip()
        contact_no = self.contact_entry.get().strip()
        email = self.email_entry.get().strip()
        gs_link = self.gs_entry.get().strip()
        orcid = self.orcid_entry.get().strip()
        linkedin = self.linkedin_entry.get().strip()
        website = self.website_entry.get().strip()
        objective = self.objective_text.get("1.0", tk.END).strip()
        research_interest = self.research_text.get("1.0", tk.END).strip()
        affiliation = self.affiliation_text.get("1.0", tk.END).strip()
        awards = self.awards_text.get("1.0", tk.END).strip()
        current_status = self.status_text.get("1.0", tk.END).strip()
        
        if not (name and dept_name):
            messagebox.showerror("Input Error", "Please fill required fields (Name, Department).")
            return
        
        if contact_no and not validate_contact(contact_no):
            messagebox.showerror("Input Error", "Contact number must be in format +XX-XXXXXXXXXX (e.g., +91-1234567890).")
            return
        
        if email and not validate_email(email):
            messagebox.showerror("Input Error", "Please enter a valid email address.")
            return
        
        dept_id = self.dept_map.get(dept_name)
        subfield_id = self.subfield_map.get(subfield_name) if subfield_name else None
        
        faculty_id = self.generate_faculty_id(dept_id)
        query = """INSERT INTO faculty 
                   (faculty_id, salutation, name, department_id, subfield_id, type_of_faculty, email, google_scholar_link, orcid, linkedin, website, contact_no, objective, research_interest, professional_affiliation, awards, current_status)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        params = (faculty_id, salutation, name, dept_id, subfield_id, faculty_type, email, gs_link, orcid, linkedin, website, contact_no, objective, research_interest, affiliation, awards, current_status)
        db.execute(query, params)
        
        for edu in self.education_data:
            query = "INSERT INTO education (faculty_id, degree, institution, year) VALUES (%s, %s, %s, %s)"
            parts = edu.split(", ")
            degree = parts[0]
            institution = parts[1]
            year = parts[2] if len(parts) > 2 else None
            db.execute(query, (faculty_id, degree, institution, year))
        
        for exp in self.experience_data:
            query = "INSERT INTO experience (faculty_id, title, place, duration) VALUES (%s, %s, %s, %s)"
            parts = exp.split(", ", 3)
            db.execute(query, (faculty_id, parts[0], parts[1], parts[2]))
        
        for pub in self.publication_data:
            query = "INSERT INTO publications (faculty_id, title, journal, year, doi, publication_link) VALUES (%s, %s, %s, %s, %s, %s)"
            parts = pub.split(", ", 4)
            title = parts[0]
            journal = parts[1]
            year = parts[2]
            doi = parts[3].replace("DOI: ", "")
            link = parts[4].replace("Link: ", "")
            db.execute(query, (faculty_id, title, journal, year, doi, link))
        
        messagebox.showinfo("Success", f"Faculty saved with ID: {faculty_id}")
        self.clear_faculty_entries()
        self.refresh_view_tab()
    
    def clear_faculty_entries(self):
        self.salutation_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.faculty_type_entry.delete(0, tk.END)
        self.contact_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.gs_entry.delete(0, tk.END)
        self.orcid_entry.delete(0, tk.END)
        self.linkedin_entry.delete(0, tk.END)
        self.website_entry.delete(0, tk.END)
        self.objective_text.delete("1.0", tk.END)
        self.research_text.delete("1.0", tk.END)
        self.affiliation_text.delete("1.0", tk.END)
        self.awards_text.delete("1.0", tk.END)
        self.status_text.delete("1.0", tk.END)
        self.edu_listbox.delete(0, tk.END)
        self.exp_listbox.delete(0, tk.END)
        self.pub_listbox.delete(0, tk.END)
        self.education_data.clear()
        self.experience_data.clear()
        self.publication_data.clear()
    
    def create_view_tab(self):
        top_frame = ttk.Frame(self.view_tab, padding=10)
        top_frame.pack(pady=10)
        
        ttk.Label(top_frame, text="Search Faculty (by Name/ID):").pack(side="left", padx=5)
        self.search_entry = ttk.Entry(top_frame)
        self.search_entry.pack(side="left", padx=5)
        self.search_entry.bind("<Return>", lambda event: self.search_faculty())
        ttk.Button(top_frame, text="Search", command=self.search_faculty).pack(side="left", padx=5)
        ttk.Button(top_frame, text="View All", command=self.refresh_view_tab).pack(side="left", padx=5)
        
        tree_frame = ttk.Frame(self.view_tab)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.tree = ttk.Treeview(tree_frame, columns=("ID", "Name", "Department", "Type", "Contact"), show="headings")
        self.tree.pack(side="left", fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        scrollbar.pack(side="bottom", fill="x")
        self.tree.configure(xscrollcommand=scrollbar.set)
        
        self.tree.heading("ID", text="Faculty ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Department", text="Department")
        self.tree.heading("Type", text="Type")
        self.tree.heading("Contact", text="Contact")
        
        self.tree.column("ID", width=200, stretch=True)
        self.tree.column("Name", width=500, stretch=True)
        self.tree.column("Department", width=400, stretch=True)
        self.tree.column("Type", width=200, stretch=True)
        self.tree.column("Contact", width=250, stretch=True)
        
        btn_frame = ttk.Frame(self.view_tab, padding=10)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Update Selected", command=self.update_faculty).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Delete Selected", command=self.delete_faculty).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Generate Resume PDF", command=self.generate_resume).pack(side="left", padx=5)
        
        self.refresh_view_tab()
    
    def refresh_view_tab(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        query = """SELECT f.faculty_id, f.name, d.department_name, f.type_of_faculty, f.contact_no 
                   FROM faculty f 
                   LEFT JOIN departments d ON f.department_id = d.id"""
        rows = db.fetchall(query)
        for row in rows:
            self.tree.insert("", tk.END, values=row)
    
    def search_faculty(self):
        key = self.search_entry.get().strip()
        if not key:
            self.refresh_view_tab()
            return
        query = """SELECT f.faculty_id, f.name, d.department_name, f.type_of_faculty, f.contact_no 
                   FROM faculty f 
                   LEFT JOIN departments d ON f.department_id = d.id 
                   WHERE f.name LIKE %s OR f.faculty_id LIKE %s"""
        rows = db.fetchall(query, (f"%{key}%", f"%{key}%"))
        for row in self.tree.get_children():
            self.tree.delete(row)
        for row in rows:
            self.tree.insert("", tk.END, values=row)
    
    def get_selected_faculty_id(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Selection Error", "No faculty selected!")
            return None
        return self.tree.item(selected[0])["values"][0]
    
    def update_faculty(self):
        faculty_id = self.get_selected_faculty_id()
        if not faculty_id:
            return
        UpdateWindow(faculty_id, self)
    
    def delete_faculty(self):
        faculty_id = self.get_selected_faculty_id()
        if not faculty_id:
            return
        if messagebox.askyesno("Confirm Delete", "Are you sure?"):
            query = "DELETE FROM faculty WHERE faculty_id=%s"
            db.execute(query, (faculty_id,))
            for table in ["education", "experience", "publications"]:
                db.execute(f"DELETE FROM {table} WHERE faculty_id=%s", (faculty_id,))
            messagebox.showinfo("Deleted", "Faculty record deleted!")
            self.refresh_view_tab()
    
    def generate_resume(self):
        faculty_id = self.get_selected_faculty_id()
        if not faculty_id:
            return
        query = """SELECT f.*, d.department_name 
                   FROM faculty f 
                   LEFT JOIN departments d ON f.department_id = d.id 
                   WHERE f.faculty_id=%s"""
        record = db.fetchone(query, (faculty_id,))
        if not record:
            messagebox.showerror("Error", "Faculty not found!")
            return
        col_names = [desc[0] for desc in db.cursor.description]
        data = dict(zip(col_names, record))
        data['department'] = data.pop('department_name', '')
        
        edu_rows = db.fetchall("SELECT degree, institution, year FROM education WHERE faculty_id=%s", (faculty_id,))
        exp_rows = db.fetchall("SELECT title, place, duration FROM experience WHERE faculty_id=%s", (faculty_id,))
        pub_rows = db.fetchall("SELECT title, journal, year, doi, publication_link FROM publications WHERE faculty_id=%s", (faculty_id,))
        
        data['education'] = [f"{e[0]}, {e[1]}{', ' + str(e[2]) if e[2] else ''}" for e in edu_rows]
        data['experience'] = [f"{e[0]}, {e[1]}, {e[2]}" for e in exp_rows]
        data['publications'] = [f"{p[0]}, {p[1]}, {p[2]}, DOI: {p[3]}, Link: {p[4]}" for p in pub_rows]
        
        generate_resume_pdf(data)

# ==============================
# Update Window
# ==============================
class UpdateWindow(tk.Toplevel):
    def __init__(self, faculty_id, parent):
        super().__init__(parent)
        self.faculty_id = faculty_id
        self.parent = parent
        self.title(f"Update Faculty Record - {faculty_id}")
        self.geometry("1200x800")
        self.configure(bg="#fff5e6")
        
        # Fetch Faculty Data
        query = "SELECT * FROM faculty WHERE faculty_id=%s"
        record = db.fetchone(query, (faculty_id,))
        if not record:
            messagebox.showerror("Error", "Faculty not found!")
            self.destroy()
            return
        col_names = [desc[0] for desc in db.cursor.description]
        self.data = dict(zip(col_names, record))
        
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Basic Info Tab
        basic_tab = ttk.Frame(notebook)
        notebook.add(basic_tab, text="Basic Info")
        
        ttk.Label(basic_tab, text="Salutation:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.up_salutation = ttk.Entry(basic_tab)
        self.up_salutation.grid(row=0, column=1, padx=5, pady=5)
        self.up_salutation.insert(0, self.data.get("salutation", ""))
        
        ttk.Label(basic_tab, text="Name:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.up_name = ttk.Entry(basic_tab)
        self.up_name.grid(row=0, column=3, padx=5, pady=5)
        self.up_name.insert(0, self.data.get("name", ""))
        
        ttk.Label(basic_tab, text="Faculty Type:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.up_faculty_type = ttk.Entry(basic_tab)
        self.up_faculty_type.grid(row=1, column=1, padx=5, pady=5)
        self.up_faculty_type.insert(0, self.data.get("type_of_faculty", ""))
        
        ttk.Label(basic_tab, text="Contact No. (e.g., +91-1234567890):").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.up_contact = ttk.Entry(basic_tab)
        self.up_contact.grid(row=1, column=3, padx=5, pady=5)
        self.up_contact.insert(0, self.data.get("contact_no", ""))
        
        ttk.Label(basic_tab, text="Email:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.up_email = ttk.Entry(basic_tab)
        self.up_email.grid(row=2, column=1, padx=5, pady=5)
        self.up_email.insert(0, self.data.get("email", ""))
        
        ttk.Label(basic_tab, text="Google Scholar:").grid(row=2, column=2, padx=5, pady=5, sticky="w")
        self.up_gs = ttk.Entry(basic_tab)
        self.up_gs.grid(row=2, column=3, padx=5, pady=5)
        self.up_gs.insert(0, self.data.get("google_scholar_link", ""))
        
        ttk.Label(basic_tab, text="ORCID:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.up_orcid = ttk.Entry(basic_tab)
        self.up_orcid.grid(row=3, column=1, padx=5, pady=5)
        self.up_orcid.insert(0, self.data.get("orcid", ""))
        
        ttk.Label(basic_tab, text="LinkedIn:").grid(row=3, column=2, padx=5, pady=5, sticky="w")
        self.up_linkedin = ttk.Entry(basic_tab)
        self.up_linkedin.grid(row=3, column=3, padx=5, pady=5)
        self.up_linkedin.insert(0, self.data.get("linkedin", ""))
        
        ttk.Label(basic_tab, text="Website:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.up_website = ttk.Entry(basic_tab)
        self.up_website.grid(row=4, column=1, padx=5, pady=5)
        self.up_website.insert(0, self.data.get("website", ""))
        
        # Additional Info Tab
        add_tab = ttk.Frame(notebook)
        notebook.add(add_tab, text="Additional Info")
        
        ttk.Label(add_tab, text="Objective:").grid(row=0, column=0, padx=5, pady=5, sticky="nw")
        self.up_objective = tk.Text(add_tab, width=50, height=3)
        self.up_objective.grid(row=0, column=1, padx=5, pady=5)
        self.up_objective.insert("1.0", self.data.get("objective", ""))
        
        ttk.Label(add_tab, text="Research Interest:").grid(row=0, column=2, padx=5, pady=5, sticky="nw")
        self.up_research = tk.Text(add_tab, width=50, height=3)
        self.up_research.grid(row=0, column=3, padx=5, pady=5)
        self.up_research.insert("1.0", self.data.get("research_interest", ""))
        
        ttk.Label(add_tab, text="Professional Affiliation:").grid(row=1, column=0, padx=5, pady=5, sticky="nw")
        self.up_affiliation = tk.Text(add_tab, width=50, height=3)
        self.up_affiliation.grid(row=1, column=1, padx=5, pady=5)
        self.up_affiliation.insert("1.0", self.data.get("professional_affiliation", ""))
        
        ttk.Label(add_tab, text="Awards & Honors:").grid(row=1, column=2, padx=5, pady=5, sticky="nw")
        self.up_awards = tk.Text(add_tab, width=50, height=3)
        self.up_awards.grid(row=1, column=3, padx=5, pady=5)
        self.up_awards.insert("1.0", self.data.get("awards", ""))
        
        ttk.Label(add_tab, text="Current Status:").grid(row=2, column=0, padx=5, pady=5, sticky="nw")
        self.up_status = tk.Text(add_tab, width=50, height=3)
        self.up_status.grid(row=2, column=1, padx=5, pady=5)
        self.up_status.insert("1.0", self.data.get("current_status", ""))
        
        # Education Tab
        edu_tab = ttk.Frame(notebook)
        notebook.add(edu_tab, text="Education")
        self.edu_listbox = tk.Listbox(edu_tab, height=10, width=80)
        self.edu_listbox.pack(pady=5)
        self.load_subdetails("education", "SELECT degree, institution, year FROM education WHERE faculty_id=%s", self.edu_listbox)
        ttk.Button(edu_tab, text="Add", command=lambda: self.edit_subdetail("education", "add")).pack(side="left", padx=5)
        ttk.Button(edu_tab, text="Edit", command=lambda: self.edit_subdetail("education", "edit")).pack(side="left", padx=5)
        ttk.Button(edu_tab, text="Delete", command=lambda: self.delete_subdetail("education", self.edu_listbox)).pack(side="left", padx=5)
        
        # Experience Tab
        exp_tab = ttk.Frame(notebook)
        notebook.add(exp_tab, text="Experience")
        self.exp_listbox = tk.Listbox(exp_tab, height=10, width=80)
        self.exp_listbox.pack(pady=5)
        self.load_subdetails("experience", "SELECT title, place, duration FROM experience WHERE faculty_id=%s", self.exp_listbox)
        ttk.Button(exp_tab, text="Add", command=lambda: self.edit_subdetail("experience", "add")).pack(side="left", padx=5)
        ttk.Button(exp_tab, text="Edit", command=lambda: self.edit_subdetail("experience", "edit")).pack(side="left", padx=5)
        ttk.Button(exp_tab, text="Delete", command=lambda: self.delete_subdetail("experience", self.exp_listbox)).pack(side="left", padx=5)
        
        # Publications Tab
        pub_tab = ttk.Frame(notebook)
        notebook.add(pub_tab, text="Publications")
        self.pub_listbox = tk.Listbox(pub_tab, height=10, width=80)
        self.pub_listbox.pack(pady=5)
        self.load_subdetails("publications", "SELECT title, journal, year, doi, publication_link FROM publications WHERE faculty_id=%s", self.pub_listbox)
        ttk.Button(pub_tab, text="Add", command=lambda: self.edit_subdetail("publications", "add")).pack(side="left", padx=5)
        ttk.Button(pub_tab, text="Edit", command=lambda: self.edit_subdetail("publications", "edit")).pack(side="left", padx=5)
        ttk.Button(pub_tab, text="Delete", command=lambda: self.delete_subdetail("publications", self.pub_listbox)).pack(side="left", padx=5)
        
        ttk.Button(self, text="Save Updated Record", command=self.update_record).pack(pady=10)
    
    def load_subdetails(self, table, query, listbox):
        rows = db.fetchall(query, (self.faculty_id,))
        listbox.delete(0, tk.END)
        if table == "education":
            for row in rows:
                listbox.insert(tk.END, f"{row[0]}, {row[1]}{', ' + str(row[2]) if row[2] else ''}")
        elif table == "experience":
            for row in rows:
                listbox.insert(tk.END, f"{row[0]}, {row[1]}, {row[2]}")
        elif table == "publications":
            for row in rows:
                listbox.insert(tk.END, f"{row[0]}, {row[1]}, {row[2]}, DOI: {row[3]}, Link: {row[4]}")
    
    def edit_subdetail(self, table, action):
        selected_item = None
        if action == "edit":
            if table == "education" and not self.edu_listbox.curselection():
                messagebox.showerror("Selection Error", "Please select an education item to edit.")
                return
            if table == "experience" and not self.exp_listbox.curselection():
                messagebox.showerror("Selection Error", "Please select an experience item to edit.")
                return
            if table == "publications" and not self.pub_listbox.curselection():
                messagebox.showerror("Selection Error", "Please select a publication item to edit.")
                return
            if table == "education":
                selected_item = self.edu_listbox.get(self.edu_listbox.curselection())
            elif table == "experience":
                selected_item = self.exp_listbox.get(self.exp_listbox.curselection())
            elif table == "publications":
                selected_item = self.pub_listbox.get(self.pub_listbox.curselection())
        
        dialog = tk.Toplevel(self)
        dialog.title(f"{action.capitalize()} {table.capitalize()}")
        dialog.geometry("600x400")
        dialog.configure(bg="#fff5e6")
        
        if table == "education":
            ttk.Label(dialog, text="Degree:").grid(row=0, column=0, padx=5, pady=5)
            degree = ttk.Entry(dialog)
            degree.grid(row=0, column=1, padx=5, pady=5)
            ttk.Label(dialog, text="Institution:").grid(row=1, column=0, padx=5, pady=5)
            institution = ttk.Entry(dialog)
            institution.grid(row=1, column=1, padx=5, pady=5)
            ttk.Label(dialog, text="Year (e.g., 2002):").grid(row=2, column=0, padx=5, pady=5)
            year = ttk.Entry(dialog)
            year.grid(row=2, column=1, padx=5, pady=5)
            if action == "edit" and selected_item:
                parts = selected_item.split(", ")
                degree.insert(0, parts[0])
                institution.insert(0, parts[1])
                if len(parts) > 2:
                    year.insert(0, parts[2])
            def save():
                if not degree.get().strip() or not institution.get().strip():
                    messagebox.showerror("Input Error", "Please fill Degree and Institution fields.")
                    return
                if year.get().strip() and not validate_year(year.get().strip()):
                    messagebox.showerror("Input Error", "Year must be a 4-digit number between 1900 and current year.")
                    return
                if action == "add":
                    query = "INSERT INTO education (faculty_id, degree, institution, year) VALUES (%s, %s, %s, %s)"
                    db.execute(query, (self.faculty_id, degree.get(), institution.get(), year.get() or None))
                else:
                    old_parts = selected_item.split(", ")
                    query = "UPDATE education SET degree=%s, institution=%s, year=%s WHERE faculty_id=%s AND degree=%s AND institution=%s"
                    db.execute(query, (degree.get(), institution.get(), year.get() or None, self.faculty_id, old_parts[0], old_parts[1]))
                self.load_subdetails("education", "SELECT degree, institution, year FROM education WHERE faculty_id=%s", self.edu_listbox)
                dialog.destroy()
            ttk.Button(dialog, text="Save", command=save).grid(row=3, column=1, pady=10)
        
        elif table == "experience":
            ttk.Label(dialog, text="Title:").grid(row=0, column=0, padx=5, pady=5)
            title = ttk.Entry(dialog)
            title.grid(row=0, column=1, padx=5, pady=5)
            ttk.Label(dialog, text="Place:").grid(row=1, column=0, padx=5, pady=5)
            place = ttk.Entry(dialog)
            place.grid(row=1, column=1, padx=5, pady=5)
            ttk.Label(dialog, text="Duration:").grid(row=2, column=0, padx=5, pady=5)
            duration = ttk.Entry(dialog)
            duration.grid(row=2, column=1, padx=5, pady=5)
            if action == "edit" and selected_item:
                parts = selected_item.split(", ", 2)
                title.insert(0, parts[0])
                place.insert(0, parts[1])
                duration.insert(0, parts[2])
            def save():
                if not title.get().strip() or not place.get().strip():
                    messagebox.showerror("Input Error", "Please fill Title and Place fields.")
                    return
                if action == "add":
                    query = "INSERT INTO experience (faculty_id, title, place, duration) VALUES (%s, %s, %s, %s)"
                    db.execute(query, (self.faculty_id, title.get(), place.get(), duration.get()))
                else:
                    old_parts = selected_item.split(", ", 2)
                    query = "UPDATE experience SET title=%s, place=%s, duration=%s WHERE faculty_id=%s AND title=%s AND place=%s"
                    db.execute(query, (title.get(), place.get(), duration.get(), self.faculty_id, old_parts[0], old_parts[1]))
                self.load_subdetails("experience", "SELECT title, place, duration FROM experience WHERE faculty_id=%s", self.exp_listbox)
                dialog.destroy()
            ttk.Button(dialog, text="Save", command=save).grid(row=3, column=1, pady=10)
        
        elif table == "publications":
            ttk.Label(dialog, text="Title:").grid(row=0, column=0, padx=5, pady=5)
            title = ttk.Entry(dialog)
            title.grid(row=0, column=1, padx=5, pady=5)
            ttk.Label(dialog, text="Journal:").grid(row=1, column=0, padx=5, pady=5)
            journal = ttk.Entry(dialog)
            journal.grid(row=1, column=1, padx=5, pady=5)
            ttk.Label(dialog, text="Year (e.g., 2002):").grid(row=2, column=0, padx=5, pady=5)
            year = ttk.Entry(dialog)
            year.grid(row=2, column=1, padx=5, pady=5)
            ttk.Label(dialog, text="DOI:").grid(row=3, column=0, padx=5, pady=5)
            doi = ttk.Entry(dialog)
            doi.grid(row=3, column=1, padx=5, pady=5)
            ttk.Label(dialog, text="Publication Link:").grid(row=4, column=0, padx=5, pady=5)
            link = ttk.Entry(dialog)
            link.grid(row=4, column=1, padx=5, pady=5)
            if action == "edit" and selected_item:
                parts = selected_item.split(", ", 4)
                title.insert(0, parts[0])
                journal.insert(0, parts[1])
                year.insert(0, parts[2])
                doi.insert(0, parts[3].replace("DOI: ", ""))
                link.insert(0, parts[4].replace("Link: ", ""))
            def save():
                if not title.get().strip() or not journal.get().strip() or not year.get().strip() or not doi.get().strip() or not link.get().strip():
                    messagebox.showerror("Input Error", "Please fill all Publication fields.")
                    return
                if not validate_year(year.get().strip()):
                    messagebox.showerror("Input Error", "Year must be a 4-digit number between 1900 and current year.")
                    return
                if action == "add":
                    query = "INSERT INTO publications (faculty_id, title, journal, year, doi, publication_link) VALUES (%s, %s, %s, %s, %s, %s)"
                    db.execute(query, (self.faculty_id, title.get(), journal.get(), year.get(), doi.get(), link.get()))
                else:
                    old_parts = selected_item.split(", ", 4)
                    query = "UPDATE publications SET title=%s, journal=%s, year=%s, doi=%s, publication_link=%s WHERE faculty_id=%s AND title=%s AND journal=%s"
                    db.execute(query, (title.get(), journal.get(), year.get(), doi.get(), link.get(), self.faculty_id, old_parts[0], old_parts[1]))
                self.load_subdetails("publications", "SELECT title, journal, year, doi, publication_link FROM publications WHERE faculty_id=%s", self.pub_listbox)
                dialog.destroy()
            ttk.Button(dialog, text="Save", command=save).grid(row=5, column=1, pady=10)
    
    def delete_subdetail(self, table, listbox):
        if not listbox.curselection():
            messagebox.showerror("Selection Error", "Please select an item to delete.")
            return
        selected = listbox.get(listbox.curselection())
        if table == "education":
            parts = selected.split(", ")
            query = "DELETE FROM education WHERE faculty_id=%s AND degree=%s AND institution=%s"
            db.execute(query, (self.faculty_id, parts[0], parts[1]))
            self.load_subdetails("education", "SELECT degree, institution, year FROM education WHERE faculty_id=%s", listbox)
        elif table == "experience":
            parts = selected.split(", ", 2)
            query = "DELETE FROM experience WHERE faculty_id=%s AND title=%s AND place=%s"
            db.execute(query, (self.faculty_id, parts[0], parts[1]))
            self.load_subdetails("experience", "SELECT title, place, duration FROM experience WHERE faculty_id=%s", listbox)
        elif table == "publications":
            parts = selected.split(", ", 4)
            query = "DELETE FROM publications WHERE faculty_id=%s AND title=%s AND journal=%s"
            db.execute(query, (self.faculty_id, parts[0], parts[1]))
            self.load_subdetails("publications", "SELECT title, journal, year, doi, publication_link FROM publications WHERE faculty_id=%s", listbox)
    
    def update_record(self):
        salutation = self.up_salutation.get().strip()
        name = self.up_name.get().strip()
        faculty_type = self.up_faculty_type.get().strip()
        contact_no = self.up_contact.get().strip()
        email = self.up_email.get().strip()
        gs_link = self.up_gs.get().strip()
        orcid = self.up_orcid.get().strip()
        linkedin = self.up_linkedin.get().strip()
        website = self.up_website.get().strip()
        objective = self.up_objective.get("1.0", tk.END).strip()
        research_interest = self.up_research.get("1.0", tk.END).strip()
        affiliation = self.up_affiliation.get("1.0", tk.END).strip()
        awards = self.up_awards.get("1.0", tk.END).strip()
        current_status = self.up_status.get("1.0", tk.END).strip()
        
        if contact_no and not validate_contact(contact_no):
            messagebox.showerror("Input Error", "Contact number must be in format +XX-XXXXXXXXXX (e.g., +91-1234567890).")
            return
        
        if email and not validate_email(email):
            messagebox.showerror("Input Error", "Please enter a valid email address.")
            return
        
        query = """UPDATE faculty SET salutation=%s, name=%s, type_of_faculty=%s, contact_no=%s, email=%s, google_scholar_link=%s, orcid=%s, linkedin=%s, website=%s, objective=%s, research_interest=%s, professional_affiliation=%s, awards=%s, current_status=%s 
                   WHERE faculty_id=%s"""
        params = (
            salutation, name, faculty_type, contact_no,
            email, gs_link, orcid, linkedin, website,
            objective, research_interest, affiliation, awards,
            current_status, self.faculty_id
        )
        db.execute(query, params)
        messagebox.showinfo("Success", "Faculty record updated!")
        self.parent.refresh_view_tab()
        self.destroy()

if __name__ == "__main__":
    app = FacultyManagementApp()
    app.mainloop()
    db.close()
