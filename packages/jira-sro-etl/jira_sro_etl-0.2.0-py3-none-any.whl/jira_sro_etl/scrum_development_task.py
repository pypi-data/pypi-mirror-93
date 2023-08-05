import logging
logging.basicConfig(level=logging.INFO)

from jiraX import factories as factory
from pprint import pprint
from .base_entity import BaseEntity

from sro_db.application import factories
from sro_db.model import factories as factories_model

""" Scrum performed development task """
class scrum_development_task(BaseEntity):
	"""
	Class responsible for retrieve tasks from jira and save them on database
	"""

	def __create_scrum_development_task(self, team_member_application, sprint_application, scrum_development_task, jira_task, project_name):
		"""Set scrum_development_task attributes

		Args:
			team_member_application (obj): 
			sprint_application (obj): 
			scrum_development_task (obj): 
			jira_task (dict):
		"""
		# Campos de toda Entity:
		# Name
		scrum_development_task.name = jira_task.raw['fields']['summary']
		# Description
		scrum_development_task.description = jira_task.raw['fields'].get('description')

		# Campos de toda ScrumDevelopmentTask:
		# Created Date
		scrum_development_task.created_date = self.date_formater(jira_task.raw['fields']['created'])
		# Created By
		try:
			scrum_development_task.created_by = team_member_application.retrive_by_external_id_and_project_name(jira_task.raw['fields']['creator']['accountId'], project_name).id
		except Exception as e:
			scrum_development_task.created_by = None
		# Assigned By
		try:
			team_member = team_member_application.retrive_by_external_id_and_project_name(jira_task.raw['fields']['assignee']['accountId'], project_name)
			if team_member == None:
				raise Exception("Member do not exists in database")
			else:
				scrum_development_task.assigned_by = [team_member]
		except Exception as e:
			scrum_development_task.assigned_by = []
		# Story Points [Não encontrei no objeto retornado pela API]
		scrum_development_task.story_points = None
		# Type [Preenchido automaticamente]
		# Sprints (Não é preenchido aqui)
		# Sprint Backlog (Não é preenchido aqui)
		# Atomic User Story (UUID da user story pai)
		try:
			atomic_user_story_application = factories.AtomicUserStoryFactory()
			scrum_development_task.atomic_user_story = atomic_user_story_application.retrive_by_external_uuid(jira_task.raw['fields']['parent']['id']).id
		except Exception as e:
			scrum_development_task.atomic_user_story = None


	def do(self,data):
		"""Retrieve all tasks from the projects and save them on db as 
		Scrum performed development task

		Args:
			data (dict): With user, key and server to connect with jira

		Returns:
			dict: Key is the project's key and value is a list with all tasks of this project
		"""
		try:
			logging.info("Scrum Development Task")

			self.config(data)

			project_apl = factory.ProjectFactory(user=self.user,apikey=self.key,server=self.url)
			issue_apl = factory.IssueFactory(user=self.user,apikey=self.key,server=self.url)
			
			projects = project_apl.find_all()
			tasks = {project.key: issue_apl.find_sub_task_by_project(project.key) for project in projects}
			
			intended_task_application = factories.ScrumIntentedDevelopmentTaskFactory()
			performed_task_application = factories.ScrumPerformedDevelopmentTaskFactory()
			team_member_application = factories.TeamMemberFactory()
			sprint_application = factories.SprintFactory()
			priority_application = factories.PriorityFactory()
			priority_dict = {'1': 'high', '2': 'high', '3': 'medium', '4': 'normal', '5': 'normal'}
			
			for project in projects:
				for task_ in tasks[project.key]:
					# Caso não seja performed, procura se já existe no banco
					if intended_task_application.retrive_by_external_uuid(task_.id):
						pass
					else:
						# Caso não encontre uma no banco, cria.
						intended_development_task = factories_model.ScrumIntentedDevelopmentTaskFactory()
						self.__create_scrum_development_task(team_member_application, sprint_application, intended_development_task, task_, project.name)

						# Campos de toda ScrumIntentedDevelopmentTask:
						# Type Activity
						intended_development_task.type_activity = None
						# Priority
						try:
							intended_development_task.priority = priority_application.retrive_by_name(priority_dict[task_.raw['fields']['priority']['id']]).id
						except Exception as e:
							intended_development_task.priority = None
						# Risk
						intended_development_task.risk = None

						intended_task_application.create(intended_development_task)
						self.create_application_reference('issue', intended_development_task, task_.id, task_.self)


					# Verifica se a tarefa já foi iniciada
					if (task_.raw['fields']['status']['statusCategory']['id'] == 3 # Itens concluídos
					or task_.raw['fields']['status']['statusCategory']['id'] == 4): # Em andamento
						# Verifica se já existe uma no banco.
						if performed_task_application.retrive_by_external_uuid(task_.id):
							continue
						# Caso não encontre, cria.
						performed_development_task = factories_model.ScrumPerformedDevelopmentTaskFactory()
						self.__create_scrum_development_task(team_member_application, sprint_application, performed_development_task, task_, project.name)

						# Campos de toda ScrumPerformedDevelopmentTask:
						# Closed Date
						performed_development_task.closed_date = self.date_formater(task_.raw['fields'].get('duedate'))
						# Activated Date
						performed_development_task.activated_date = self.date_formater(None if type(next(iter(task_.raw['fields'].get('customfield_10018') or []), None)) != dict else task_.raw['fields']['customfield_10018'][0]['startDate'])
						#Resolved Date
						performed_development_task.resolved_date = self.date_formater(task_.raw['fields'].get('resolutiondate'))
						# Activated By
						try:
							performed_development_task.activated_by = team_member_application.retrive_by_external_id_and_project_name(task_.raw['fields']['reporter']['accountId'], project.name).id
						except Exception as e:
							performed_development_task.activated_by = None
						# Closed By
						try:
							performed_development_task.closed_by = team_member_application.retrive_by_external_id_and_project_name(task_.raw['fields']['assignee']['accountId'], project.name).id
						except Exception as e:
							performed_development_task.closed_by = None
						# Resolved By 
						# Falta validar se reporter é mesmo o que queremos!!!
						try:
							performed_development_task.resolved_by = team_member_application.retrive_by_external_id_and_project_name(task_.raw['fields']['reporter']['accountId'], project.name).id
						except Exception as e:
							performed_development_task.resolved_by = None
						# Caused By
						try:
							performed_development_task.caused_by = intended_task_application.retrive_by_external_uuid(task_.id).id
						except Exception as e:
							performed_development_task.caused_by = None

						performed_task_application.create(performed_development_task)
						self.create_application_reference('issue', performed_development_task, task_.id, task_.self)

			logging.info("successfuly done (Scrum Development Task)")
			return tasks
		
		except Exception as e:
			logging.info(e)

	
