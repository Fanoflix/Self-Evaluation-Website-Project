from flask import Flask

class Tutor():
    def __init__(self, tutor_id, tutor_name, tutor_email, rating, no_reviews):
        self.tutor_id = tutor_id
        self.tutor_name = tutor_name
        self.tutor_email = tutor_email
        self.rating = rating
        self.no_reviews = no_reviews

    def __repr__(self):
        print("---------------------------------------------------------")
        print(f"ID: {self.tutor_id} Name: {self.tutor_name}")
        print(f"Email: {self.tutor_email} Rating: {self.rating} Reviews: {self.no_reviews}")
        return "---------------------------------------------------------"
