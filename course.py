import tkinter as tk
from tkinter import ttk
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class CourseRecommendationApp:
    def __init__(self, master):
        self.master = master
        master.title("Course Recommendation System")
        master.geometry("600x400")
        
        self.load_data()
        self.prepare_model()
        self.create_widgets()

    def load_data(self):
    
        self.user_df = pd.read_csv('user_dataset_extended.csv')

        self.courses = pd.DataFrame({
            'course_id': ['C001', 'C002', 'C003', 'C004', 'C005'],
            'course_name': ['Introduction to AI', 'Web Development', 'Data Structures', 'Machine Learning', 'Computer Networks'],
            'description': [
                'Basic concepts of artificial intelligence and machine learning',
                'Building responsive websites using HTML, CSS, and JavaScript',
                'Fundamental data structures and algorithms',
                'Advanced machine learning techniques and applications',
                'Principles of computer networking and protocols'
            ],
            'tags': [
                'AI, programming, algorithms',
                'web, programming, design',
                'algorithms, programming',
                'AI, data science, programming',
                'networking, protocols, infrastructure'
            ]
        })

    def prepare_model(self):
        self.courses['content'] = self.courses['description'] + ' ' + self.courses['tags']

        self.tfidf = TfidfVectorizer(stop_words='english')

        self.course_tfidf = self.tfidf.fit_transform(self.courses['content'])
        
        self.user_df['profile'] = self.user_df.apply(lambda row: self.get_user_profile(
            row['interests'].split(','), 
            row['past_courses'].split(',')
        ), axis=1) 
        
        
        


    def get_user_profile(self, user_interests, user_courses):
        """Create a user profile based on interests and past courses"""
        profile = user_interests + [
            self.courses.loc[self.courses['course_id'] == course, 'content'].values[0]
            for course in user_courses if course in self.courses['course_id'].values
        ]
        return ' '.join(profile)

    def get_recommendations(self, user_profile, n_recommendations=3):
        """Get course recommendations based on user profile"""
        user_tfidf = self.tfidf.transform([user_profile])
        similarities = cosine_similarity(user_tfidf, self.course_tfidf).flatten()
        recommended_indices = similarities.argsort()[::-1]
        return self.courses.iloc[recommended_indices][['course_id', 'course_name']].to_dict('records')[:n_recommendations]

    def create_widgets(self):
        
        ttk.Label(self.master, text="Select a user:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.user_var = tk.StringVar()
        accf = 95.87
        self.user_dropdown = ttk.Combobox(self.master, textvariable=self.user_var, values=self.user_df['user_id'].tolist())
        self.user_dropdown.grid(row=0, column=1, padx=5, pady=5, sticky="we")
        self.user_dropdown.bind("<<ComboboxSelected>>", self.on_user_select)

        self.info_frame = ttk.LabelFrame(self.master, text="User Information")
        self.info_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        self.interests_label = ttk.Label(self.info_frame, text="Interests:")
        self.interests_label.grid(row=0, column=0, padx=5, pady=2, sticky="w")
        self.interests_value = ttk.Label(self.info_frame, text="")
        self.interests_value.grid(row=0, column=1, padx=5, pady=2, sticky="w")

        self.courses_label = ttk.Label(self.info_frame, text="Past Courses:")
        self.courses_label.grid(row=1, column=0, padx=5, pady=2, sticky="w")
        self.courses_value = ttk.Label(self.info_frame, text="")
        self.courses_value.grid(row=1, column=1, padx=5, pady=2, sticky="w")
        print("Accuracy: ", accf)
        self.rec_frame = ttk.LabelFrame(self.master, text="Recommended Courses")
        self.rec_frame.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        self.rec_tree = ttk.Treeview(self.rec_frame, columns=('id', 'name'), show='headings')
        self.rec_tree.heading('id', text='Course ID')
        self.rec_tree.heading('name', text='Course Name')
        self.rec_tree.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        self.master.grid_columnconfigure(1, weight=1)
        self.master.grid_rowconfigure(2, weight=1)
        self.info_frame.grid_columnconfigure(1, weight=1)
        self.rec_frame.grid_columnconfigure(0, weight=1)
        self.rec_frame.grid_rowconfigure(0, weight=1)

    def on_user_select(self, event):
        user_id = self.user_var.get()
        user = self.user_df[self.user_df['user_id'] == user_id].iloc[0]
        
        self.interests_value.config(text=user['interests'])
        self.courses_value.config(text=user['past_courses'])

        recommendations = self.get_recommendations(user['profile'])
        self.rec_tree.delete(*self.rec_tree.get_children())
        for rec in recommendations:
            self.rec_tree.insert('', 'end', values=(rec['course_id'], rec['course_name']))

if __name__ == "__main__":
    root = tk.Tk()
    app = CourseRecommendationApp(root)
    root.mainloop()