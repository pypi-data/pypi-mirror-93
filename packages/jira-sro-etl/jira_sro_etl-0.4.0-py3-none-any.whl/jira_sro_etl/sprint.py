import logging
import datetime
logging.basicConfig(level=logging.INFO)

from jiraX import factories as factory
from pprint import pprint
from .base_entity import BaseEntity

from sro_db.application import factories
from sro_db.model import factories as factories_model

""" Sprint (Time box) """
class sprint(BaseEntity):
	"""
	Class responsible for retrieve sprints from jira
	"""
	def do (self,data):
		"""Retrive all sprints from all projects

		Args:
			data (dict): With user, key and server to connect with jira

		Returns:
			dict: Key is the project's key and value is a list with all sprints of this project
		"""
		try:
			logging.info("Sprint")

			self.config(data)

			project_apl = factory.ProjectFactory(user=self.user,apikey=self.key,server=self.url)
			board_apl = factory.BoardFactory(user=self.user,apikey=self.key,server=self.url)
			sprint_apl = factory.SprintFactory(user=self.user,apikey=self.key,server=self.url)
			
			# Associa tasks do banco com o sprint e sprint_backlog
			# Associa user_stories do banco com o sprint_backlog
			issue_apl = factory.IssueFactory(user=self.user,apikey=self.key,server=self.url)
			intended_task_application = factories.ScrumIntentedDevelopmentTaskFactory()
			performed_task_application = factories.ScrumPerformedDevelopmentTaskFactory()
			atomic_user_story_application = factories.AtomicUserStoryFactory()

			sprints = {}
			projects = project_apl.find_all()
			for project in projects:
				boards = board_apl.find_by_project(project.key)
				if(boards != None):
					sprints[project.key] = []
					for board in boards:
						try:
							sprints[project.key] += sprint_apl.find_by_board(board.id)
						except Exception as e:
							pprint("O quadro não aceita sprints")
			# pprint(sprints)

			sprint_application = factories.SprintFactory()
			scrum_process_application = factories.ScrumProcessFactory()
			sprint_backlog_application = factories.SprintBacklogFactory()
			
			for project in projects:
				for sprint_ in sprints[project.key]:
					if sprint_application.retrive_by_external_uuid(sprint_.id):
						continue
					# Sprint
					sprint = factories_model.SprintFactory()
					sprint.organization = self.organization
					sprint.startDate = self.date_formater(getattr(sprint_,'startDate', None))
					sprint.endDate = self.date_formater(getattr(sprint_,'endDate', None))
					sprint.name = sprint_.name
					scrum_process = scrum_process_application.retrive_by_external_uuid(project.id)
					if(scrum_process == None): #de algume forma ele tava recuperando um projeto vazio, como se o project n estivesse no banco
						continue #então tal sprint n é salvo no banco
					else:
						sprint.scrum_process_id = scrum_process.id

					issues = issue_apl.find_by_sprint(sprint_.id)
					scrum_development_tasks = []
					atomic_user_stories = []
					for issue in issues:
						# pprint(issue.__dict__)
						if issue.raw['fields']['issuetype']['name'] == 'Sub-task':
							intended_task = intended_task_application.retrive_by_external_uuid(issue.id)
							if intended_task != None:
								scrum_development_tasks.append(intended_task)
							performed_task = performed_task_application.retrive_by_external_uuid(issue.id)
							if performed_task != None:
								scrum_development_tasks.append(performed_task)
						# pprint(scrum_development_tasks)
						if issue.raw['fields']['issuetype']['name'] == 'Story':
							atomic_story = atomic_user_story_application.retrive_by_external_uuid(issue.id)
							if atomic_story != None:
								atomic_user_stories.append(atomic_story)
						# pprint(atomic_user_stories)
						sprint.scrum_development_tasks = scrum_development_tasks
					sprint_application.create(sprint)
					self.create_application_reference('sprint', sprint, sprint_.id, sprint_.self)

					# Sprint Backlog
					sprint_backlog = factories_model.SprintBacklogFactory()
					sprint_backlog.name = sprint_.name
					sprint_backlog.sprint = sprint.id

					sprint_backlog.scrum_development_tasks = scrum_development_tasks
					sprint_backlog.atomic_user_stories = atomic_user_stories

					sprint_backlog_application.create(sprint_backlog)
					self.create_application_reference('sprint', sprint_backlog, sprint_.id, sprint_.self)


			logging.info("successfuly done (Sprint)")
			return sprints
			
		except e:
			pass


