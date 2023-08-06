from python_graphql_client import GraphqlClient

class GraphQLClient:

    def __init__(self, endpoint: str, headers: dict = None):
        """Insantiate the client."""
        self.client = GraphqlClient(endpoint=endpoint, headers=headers)

    
    def execute(
        self,
        query: str,
        variables: dict = None,
        operation_name: str = None,
        headers: dict = None,
    ):
      result = self.client.execute(
        query=query,
        variables=variables,
        operation_name=operation_name,
        headers=headers, 
      )
      errors = result.get('errors')
      if (errors != None): 
         raise Exception(errors)
      return result