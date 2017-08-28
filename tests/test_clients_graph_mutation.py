# -*- coding: utf-8 -*-
#
# Copyright 2017 Swiss Data Science Center
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Tests for the knowledge graph client."""

import pytest

from renga.clients.deployer import Context, Execution
from renga.clients.project import Project


@pytest.fixture(scope='session')
def graph_mutation_client():
    """Return a graph mutation client."""
    from renga.clients.graph.mutation import GraphMutationClient
    return GraphMutationClient('http://localhost')


@pytest.fixture(scope='session')
def project_client():
    """Return a project client."""
    from renga.clients.project import ProjectClient
    return ProjectClient('http://localhost')


def test_knowledge_graph_init(graph_mutation_client, kg_requests):
    """Test knowldge graph client initialization."""
    return graph_mutation_client.named_types


def test_knowledge_graph_deploy_context(graph_mutation_client, kg_requests):
    """Test sending a deployment context to the KG."""
    context = Context(id=1234, spec={'image': 'hello-world', 'ports': '9999'})
    operation = graph_mutation_client.vertex_operation(context, 0,
                                                       'deployer:context')
    assert len(operation['element']['properties']) == 3

    vertex_id = graph_mutation_client.mutation(
        [operation], wait_for_response=True)

    assert vertex_id == 1234


def test_knowledge_graph_deploy_execution(graph_mutation_client, kg_requests):
    """Test sending a deployment context to the KG."""
    execution = Execution(id=1234, engine='docker', namespace='default')
    operation = graph_mutation_client.vertex_operation(execution, 0,
                                                       'deployer:execution')
    assert len(operation['element']['properties']) == 3

    vertex_id = graph_mutation_client.mutation(
        [operation], wait_for_response=True)
    assert vertex_id == 1234


def test_knowledge_graph_add_project(graph_mutation_client, kg_requests):
    """Test sending a deployment context to the KG."""
    project = Project(name='MyProject')
    operation = graph_mutation_client.vertex_operation(project, 0,
                                                       'project:project')
    assert len(operation['element']['properties']) == 1

    vertex_id = graph_mutation_client.mutation(
        [operation], wait_for_response=True)

    assert vertex_id == 1234


def test_knowledge_graph_add_project(project_client, kg_requests):
    """Test sending a deployment context to the KG."""
    project = project_client.create(name='My Project')

    assert isinstance(project, Project)
    assert project.name == 'My Project'
    assert project.vertex_id == 1234