import logging
logging.basicConfig(level=logging.INFO)

from jiraX import factories as factory
from pprint import pprint
from .base_entity import BaseEntity

from sro_db.application import factories
from sro_db.model import factories as factories_model

""" User story """
class user_story(BaseEntity):
	"""
	Class responsible for retrieve user storys from jira
	"""

	def resolve_start_date(self,arr):
		if arr == None:
			return None
		for d in arr:
			if 'startDate' in d:
				return d['startDate']
		return None


	def do(self,data):
		"""Retrieve user storys from all projects

		Args:
			data (dict): With user, key and server to connect with jira

		Returns:
			dict: Key is the project's key and value is a list with all user storys of this project
		"""
		try:
			logging.info("User Story")

			self.config(data)

			project_apl = factory.ProjectFactory(user=self.user,apikey=self.key,server=self.url)
			issue_apl = factory.IssueFactory(user=self.user,apikey=self.key,server=self.url)

			projects = project_apl.find_all()
			storys = {}
			for project in projects:
				storys[project.id] = issue_apl.find_story_by_project(project.key)
			# pprint(storys)

			projects_names = {str(project.id): project.name for project in projects}

			atomic_user_story_application = factories.AtomicUserStoryFactory()
			product_backlog_application = factories.ProductBacklogFactory()
			team_member_application = factories.TeamMemberFactory()

			for project_id, story_list in storys.items():
				for atomic_user_story_ in story_list:
					if atomic_user_story_application.retrive_by_external_uuid(atomic_user_story_.id): 
						continue
					atomic_user_story = factories_model.AtomicUserStoryFactory()
					atomic_user_story.name = atomic_user_story_.raw['fields']['summary']
					atomic_user_story.description = atomic_user_story_.raw['fields'].get('description')
					atomic_user_story.product_backlog = product_backlog_application.retrive_by_external_uuid(project_id).id
					try:
						atomic_user_story.created_by = team_member_application.retrive_by_external_id_and_project_name(atomic_user_story_.raw['fields']['creator']['accountId'], projects_names[project_id]).id
					except Exception as e:
						atomic_user_story.created_by = None
					try:
						atomic_user_story.activated_by = team_member_application.retrive_by_external_id_and_project_name(atomic_user_story_.raw['fields']['reporter']['accountId'], projects_names[project_id]).id
					except Exception as e:
						atomic_user_story.activated_by = None
					try:
						atomic_user_story.closed_by = team_member_application.retrive_by_external_id_and_project_name(atomic_user_story_.raw['fields']['assignee']['accountId'], projects_names[project_id]).id
					except Exception as e:
						atomic_user_story.closed_by = None
					# atomic_user_story.story_points = TODO
					# atomic_user_story.created_date = TODO
					atomic_user_story.activated_date = self.date_formater(None if type(next(iter(atomic_user_story_.raw['fields'].get('customfield_10018') or []), None)) != dict else self.resolve_start_date(atomic_user_story_.raw['fields']['customfield_10018']))
					atomic_user_story.closed_date = self.date_formater(atomic_user_story_.raw['fields'].get('duedate'))
					atomic_user_story.resolved_date = self.date_formater(atomic_user_story_.raw['fields'].get('resolutiondate'))
					atomic_user_story_application.create(atomic_user_story)
					self.create_application_reference('issue', atomic_user_story, atomic_user_story_.id, atomic_user_story_.self)

			logging.info("successfuly done (Atomic User Story)")
			return storys

		except e:
			pass

