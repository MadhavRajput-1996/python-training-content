from django.core.management.base import BaseCommand
from faker import Faker
from todos.models import Todo
from django.contrib.auth.models import User
from random import randint

class Command(BaseCommand):
    help = 'Populates the Todo database with dummy data'

    def handle(self, *args, **kwargs):
        fake = Faker()
        users = User.objects.all()
        print('---users',users)

        for _ in range(20):  # Adjust the number of todos you want to create
            title = fake.sentence(nb_words=3, variable_nb_words=True, ext_word_list=None)
            description = fake.text(max_nb_chars=200, ext_word_list=None)
            completed = fake.boolean(chance_of_getting_true=50)
            print('---title',title)

            # Select a random user for the todo
            user = users[randint(0, len(users) - 1)]

            # Create the Todo object and save it
            todo = Todo.objects.create(
                user=user,
                title=title,
                description=description,
                completed=completed
            )

            self.stdout.write(self.style.SUCCESS(f'Successfully created Todo "{todo.title}"'))
