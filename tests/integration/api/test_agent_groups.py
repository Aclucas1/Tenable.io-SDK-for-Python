import pytest

from tenable_io.api.agent_groups import AgentGroupSaveRequest
from tenable_io.api.models import Agent, AgentGroup, AgentGroupList, AgentList, FilterPagination, FilterSort

from tests.base import BaseTest


class TestAgentGroupsApi(BaseTest):

    def test_create_list_details_configure_delete(self, app, client):
        # Create agent group for testing.
        agent_group_name = app.session_name('test_agent_groups')
        agent_group_id = client.agent_groups_api.create(
            AgentGroupSaveRequest(
                agent_group_name
            )
        )
        assert agent_group_id, u'Create request returns valid ID.'

        # List agent groups
        agent_group_list = client.agent_groups_api.list()
        assert isinstance(agent_group_list, AgentGroupList), u'List request returns type.'

        test_agent_group = [a for a in agent_group_list.groups if a.id == agent_group_id]
        assert len(test_agent_group) == 1, u'Newly created agent group exists in list.'

        # Configure agent group name
        configured_agent_group_name = app.session_name('test_agent_groups_configure')
        client.agent_groups_api.configure(
            agent_group_id,
            AgentGroupSaveRequest(configured_agent_group_name)
        )

        # Get agent group details
        agent_group_details = client.agent_groups_api.details(agent_group_id)
        assert isinstance(agent_group_details, AgentGroup), u'Details request returns type.'
        assert agent_group_details.name == configured_agent_group_name, u'Agent group name must be configured.'
        for a in agent_group_details.agents:
            assert isinstance(a, Agent), u'Agents property represents type.'

        assert isinstance(agent_group_details.pagination, FilterPagination), u'Pagination represents type.'
        for s in agent_group_details.pagination.sort:
            assert isinstance(s, FilterSort), u'Sort represents type.'

        # Get agent group agents
        agent_group_agents = client.agent_groups_api.agents(agent_group_id)
        assert isinstance(agent_group_agents, AgentList), u'Agent groups agents request returns type.'
        for a in agent_group_agents.agents:
            assert isinstance(a, Agent), u'Agents property represents type.'
        assert isinstance(agent_group_agents.pagination, FilterPagination), u'Pagination represents type.'
        for s in agent_group_agents.pagination.sort:
            assert isinstance(s, FilterSort), u'Sort represents type.'

        # Delete the newly created agent group
        client.agent_groups_api.delete(agent_group_id)
