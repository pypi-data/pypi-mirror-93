import logging
logging.basicConfig(level=logging.INFO)

from jiraX import factories as factory
from pprint import pprint
from .base_entity import BaseEntity

from sro_db.application import factories
from sro_db.model import factories as factories_model

""" User """
class user(BaseEntity):
	"""
	Class responsible for retrieve users from jira and sabe them on database
	"""
	def do(self,data):
		"""Retrieve all users from all projects and save on database

		Args:
			data (dict): With user, key, server, organization_id and 
						 configuration_id to configure object

		Returns:
			list: List with all users of all projects
		"""
		try:
			logging.info("User")

			self.config(data)

			project_apl = factory.ProjectFactory(user=self.user,apikey=self.key,server=self.url)
			user_apl = factory.UserFactory(user=self.user,apikey=self.key,server=self.url)

			projects = project_apl.find_all() 
			members = list({str(member.accountId): member for project in projects for member in user_apl.find_by_project(project.key)}.values())
			# pprint(members)

			person_application = factories.PersonFactory()

			for member in members:
				if person_application.retrive_by_external_uuid(member.accountId):
					continue
				person = factories_model.PersonFactory()
				person.organization = self.organization
				person.name = member.displayName
				if member.emailAddress != '':
					person.email = member.emailAddress
				person_application.create(person)

				self.create_application_reference('user', person, member.accountId, member.self)
			
			logging.info("successfuly done (User)")
			return members

		except e:
			pass




	


		
