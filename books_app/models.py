from django.db import models
import re
import bcrypt


class UserManager(models.Manager):
    def register_validator(self, post_data):
        errors = {}
        
        if len(post_data['first_name']) < 2:
            errors['first_name'] = 'First name should be at least two characters'
        
        if len(post_data['last_name']) < 2:
            errors['last_name'] = 'Last name should be at least two characters'
        
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(post_data['email']):    # test whether a field matches the pattern            
            errors['email'] = "Invalid email/password!"
        
        if len(post_data['password']) < 8:
            errors['password'] = 'Password should be at least eight characters'
        
        if (post_data['password'] != post_data['confirm_password']):
            errors['confirm_password'] = "Password confirm didn't match"

        user_list = User.objects.filter(email=post_data['email'])
        if len(user_list) > 0:
            errors['email_password'] = "Email/password is incorrect. Please try again."

        return errors

    def login_validator(self, post_data):
        errors = {}
        user_list = User.objects.filter(email=post_data['email'])
        if len(user_list) == 0:
            errors['email_password'] = "Email/password is incorrect. Please try again."
        else:
            if bcrypt.checkpw(
                post_data['password'].encode(),
                user_list[0].password.encode()
            ) != True:
                errors['email_password'] = "Email/password is incorrect. Please try again."
        return errors

    def book_validator(self, post_data):
        errors = {}
        if len(post_data['title']) < 1:
            errors['title'] = 'Title is required'
        
        if len(post_data['description']) < 5:
            errors['description'] = 'Description should be at least five characters'
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.EmailField(max_length=45)
    password = models.CharField(max_length=255)
    objects = UserManager()
    # books_uploaded_one
    # favorite_books_many
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Book(models.Model):
    title = models.CharField(max_length=255)
    desc = models.TextField()
    uploaded_by_id_one = models.ForeignKey(User, related_name="books_uploaded_one", on_delete=models.CASCADE)
    favorites_by_many = models.ManyToManyField(User, related_name="favorite_books_many")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
