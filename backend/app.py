from flask import Flask
from flask_restx import Api, Resource, fields
from flask_cors import CORS

from azure_service import fetch_repositories

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})


api = Api(
    app,
    version="1.0",
    title="Azure DevOps API",
    description="Backend API for Azure DevOps Repositories",
    doc="/docs"
)

ns = api.namespace("azure", description="Azure DevOps operations")


repo_model = api.model("Repository", {
    "id": fields.String,
    "name": fields.String,
    "project": fields.String,
    "remoteUrl": fields.String,
    "defaultBranch": fields.String
})

response_model = api.model("RepoResponse", {
    "success": fields.Boolean,
    "count": fields.Integer,
    "repositories": fields.List(fields.Nested(repo_model))
})


@ns.route("/repositories")
class Repositories(Resource):
    @api.doc("get_repositories")
    @api.marshal_with(response_model)
    def get(self):
        """
        Fetch all Azure DevOps repositories
        """
        return fetch_repositories()


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)