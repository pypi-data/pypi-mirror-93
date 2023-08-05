"""FastAPI app."""
import json
import os
import yaml
from typing import Any, Dict, List

from fastapi import Body, Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from PLATER.services.models import (
    Message, ReasonerRequest, CypherRequest, SimpleSpecResponse, SimpleSpecElement,
    GraphSummaryResponse, CypherResponse, PredicatesResponse
)
from PLATER.services.config import config
from PLATER.services.util.bl_helper import BLHelper
from PLATER.services.util.graph_adapter import GraphInterface
from PLATER.services.util.logutil import LoggingUtil
from PLATER.services.util.overlay import Overlay
from PLATER.services.util.question import Question

TITLE = config.get('PLATER_TITLE', 'Plater API')
VERSION = os.environ.get('PLATER_VERSION', '1.0.0')

logger = LoggingUtil.init_logging(
    __name__,
    config.get('logging_level'),
    config.get('logging_format'),
)

APP = FastAPI()


def get_graph_interface():
    """Get graph interface."""
    return GraphInterface(
        host=config.get('DB_HOST'),
        port=config.get('DB_PORT'),
        auth=(
            config.get('DB_USERNAME'),
            config.get('DB_PASSWORD')
        ),
        db_type=config.get('DB_TYPE'),
        db_name=config.get('DB_NAME')
    )


def get_bl_helper():
    """Get Biolink helper."""
    return BLHelper(config.get('BL_HOST', 'https://bl-lookup-sri.renci.org'))


def get_example(operation: str):
    """Get example for operation."""
    with open(os.path.join(
        os.path.dirname(__file__),
        "..",
        "examples",
        f"{operation}.json",
    )) as stream:
        return json.load(stream)


async def reasoner_api(
        request: ReasonerRequest = Body(
            ...,
            example=get_example("reasoner"),
        ),
        graph_interface: GraphInterface = Depends(get_graph_interface),
) -> Message:
    """Handle TRAPI request."""
    request_json = request.dict()
    question = Question(request_json["message"])
    response = await question.answer(graph_interface)
    request_json.update({'message': response})
    return request_json


APP.add_api_route(
    "/query",
    reasoner_api,
    methods=["POST"],
    response_model=ReasonerRequest,
    summary="Query Reasoner API",
    description="Given a question graph return question graph plus answers.",
    tags=["translator"]
)

APP.add_api_route(
    "/reasonerapi",
    reasoner_api,
    methods=["POST"],
    response_model=ReasonerRequest,
    deprecated=True,
)


async def cypher(
        request: CypherRequest = Body(
            ...,
            example={"query": "MATCH (n) RETURN count(n)"},
        ),
        graph_interface: GraphInterface = Depends(get_graph_interface),
) -> CypherResponse:
    """Handle cypher."""
    request = request.dict()
    results = await graph_interface.run_cypher(
        request["query"],
        return_errors=True,
    )
    return results


APP.add_api_route(
    "/cypher",
    cypher,
    methods=["POST"],
    response_model=CypherResponse,
    summary="Run cypher query",
    description=(
        "Runs cypher query against the Neo4j instance, and returns an "
        "equivalent response expected from a Neo4j HTTP endpoint "
        "(https://neo4j.com/docs/rest-docs/current/)."
    ),
)


async def predicates(
        graph_interface: GraphInterface = Depends(get_graph_interface),
) -> PredicatesResponse:
    """Handle /predicates."""
    return graph_interface.get_schema()


APP.add_api_route(
    "/predicates",
    predicates,
    methods=["GET"],
    response_model=PredicatesResponse,
    summary="Get one-hop connection types",
    description=(
        "Returns an object where outer keys represent source types with "
        "second level keys as targets. And the values of the second level "
        "keys is the type of possible edge typesthat connect these concepts."
    ),
    tags=["translator"]
)


APP.add_api_route(
    "/graph/schema",
    predicates,
    methods=["GET"],
    response_model=Dict,
    summary="Get one-hop connection types",
    description="Get one-hop connection types",
    deprecated=True
)


async def simple_spec(
        source: str = None,
        target: str = None,
        graph_interface: GraphInterface = Depends(get_graph_interface),
        bl_helper: BLHelper = Depends(get_bl_helper),
) -> SimpleSpecResponse:
    """Handle simple spec."""
    source_id = source
    target_id = target
    if source_id or target_id:
        minischema = []
        mini_schema_raw = await graph_interface.get_mini_schema(
            source_id,
            target_id,
        )
        for row in mini_schema_raw:
            source_labels = await bl_helper.get_most_specific_concept(
                row['source_label']
            )
            target_labels = await bl_helper.get_most_specific_concept(
                row['target_label']
            )
            for source_type in source_labels:
                for target_type in target_labels:
                    minischema.append((
                        source_type,
                        row['predicate'],
                        target_type,
                    ))
        minischema = list(set(minischema))  # remove dups
        return list(map(lambda x: SimpleSpecElement(**{
                'source_type': x[0],
                'target_type': x[2],
                'edge_type': x[1],
            }), minischema))
    else:
        schema = graph_interface.get_schema()
        reformatted_schema = []
        for source_type in schema:
            for target_type in schema[source_type]:
                for edge in schema[source_type][target_type]:
                    reformatted_schema.append(SimpleSpecElement(**{
                        'source_type': source_type,
                        'target_type': target_type,
                        'edge_type': edge
                    }))
        return reformatted_schema


APP.add_api_route(
    "/simple_spec",
    simple_spec,
    methods=["GET"],
    response_model=SimpleSpecResponse,
    summary="Get one-hop connection schema",
    description=(
        "Returns a list of available predicates when choosing a single source "
        "or target curie. Calling this endpoint with no query parameters will "
        "return all possible hops for all types."
    ),
)


async def get_reasoner_api(
        graph_interface: GraphInterface = Depends(get_graph_interface),
) -> List[Message]:
    """Handle GET /reasonerapi."""
    return Question.transform_schema_to_question_template(
        graph_interface.get_schema()
    )


APP.add_api_route(
    "/reasonerapi",
    get_reasoner_api,
    methods=["GET"],
    response_model=List[Message],
    summary="Get question templates",
    description=(
        "Returns a list of question templates that can be used to query this "
        "plater instance."
    ),
)


async def graph_summary(
        graph_interface: GraphInterface = Depends(get_graph_interface),
) -> GraphSummaryResponse:
    """Handle GET /graph_summary."""
    graph_interface.get_schema()
    return graph_interface.summary


APP.add_api_route(
    "/graph/summary",
    graph_summary,
    methods=["GET"],
    response_model=GraphSummaryResponse,
    summary="Get graph summary",
    description="Returns a summary of the graph.",
)


async def overlay(
        request: ReasonerRequest = Body(
            ...,
            example={"message": get_example("overlay")},
        ),
        graph_interface: GraphInterface = Depends(get_graph_interface),
) -> Message:
    """Handle TRAPI request."""
    overlay_class = Overlay(graph_interface)
    return await overlay_class.overlay_support_edges(request.dict()["message"])


APP.add_api_route(
    "/overlay",
    overlay,
    methods=["POST"],
    response_model=Message,
    description=(
        "Given a ReasonerAPI graph, add support edges for any nodes linked in "
        "result bindings."
    ),
    summary="Overlay results with available connections between each node.",
    tags=["translator"]
)


async def about() -> Any:
    """Handle /about."""
    with open('about.json') as f:
        return json.load(f)


APP.add_api_route(
    "/about",
    about,
    methods=["GET"],
    response_model=Any,
    summary="JSON about dataset",
    description="Returns a JSON describing dataset.",
)


async def one_hop(
        source_type: str,
        target_type: str,
        curie: str,
        graph_interface: GraphInterface = Depends(get_graph_interface),
) -> List[Dict]:
    """Handle one-hop."""
    return await graph_interface.get_single_hops(
        source_type,
        target_type,
        curie,
    )


APP.add_api_route(
    "/{source_type}/{target_type}/{curie}",
    one_hop,
    methods=["GET"],
    response_model=List,
    summary=(
        "Get one hop results from source type to target type. "
        "Note: Please GET /predicates to determine what target goes "
        "with a source"
    ),
    description=(
        "Returns one hop paths from `source_node_type`  with `curie` "
        "to `target_node_type`."
    ),
)


async def node(
        node_type: str,
        curie: str,
        graph_interface: GraphInterface = Depends(get_graph_interface),
) -> List[List[Dict]]:
    """Handle node lookup."""
    return await graph_interface.get_node(
        node_type,
        curie,
    )


APP.add_api_route(
    "/{node_type}/{curie}",
    node,
    methods=["GET"],
    response_model=List,
    summary="Find `node` by `curie`",
    description="Returns `node` matching `curie`.",
)


def construct_open_api_schema():

    if APP.openapi_schema:
        return APP.openapi_schema
    open_api_schema = get_openapi(
        title=TITLE,
        version=VERSION,
        description='',
        routes=APP.routes
    )

    open_api_extended_file_path = config.get_resource_path('../openapi-config.yaml')
    with open(open_api_extended_file_path) as open_api_file:
        open_api_extended_spec = yaml.load(open_api_file, Loader=yaml.SafeLoader)

    x_translator_extension = open_api_extended_spec.get("x-translator")
    contact_config = open_api_extended_spec.get("contact")
    terms_of_service = open_api_extended_spec.get("termsOfService")
    servers_conf = open_api_extended_spec.get("servers")
    tags = open_api_extended_spec.get("tags")
    title_override = open_api_extended_spec.get("title") or TITLE
    description = open_api_extended_spec.get("description")

    if tags:
        open_api_schema['tags'] = tags

    if x_translator_extension:
        # if x_translator_team is defined amends schema with x_translator extension
        open_api_schema["info"]["x-translator"] = x_translator_extension

    if contact_config:
        open_api_schema["info"]["contact"] = contact_config

    if terms_of_service:
        open_api_schema["info"]["termsOfService"] = terms_of_service

    if description:
        open_api_schema["info"]["description"] = description

    if title_override:
        open_api_schema["info"]["title"] = title_override

    if servers_conf:
        open_api_schema["servers"] = servers_conf

    return open_api_schema


APP.openapi_schema = construct_open_api_schema()

# CORS
APP.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

