import logging
logging.basicConfig(level=logging.INFO)
from .base_entity import BaseEntity
from jiraX import factories as factory
from pprint import pprint

from sro_db.application import factories
from sro_db.model import factories as factories_model

""" Scrum development team """
class scrum_project_team(BaseEntity):
	"""
	Class responsible for retrieve teams from jira
	"""
	def do (self,data):
		"""Retrieve all teams

		Args:
			data (dict): With user, key and server to connect with jira

		Returns:
			list: List of all develpoment teams
		"""
		try:
			logging.info("Scrum Project Team")

			self.config(data)

			project_apl = factory.ProjectFactory(user=self.user,apikey=self.key,server=self.url)
			projects = project_apl.find_all() 
			scrum_teams = {str(project.id): f"{project.key}_scrum_team" for project in projects}
			# pprint(scrum_teams)

			scrum_project_application = factories.ScrumAtomicProjectFactory()
			scrum_team_application = factories.ScrumTeamFactory()

			for project_id,scrum_team_name in scrum_teams.items():
				if scrum_team_application.retrive_by_external_uuid(project_id):
					continue
				scrum_team = factories_model.ScrumTeamFactory()
				scrum_team.name = scrum_team_name
				scrum_team.organization = self.organization
				scrum_project = scrum_project_application.retrive_by_external_uuid(project_id)
				scrum_team.scrum_project = scrum_project.id
				scrum_team_application.create(scrum_team)
				self.create_application_reference('project', scrum_team, project_id)
			
			logging.info("successfuly done (Scrum Project Team)")
			return scrum_teams

		except e:
			pass
