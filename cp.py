import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class CourseRecommendationSystem:
    def __init__(self):
        self.load_data()
        self.prepare_model()

    def load_data(self):
        # Load user data
        self.user_df = pd.read_csv('user_dataset_extended.csv')

        # Load course data
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
        # Combine description and tags into a single field for each course
        self.courses['content'] = self.courses['description'] + ' ' + self.courses['tags']

        # Use TF-IDF to convert text data into numeric form
        self.tfidf = TfidfVectorizer(stop_words='english')
        self.course_tfidf = self.tfidf.fit_transform(self.courses['content'])

        # Create a user profile based on interests and past courses
        self.user_df['profile'] = self.user_df.apply(lambda row: self.get_user_profile(
            row['interests'].split(','), 
            row['past_courses'].split(',')
        ), axis=1)

    def get_user_profile(self, user_interests, user_courses):
        """Create a user profile based on interests and past courses."""
        profile = user_interests + [
            self.courses.loc[self.courses['course_id'] == course, 'content'].values[0]
            for course in user_courses if course in self.courses['course_id'].values
        ]
        return ' '.join(profile)

    def get_recommendations(self, user_profile, n_recommendations=3):
        """Get course recommendations based on user profile."""
        user_tfidf = self.tfidf.transform([user_profile])
        similarities = cosine_similarity(user_tfidf, self.course_tfidf).flatten()
        recommended_indices = similarities.argsort()[::-1]
        return self.courses.iloc[recommended_indices][['course_id', 'course_name']].to_dict('records')[:n_recommendations]

    def calculate_accuracy(self):
        """Calculate accuracy based on how well recommendations match user's past courses."""
        total_users = len(self.user_df)
        correct_predictions = 0

        for _, user in self.user_df.iterrows():
            # Get user's past courses to compare against recommendations
            past_courses = user['past_courses'].split(',')

            # Get recommendations for the user
            recommendations = self.get_recommendations(user['profile'])

            # Check if any of the recommended courses match the user's past courses
            recommended_course_ids = [rec['course_id'] for rec in recommendations]
            for course in past_courses:
                if course in recommended_course_ids:
                    correct_predictions += 1
                    break  # Only count one correct match per user

        # Accuracy = (correct predictions / total users) * 100
        accuracy = (correct_predictions / total_users) * 100
        return accuracy

if __name__ == "__main__":
    # Instantiate the system
    app = CourseRecommendationSystem()

    # Calculate and print the accuracy
    accuracy = app.calculate_accuracy()
    print(f"Accuracy: {accuracy:.2f}%")
