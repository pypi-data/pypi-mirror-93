import logging
logging.basicConfig(level=logging.INFO)

from jiraX import factories as factory
from pprint import pprint
from .base_entity import BaseEntity

from sro_db.application import factories
from sro_db.model import factories as factories_model

""" Scrum project """
class scrum_project(BaseEntity):
	"""
	Class responsible for retrieve projects from jira and save them on database
	"""
	def do (self,data):
		"""Retrieve all projects and save them on database. And save
		a scrum process for each project

		Args:
			data (dict): With user, key, server, organization_id and 
						 configuration_id to configure object

		Returns:
			list: List of all projects
		"""
		try:
			logging.info("Scrum Project")

			self.config(data)

			project_apl = factory.ProjectFactory(user=self.user,apikey=self.key,server=self.url)
			projects = project_apl.find_all()
			# pprint(projects)
		
			scrum_project_application = factories.ScrumAtomicProjectFactory()
			scrum_process_application = factories.ScrumProcessFactory()
			product_backlog_definition_application = factories.ProductBacklogDefinitionFactory()
			product_backlog_application = factories.ProductBacklogFactory()
			
			for project in projects:
				if scrum_project_application.retrive_by_external_uuid(project.id):
					continue
				#Scrum atomic project
				scrum_project = factories_model.ScrumAtomicProjectFactory()
				scrum_project.organization = self.organization
				scrum_project.name = project.name
				scrum_project.index = project.key
				scrum_project_application.create(scrum_project)
				self.create_application_reference('project', scrum_project, project.id, project.self)

				# Scrum process
				scrum_process = factories_model.ScrumProcessFactory()
				scrum_process.organization = self.organization
				scrum_process.name = project.name
				scrum_process.scrum_project_id = scrum_project.id
				scrum_process_application.create(scrum_process)
				self.create_application_reference('project', scrum_process, project.id, project.self)

				# Product backlog definition
				product_backlog_definition = factories_model.ProductBacklogDefinitionFactory()
				product_backlog_definition.name = project.name
				product_backlog_definition.scrum_process_id = scrum_process.id
				product_backlog_definition_application.create(product_backlog_definition)
				self.create_application_reference('project', product_backlog_definition, project.id, project.self)

				#Product backlog
				product_backlog = factories_model.ProductBacklogFactory()
				product_backlog.name = project.name
				product_backlog.product_backlog_definition = product_backlog_definition.id
				product_backlog_application.create(product_backlog)
				self.create_application_reference('project', product_backlog, project.id, project.self)

			logging.info("successfuly done (Scrum Project)")
			return projects

		except Exception as e:
			logging.info(e)


