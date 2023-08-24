import uuid

import pika
from flask import Flask, jsonify, request

conn_param = pika.ConnectionParameters("localhost")
connection = pika.BlockingConnection(conn_param)
channel = connection.channel()

lookup_table = {}

channel.queue_declare("computation-request-queue")
# channel.queue_declare("computation-response-queue")

app = Flask(__name__)


@app.route("/calculate/<int:num>", methods=["GET"])
def calculate(num):
    correlation_id = str(uuid.uuid4())
    channel.basic_publish(
        exchange="",
        routing_key="computation-request-queue",
        properties=pika.BasicProperties(correlation_id=correlation_id),
        body=str(num),
    )
    return (
        jsonify(
            {"message": "Computation request sent.", "correlation_id": correlation_id}
        ),
        202,
    )


@app.route("/result/<uuid>", methods=["GET"])
def result(uuid):
    res = lookup_table.get(uuid)
    if res is None:
        return (
            jsonify({"message": "Processing."}),
            202,
        )
    return jsonify({"result": res}), 200


@app.route("/write-result", methods=["POST"])
def write_result():
    body = request.json

    id = body.get("id")
    result = body.get("result")
    lookup_table[id] = result
    return {"message": "received"}


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
