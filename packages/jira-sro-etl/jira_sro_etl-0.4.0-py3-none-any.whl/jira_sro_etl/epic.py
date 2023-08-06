import logging
logging.basicConfig(level=logging.INFO)

from jiraX import factories as factory
from pprint import pprint
from .base_entity import BaseEntity

from sro_db.application import factories
from sro_db.model import factories as factories_model

""" An epic """
class epic(BaseEntity):
	"""
	Class responsible for retrieve epics from jira lala
	"""
	def do(self,data):
		"""Retrieve all epics from jira

		Args:
			data (dict): With user, key and server to connect with jira

		Returns:
			dict: Key is the project's key and value is a list with all epics of this project
		"""
		try:
			logging.info("Epic")

			self.config(data)

			project_apl = factory.ProjectFactory(user=self.user,apikey=self.key,server=self.url)
			issue_apl = factory.IssueFactory(user=self.user,apikey=self.key,server=self.url)

			projects = project_apl.find_all()
			epics = {}
			for project in projects:
				epics[project.id] = issue_apl.find_epic_by_project(project.key)
			# pprint(epics)

			projects_names = {str(project.id): project.name for project in projects}

			epic_application = factories.EpicFactory()
			product_backlog_application = factories.ProductBacklogFactory()
			team_member_application = factories.DeveloperFactory()
			
			for project_id, epic_list in epics.items():
				for epic_ in epic_list:
					if epic_application.retrive_by_external_uuid(epic_.id):
						continue
					epic = factories_model.EpicFactory()
					epic.name = epic_.raw['fields']['summary']
					epic.description = epic_.raw['fields'].get('description')
					epic.product_backlog = product_backlog_application.retrive_by_external_uuid(project_id).id
					try:
						epic.created_by = team_member_application.retrive_by_external_id_and_project_name(epic_.raw['fields']['creator']['accountId'], projects_names[project_id])
					except Exception as e:
						epic.created_by = None
					try:
						epic.activated_by = team_member_application.retrive_by_external_id_and_project_name(epic_.raw['fields']['reporter']['accountId'], projects_names[project_id])
					except Exception as e:
						epic.activated_by = None
					try:
						epic.closed_by = team_member_application.retrive_by_external_id_and_project_name(epic_.raw['fields']['assignee']['accountId'], projects_names[project_id])
					except Exception as e:
						epic.closed_by = None
					# epic.story_points = TODO
					# epic.created_date = TODO
					epic.activated_date = self.date_formater(None if type(next(iter(epic_.raw['fields'].get('customfield_10018') or []), None)) != dict else epic_.raw['fields']['customfield_10018'][0]['startDate'])
					epic.closed_date = self.date_formater(epic_.raw['fields'].get('duedate'))
					epic.resolved_date = self.date_formater(epic_.raw['fields'].get('resolutiondate'))
					epic_application.create(epic)
					self.create_application_reference('issue', epic, epic_.id, epic_.self)

			logging.info("successfuly done (Epic)")
			return epics

		except Exception as e:
			pprint('Error')
			pprint(e)
