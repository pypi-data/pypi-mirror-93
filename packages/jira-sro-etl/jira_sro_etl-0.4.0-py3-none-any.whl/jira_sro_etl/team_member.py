import logging
logging.basicConfig(level=logging.INFO)

from jiraX import factories as factory
from pprint import pprint
from .base_entity import BaseEntity

from sro_db.application import factories
from sro_db.model import factories as factories_model

""" Team member of a project """
class team_member(BaseEntity):
	"""
	Class responsible for retrieve team members from jira and save on database
	"""
	def do(self,data):
		"""Retrieve members from all projects and save on database

		Args:
			data (dict): With user, key, server, organization_id and 
						 configuration_id to configure object
		Returns:
			dict: Key is the project's key and value is a list with all members of this project
		"""
		try:
			logging.info("Team Member")

			self.config(data)

			project_apl = factory.ProjectFactory(user=self.user,apikey=self.key,server=self.url)
			user_apl = factory.UserFactory(user=self.user,apikey=self.key,server=self.url)
			projects = project_apl.find_all() 
			team_members = {str(project.id): user_apl.find_by_project(project.key) for project in projects}
			# pprint(team_members)

			projects_names = {str(project.id): project.name for project in projects}

			person_application = factories.PersonFactory()
			scrum_development_team_application = factories.DevelopmentTeamFactory()
			developer_application = factories.DeveloperFactory()
			team_member_application = factories.TeamMemberFactory()

			for project_id, members in team_members.items():
				for member in members:
					if team_member_application.retrive_by_external_id_and_project_name(member.accountId, projects_names[project_id]): 
						continue
					team_member = factories_model.DeveloperFactory()
					team_member.organization = self.organization
					person = person_application.retrive_by_external_uuid(member.accountId)
					team = scrum_development_team_application.retrive_by_external_uuid(project_id)
					team_member.person = person
					team_member.team = team
					team_member.team_role = 'developer'
					team_member.name = member.displayName
					developer_application.create(team_member)
					# self.create_application_reference('user', team_member, member.accountId, member.self)
			
			logging.info("successfuly done (Team Member)")
			return team_members

		except e:
			pass


