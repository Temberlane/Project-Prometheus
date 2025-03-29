import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModelForSequenceClassification

import grpc
import distributed_ai_pb2
import distributed_ai_pb2_grpc
from concurrent import futures

class NodeServiceServicer(distributed_ai_pb2_grpc.NodeServiceServicer):
    def __init__(self, model_name="bert-base-cased", node_id="node_A"):
        self.node_id = node_id
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)

    def Predict(self, request, context):
        input_text = request.input_text
        inputs = self.tokenizer(input_text, return_tensors="pt")
        outputs = self.model(**inputs)
        # Take a simple argmax of logits as a placeholder prediction.
        prediction_index = int(torch.argmax(outputs.logits, dim=1))
        return distributed_ai_pb2.PredictResponse(
            prediction=f"{self.node_id} prediction index: {prediction_index}"
        )

    def Critique(self, request, context):
        # Here you might analyze how the other node's rationale compares to your predictions
        # and produce a critique or a suggestion
        critique_content = (
            f"{self.node_id} critique > Node {request.node_id}'s prediction:{request.previous_prediction} "
            f"Rationale: {request.rationale}"
        )
        return distributed_ai_pb2.CritiqueResponse(critique=critique_content)

def serve(node_id="node_A", port=50051, model_name="bert-base-cased"):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    distributed_ai_pb2_grpc.add_NodeServiceServicer_to_server(
        NodeServiceServicer(model_name=model_name, node_id=node_id),
        server
    )
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    print(f"{node_id} is listening on port {port}...")
    server.wait_for_termination()

if __name__ == "__main__":
    serve(node_id="node_B", port=50053)