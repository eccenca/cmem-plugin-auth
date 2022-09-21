"""Random values workflow plugin module"""
from typing import Sequence, Iterator, Dict, Any

from cmem_plugin_base.dataintegration.context import ExecutionContext
from cmem_plugin_base.dataintegration.description import Plugin, PluginParameter
from cmem_plugin_base.dataintegration.entity import (
    Entities,
    Entity,
    EntitySchema,
    EntityPath,
)
from cmem_plugin_base.dataintegration.plugins import WorkflowPlugin
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session


@Plugin(
    label="Access token Generator",
    description="Generates access token using OAuth2",
    documentation="""Generates access token using OAuth2""",
    parameters=[
        PluginParameter(
            name="oauth_token_url",
            label="Token endpoint URL",
            description="Token endpoint URL, must use HTTPS.",
        ),
        PluginParameter(
            name="oauth_client_id",
            label="Client Id",
            description="Client id obtained during registration",
        ),
        PluginParameter(
            name="oauth_client_secret",
            label="Values (Columns)",
            description="Client id obtained during registration",
        ),
    ],
)
class OAuth2(WorkflowPlugin):
    """Workflow Plugin: Generate oauth access token"""

    def __init__(
        self, oauth_token_url: str, oauth_client_id: str, oauth_client_secret: str
    ) -> None:
        self.oauth_token_url: str = oauth_token_url
        self.oauth_client_id: str = oauth_client_id
        self.oauth_client_secret: str = oauth_client_secret
        self.token: Dict[str, Any] = {}

    def execute(
        self, inputs: Sequence[Entities], context: ExecutionContext
    ) -> Entities:
        self.log.info("Start creating access token.")
        client = BackendApplicationClient(client_id=self.oauth_client_id)
        oauth = OAuth2Session(client=client)
        self.token = oauth.fetch_token(
            token_url=self.oauth_token_url,
            client_id=self.oauth_client_id,
            client_secret=self.oauth_client_secret,
        )
        return self.get_or_create_entities(inputs)

    def get_or_create_entities(self, inputs: Sequence[Entities]) -> Entities:
        """
        if exists append oauth access token to first entity or
        create new one wth oauth access token path
        """
        entity = None
        if inputs:
            if inputs[0].entities:
                entity = next(self.get_entities(inputs[0]))
                schema = self.clone_schema(inputs[0].schema)
        if not entity:
            schema = EntitySchema(
                type_uri="https://eccenca.com/plugin/auth",
                paths=[],
            )
            entity = Entity(uri="", values=[])

        entity.uri = "urn:Parameter"
        entity.values.append([self.token["access_token"]])

        schema.type_uri = "urn:ParameterSettings"
        schema.paths.append(EntityPath(path="oauth_access_token"))

        return Entities(entities=[entity], schema=schema)

    def get_entities(self, entities: Entities) -> Iterator[Entity]:
        """Generate python entity iterator"""
        for entity in entities.entities:
            yield self.clone_entity(entity)

    def clone_entity(self, entity: Entity) -> Entity:
        """Clone java entity to python entity"""
        self.log.info("Clone java entity to python entity")
        values = []
        for value in entity.values:
            values.append(value)
        return Entity(uri=entity.uri, values=values)

    def clone_schema(self, schema: EntitySchema) -> EntitySchema:
        """Clone java schema to python schema"""
        self.log.info("Clone java schema to python schema")
        paths = []
        for path in schema.paths:
            paths.append(path)
        return EntitySchema(type_uri=schema.type_uri, paths=paths)
