"""HTTP API for PyTest runner."""
import logging
import os
import traceback
from typing import Dict, Any, Tuple

import flask
import flask_socketio  # type: ignore
import pkg_resources

from pytest_commander import runner
from pytest_commander import result_tree
from pytest_commander import environment

LOGGER = logging.getLogger(__name__)


def build_app(
    directory: str,
    watch_mode: str,
) -> Tuple[flask.Flask, flask_socketio.SocketIO, runner.PyTestRunner]:
    """Build a Flask app to serve the API and static files."""
    build_dir = pkg_resources.resource_filename(__name__, "web_client/build")
    LOGGER.debug("build_dir: %s", build_dir)
    static_dir = os.path.join(build_dir, "static")
    index_file = os.path.join(build_dir, "index.html")

    app = flask.Flask(__name__, root_path=build_dir, static_folder=static_dir)
    branch_schema = result_tree.BranchNodeSchema()
    socketio = flask_socketio.SocketIO(app)
    test_runner = runner.PyTestRunner(directory, socketio, watch_mode)

    @app.route("/")
    def index():
        return flask.send_file(index_file)

    @app.route("/<path:path>")
    def send_build(path):
        LOGGER.debug("Sending file: %s", path)
        return flask.send_from_directory(build_dir, path)

    @app.route("/api/v1/result-tree")
    def tree() -> Dict[str, Any]:
        try:
            return branch_schema.dump(test_runner.result_tree)
        except Exception:
            traceback.print_exc()
            raise

    @socketio.on("run test")
    def run_test(nodeid):
        LOGGER.info("Running test: %s", nodeid)
        test_runner.run_tests(nodeid)

    @socketio.on("start env")
    def start_env(nodeid):
        LOGGER.info("starting env: %s", nodeid)
        test_runner.start_env(nodeid)

    @socketio.on("stop env")
    def stop_env(nodeid):
        LOGGER.info("stopping env: %s", nodeid)
        test_runner.stop_env(nodeid)

    @socketio.on("connect")
    def connect():
        LOGGER.debug("Client connected")

    @socketio.on("disconnect")
    def disconnect():
        LOGGER.debug("Client disconnected")

    return app, socketio, test_runner
