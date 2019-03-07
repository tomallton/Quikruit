import random
from applicants.models import SkillHobby
from .models import TestQuestion

def generate_questions():
	while True:
		skill = random.choice(SkillHobby.objects.exclude(kind=SkillHobby.HOBBY))
		question_type = random.randint(0,1)

		all_choices = 'ABCD'

		answer = None
		if question_type == TestQuestion.SINGLE_SELECT:
			answer = random.choice(all_choices)
		else:
			answer = ''.join(c for c in all_choices if random.random() > 0.5)

		question_text = '''## Testing {}: \n### Correct answer: {}'''.format(skill, answer)

		print('{} | {} | {} | {}'.format(skill, question_type, question_text, answer))

		q = TestQuestion()
		q.question_type = question_type
		q.tested_skill = skill
		q.question = question_text
		q.correct_answer = answer
		q.save()