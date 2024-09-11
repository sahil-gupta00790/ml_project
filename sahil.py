import pandas as pd
import random

courses = pd.DataFrame({
    'course_id': [f'C{i:03d}' for i in range(1, 21)],
    'course_name': [
        'Introduction to AI', 'Web Development', 'Data Structures', 'Machine Learning', 'Computer Networks',
        'Database Systems', 'Software Engineering', 'Computer Graphics', 'Cybersecurity', 'Cloud Computing',
        'Mobile App Development', 'Big Data Analytics', 'Natural Language Processing', 'Computer Vision',
        'Robotics', 'Quantum Computing', 'Blockchain Technology', 'Internet of Things', 'Game Development',
        'Augmented Reality'
    ],
    'description': [
        'Basic concepts of artificial intelligence and machine learning',
        'Building responsive websites using HTML, CSS, and JavaScript',
        'Fundamental data structures and algorithms',
        'Advanced machine learning techniques and applications',
        'Principles of computer networking and protocols',
        'Design and implementation of database management systems',
        'Principles and practices of software development',
        'Techniques for creating and manipulating digital images',
        'Fundamentals of information security and network protection',
        'Concepts and technologies for cloud-based computing',
        'Developing applications for mobile devices',
        'Processing and analyzing large-scale data sets',
        'Computational techniques for analyzing human language',
        'Algorithms for understanding and processing visual information',
        'Design and control of autonomous mechanical systems',
        'Principles of quantum computation and information',
        'Decentralized and distributed ledger technologies',
        'Connecting and controlling devices through the internet',
        'Principles and techniques of video game creation',
        'Technologies for overlaying digital information on the real world'
    ],
    'tags': [
        'AI, programming, algorithms',
        'web, programming, design',
        'algorithms, programming',
        'AI, data science, programming',
        'networking, protocols, infrastructure',
        'data, SQL, information systems',
        'development, project management, testing',
        'visualization, algorithms, multimedia',
        'security, cryptography, networks',
        'distributed systems, virtualization, scalability',
        'iOS, Android, cross-platform development',
        'Hadoop, Spark, data processing',
        'text analysis, AI, linguistics',
        'image processing, AI, pattern recognition',
        'control systems, AI, mechatronics',
        'physics, computation, cryptography',
        'cryptocurrencies, distributed systems, cryptography',
        'embedded systems, networking, sensors',
        'Unity, graphics, interactive media',
        'VR, 3D modeling, interaction design'
    ]
})

num_users = 1000
users = []
interests = [
    'AI', 'web development', 'algorithms', 'data science', 'networking',
    'databases', 'software engineering', 'graphics', 'cybersecurity', 'cloud computing',
    'mobile development', 'big data', 'natural language processing', 'computer vision',
    'robotics', 'quantum computing', 'blockchain', 'IoT', 'game development', 'augmented reality'
]

for i in range(num_users):
    user_id = f'U{i+1:03d}'
    num_interests = random.randint(2, 5)
    user_interests = random.sample(interests, num_interests)
    
    num_past_courses = random.randint(2, 5)
    past_courses = random.sample(courses['course_id'].tolist()[:10], num_past_courses)
    
    num_future_courses = random.randint(2, 5)
    future_courses = random.sample([c for c in courses['course_id'].tolist()[10:] if c not in past_courses], num_future_courses)
    
    users.append({
        'user_id': user_id,
        'interests': ','.join(user_interests),
        'past_courses': ','.join(past_courses),
        'future_courses': ','.join(future_courses)
    })

user_df = pd.DataFrame(users)
 
courses.to_csv('course_data.csv', index=False)
user_df.to_csv('user_data_extended.csv', index=False)

print("Datasets generated and saved as 'course_data.csv' and 'user_data_extended.csv'")
print("\nSample user data:")
print(user_df.head())
print("\nSample course data:")
print(courses.head())